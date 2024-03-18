import copy
from datetime import datetime

import pytest
from deepdiff import DeepDiff

from ddd_py.auth_ctx.adapter.outbound.domain.auth_session.auth_session_inmem.repository import (
    Repository,
    data_store,
)
from ddd_py.auth_ctx.domain.auth_session import auth_session

dummies: list[auth_session.AuthSession] = [
    auth_session.generate_auth_session("", datetime(2011, 11, 11, 0, 0, 0, 0)),
    auth_session.generate_auth_session("", datetime(2011, 11, 12, 0, 0, 0, 0)),
    auth_session.generate_auth_session("", datetime(2011, 11, 13, 0, 0, 0, 0)),
]

dummy_ids: list[auth_session.Id] = [e.id for e in dummies]


@pytest.fixture
def repo():
    print("\n******* initialized")
    data_store.clear()
    for e in dummies:
        data_store[e.id] = copy.deepcopy(e)
    yield Repository()
    print("******* closed")


def test_get(repo: auth_session.Repository):  # pylint: disable=W0621
    aus0 = repo.get(dummy_ids[0])
    assert aus0 == dummies[0]

    auss = repo.bulk_get(dummy_ids)
    actual = list(auss.values())

    print(f"[actual ids]: {[id(e) for e in actual]}")
    print(f"[expected ids]: {[id(e) for e in dummies]}")

    assert not DeepDiff(actual, dummies, ignore_order=True)
