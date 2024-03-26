from datetime import datetime

import pytest
import pytest_asyncio
from deepdiff import DeepDiff
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
)

from ddd_py.auth_ctx.domain.auth_session import auth_session
from ddd_py.common.adapter.mysql.conftest import (  # noqa: F401 pylint: disable=W0611
    general_engine,
    initializer,
)

from .repository import Repository


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
