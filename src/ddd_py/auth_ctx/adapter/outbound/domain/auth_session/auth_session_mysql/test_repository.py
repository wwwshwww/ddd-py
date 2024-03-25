import asyncio

import pytest
import pytest_asyncio
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from ddd_py.common.adapter.mysql import test_utils

DATABASE_NAME = "auth_session_test"
CLEANUP_TABLES = ["user"]

db_user = "root"
db_password = "root"
db_host = "localhost"

# テスト戦略：
# テストモジュール（ファイル）毎に database を作成し、複数の repository テストの並行実施を可能にする。
# DBのテーブル構造は RDB Model に依存させない。テスト用 DB のテーブルは別ファイルから読み込んだ内容をもとに初期化する。
# sqldef を採用することにより、スキーマ定義は常に最新のものだけを保持しておけば良いため都合が良い。
# スキーマ定義ファイルのパスは環境変数から取得する。./.envrc に記載済みのため direnv を使用すれば手動設定は不要。


async def cleanup_table(session: AsyncSession, tables: list[str] = None):
    if tables is None:
        return

    await session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    tasks = [
        asyncio.create_task(session.execute(text(f"TRUNCATE TABLE {t}")))
        for t in tables
    ]
    await asyncio.gather(*tasks)


@pytest_asyncio.fixture(scope="module")
async def setup_db():
    init_engine = create_async_engine(
        f"mysql+aiomysql://{db_user}:{db_password}@{db_host}/",
        echo=True,
        poolclass=NullPool,
    )
    try:
        async with init_engine.begin() as conn:
            sql1 = f"DROP DATABASE IF EXISTS {DATABASE_NAME}"
            await conn.execute(text(sql1))
            sql2 = f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME} CHARACTER SET = 'utf8mb4'"
            await conn.execute(text(sql2))
    finally:
        await init_engine.dispose()

    engine = create_async_engine(
        f"mysql+aiomysql://{db_user}:{db_password}@{db_host}/{DATABASE_NAME}",
        echo=True,
        poolclass=NullPool,
    )
    async with engine.begin() as conn:
        tasks = [
            asyncio.create_task(conn.execute(text(sc)))
            for sc in test_utils.table_schemas
        ]
        await asyncio.gather(*tasks)

    async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async_scoped_session_factory = async_scoped_session(
        async_session_factory,
        scopefunc=asyncio.current_task,
    )

    try:
        yield async_scoped_session_factory
    finally:
        await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def setup_session(setup_db: async_scoped_session[AsyncSession]):  # pylint: disable=redefined-outer-name
    try:
        async with setup_db() as session:
            yield session
    finally:
        print("done")


@pytest.mark.asyncio
async def test_get(setup_session: AsyncSession):  # pylint: disable=redefined-outer-name
    print(setup_session)


@pytest.mark.asyncio
async def test_save(setup_session: AsyncSession):  # pylint: disable=redefined-outer-name
    print(setup_session)


@pytest.mark.asyncio
async def test_delete(setup_session: AsyncSession):  # pylint: disable=redefined-outer-name
    print(setup_session)
