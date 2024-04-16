from collections.abc import Callable
from contextlib import _AsyncGeneratorContextManager
from datetime import datetime

import pytest
import pytest_asyncio
from deepdiff import DeepDiff
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
)

from ddd_py.auth_ctx.adapter.outbound.domain.auth_session.auth_session_mysql.repository import (
    Repository,
)
from ddd_py.auth_ctx.domain.auth_session import auth_session
from ddd_py.common.adapter.mysql.conftest import (
    general_engine,
    initializer,
)


@pytest_asyncio.fixture(scope="function")
async def session(
    initializer: Callable[  # noqa: F811, pylint: disable=W0621
        [str], _AsyncGeneratorContextManager[async_scoped_session[AsyncSession]]
    ],
):
    label = "auth_session_repo_test"
    session_factory: async_scoped_session[AsyncSession]
    async with initializer(label) as session_factory:
        async with session_factory() as ss:
            yield ss


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
async def test_repository(session: AsyncSession):  # pylint: disable=W0621
    async with session.begin():
        repo1 = Repository(session)
        await repo1.bulk_save(dummies)

    async with session.begin():
        repo2 = Repository(session)
        actual = await repo2.bulk_get(dummy_ids)
        assert not DeepDiff(list(actual.values()), dummies, ignore_order=True)

    async with session.begin():
        repo3 = Repository(session)
        await repo3.bulk_delete(dummy_ids[:2])
        actual = await repo3.bulk_get(dummy_ids[2:])
        assert not DeepDiff(list(actual.values()), dummies[2:], ignore_order=True)
