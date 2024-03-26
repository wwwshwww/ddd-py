import asyncio
import os
from contextlib import asynccontextmanager

import pytest_asyncio
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)


def load_schema() -> list[str]:
    """スキーマ定義ファイルを読み込む (デフォルトのファイルパスは .envrc に記載)

    Returns:
        list[str]: _description_
    """
    schema_path = os.getenv("DB_SCHEMA_PATH")
    schemas: list[str] = []
    with open(schema_path, encoding="utf-8", mode="r") as f:
        schemas = f.read().split(";")
    return schemas[:-1]  # 末尾に改行コードとかが入るのでトリムする


table_schemas: list[str] = load_schema()

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
            tasks = [
                asyncio.create_task(conn.execute(text(sc))) for sc in table_schemas
            ]
            await asyncio.gather(*tasks)
            # for sql in table_schemas:
            #     await conn.execute(text(sql))

        try:
            yield async_scoped_session_factory
        finally:
            await db_engine.dispose()

    return fn
