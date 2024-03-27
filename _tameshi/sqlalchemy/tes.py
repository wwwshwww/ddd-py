import asyncio

import conf
import pytest
import pytest_asyncio
import schema_getter
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

DATABASE_NAME = "test_dayo"
CLEANUP_TABLES = ["user"]


@pytest_asyncio.fixture(scope="module")
async def setup_db():
    init_engine = create_async_engine(
        f"mysql+aiomysql://{conf.user}:{conf.password}@{conf.host}/",
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
        f"mysql+aiomysql://{conf.user}:{conf.password}@{conf.host}/{DATABASE_NAME}",
        echo=True,
        poolclass=NullPool,
    )
    async with engine.begin() as conn:
        tasks = [
            asyncio.create_task(conn.execute(text(sc)))
            for sc in schema_getter.table_schemas
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
async def test_func1(setup_session: AsyncSession):  # pylint: disable=redefined-outer-name
    print(setup_session)
