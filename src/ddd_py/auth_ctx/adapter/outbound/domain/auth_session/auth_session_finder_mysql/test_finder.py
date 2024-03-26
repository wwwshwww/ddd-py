import logging
import uuid
from dataclasses import dataclass
from datetime import datetime

import pytest
import pytest_asyncio
from deepdiff import DeepDiff
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
)

from ddd_py.auth_ctx.adapter.outbound.domain.auth_session.auth_session_finder_mysql.finder import (
    Finder,
)
from ddd_py.auth_ctx.adapter.outbound.domain.auth_session.auth_session_mysql.models import (
    AuthSession,
)
from ddd_py.auth_ctx.domain.auth_session import auth_session, auth_session_finder
from ddd_py.common.adapter.mysql.conftest import (  # noqa: F401 pylint: disable=W0611
    general_engine,
    initializer,
)

logger = logging.getLogger(__name__)


@pytest_asyncio.fixture(scope="function")
async def session(initializer):  # noqa: F811, pylint: disable=W0621
    label = "auth_session_finder_test"
    session_factory: async_scoped_session[AsyncSession]
    async with initializer(label) as session_factory:
        async with session_factory() as session:
            yield session


data: list[AuthSession] = [
    AuthSession(
        id=uuid.UUID("b00ee983-618e-4fe2-9e56-11f5d359a092"),
        client_state="hoshino",
        started_at=datetime(2022, 1, 1),
        expires_at=datetime(2022, 1, 2),
    ),
    AuthSession(
        id=uuid.UUID("6844f2cc-4d1b-42e0-8bd8-c24f1044f2bb"),
        client_state="yume",
        started_at=datetime(2022, 1, 2),
        expires_at=datetime(2022, 1, 3),
    ),
    AuthSession(
        id=uuid.UUID("28edf2e6-282b-41a8-8a25-4022a17d2837"),
        client_state="abc",
        started_at=datetime(2022, 1, 2),
        expires_at=datetime(2022, 1, 3),
    ),
]


@pytest.mark.asyncio
async def test_finder(session: AsyncSession):  # pylint: disable=W0621
    async with session.begin():
        session.add_all(data)

    async with session.begin():
        finder = Finder(session)

        @dataclass
        class TestCase:
            desc: str
            arg: auth_session_finder.FilteringOptions | None
            expected: list[auth_session.Id]

        tcs: list[TestCase] = [
            TestCase(
                desc="無指定の場合は全件取得できる",
                arg=None,
                expected=[auth_session.Id(d.id) for d in data],
            ),
            TestCase(
                desc="複数 id で検索し、ヒットするレコードの識別子だけを一括取得できる",
                arg=auth_session_finder.FilteringOptions(
                    id_in=[
                        auth_session.Id(data[0].id),
                        auth_session.Id(data[1].id),
                        auth_session.Id(uuid.uuid4()),
                    ],
                ),
                expected=[auth_session.Id(data[0].id), auth_session.Id(data[1].id)],
            ),
        ]

        for t in tcs:
            logger.info(t.desc)
            actual = await finder.find(t.arg)
            assert not DeepDiff(actual, t.expected, ignore_order=True)
