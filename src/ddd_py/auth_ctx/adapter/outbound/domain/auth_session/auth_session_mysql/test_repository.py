import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from deepdiff import DeepDiff
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from ddd_py.auth_ctx.domain.auth_session import auth_session
from ddd_py.common.adapter.mysql import test_utils

from .repository import Repository

DATABASE_NAME = "auth_session_test"
CLEANUP_TABLES = ["user"]

db_user = "root"
db_password = "root"
db_host = "localhost"


# テスト戦略：
# テストケース毎に database を作成し、pytest-xdist による repository テストの並行実施を可能にする。
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


@pytest_asyncio.fixture(scope="session")
async def general_engine():
    e = create_async_engine(
        f"mysql+aiomysql://{db_user}:{db_password}@{db_host}/",
        echo=True,
        poolclass=NullPool,
    )
    try:
        yield e
    finally:
        await e.dispose()


@pytest_asyncio.fixture(scope="session")
async def initializer(general_engine: AsyncEngine):  # pylint: disable=redefined-outer-name
    @asynccontextmanager
    async def fn(db_name: str):
        async with general_engine.begin() as conn:
            sql1 = f"DROP DATABASE IF EXISTS {db_name}"
            sql2 = f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET = 'utf8mb4'"
            await conn.execute(text(sql1))
            await conn.execute(text(sql2))

        db_engine = create_async_engine(
            f"mysql+aiomysql://{db_user}:{db_password}@{db_host}/{db_name}",
            echo=True,
            poolclass=NullPool,
        )
        async_session_factory = async_sessionmaker(db_engine, expire_on_commit=False)
        async_scoped_session_factory = async_scoped_session(
            async_session_factory,
            scopefunc=asyncio.current_task,
        )

        async with db_engine.begin() as conn:
            # tasks = [
            #     asyncio.create_task(conn.execute(text(sc)))
            #     for sc in test_utils.table_schemas
            # ]
            # await asyncio.gather(*tasks)
            for sql in test_utils.table_schemas:
                await conn.execute(text(sql))

        try:
            yield async_scoped_session_factory
        finally:
            await db_engine.dispose()

    return fn


@pytest_asyncio.fixture(scope="function")
async def auth_session_test_session(initializer):  # pylint: disable=redefined-outer-name
    label = "auth_session_test"
    session_factory: async_scoped_session[AsyncSession]
    async with initializer(label) as session_factory:
        async with session_factory() as session:
            yield session


dummies: list[auth_session.AuthSession] = [
    auth_session.generate_auth_session(
        auth_session.ClientState("a"), datetime(2011, 11, 11, 0, 0, 0, 0)
    ),
    auth_session.generate_auth_session(
        auth_session.ClientState(""), datetime(2011, 11, 12, 0, 0, 0, 0)
    ),
    auth_session.generate_auth_session(
        auth_session.ClientState("c"), datetime(2011, 11, 13, 0, 0, 0, 0)
    ),
]

dummy_ids: list[auth_session.Id] = [e.id for e in dummies]


@pytest.mark.asyncio
async def test_repository(
    auth_session_test_session: AsyncSession,
):  # pylint: disable=redefined-outer-name
    async with auth_session_test_session.begin():
        repo1 = Repository(auth_session_test_session)
        await repo1.bulk_save(dummies)

    async with auth_session_test_session.begin():
        repo2 = Repository(auth_session_test_session)
        actual = await repo2.bulk_get(dummy_ids)
        assert not DeepDiff(list(actual.values()), dummies, ignore_order=True)

    async with auth_session_test_session.begin():
        repo3 = Repository(auth_session_test_session)
        await repo3.bulk_delete(dummy_ids[:2])
        actual = await repo3.bulk_get(dummy_ids[2:])
        assert not DeepDiff(list(actual.values()), dummies[2:], ignore_order=True)
