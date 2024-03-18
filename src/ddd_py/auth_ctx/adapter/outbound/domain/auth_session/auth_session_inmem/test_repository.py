import unittest
from datetime import datetime

from ddd_py.auth_ctx.adapter.outbound.domain.auth_session.auth_session_inmem.repository import (
    Repository,
    data_store,
)
from ddd_py.auth_ctx.domain.auth_session import auth_session


class TestRepository(unittest.TestCase):
    fixtures: list[auth_session.AuthSession] = [
        auth_session.generate_auth_session("", datetime(2011, 11, 11, 0, 0, 0, 0)),
        auth_session.generate_auth_session("", datetime(2011, 11, 12, 0, 0, 0, 0)),
        auth_session.generate_auth_session("", datetime(2011, 11, 13, 0, 0, 0, 0)),
    ]
    fixture_ids: list[auth_session.Id] = [e.id for e in fixtures]

    def setUp(self):
        data_store.clear()
        for e in self.fixtures:
            data_store[e.id] = e

    def test_get(self):
        repo = Repository()

        aus0 = repo.get(self.fixture_ids[0])
        print(f"[actual]: {id(aus0)}, [expected]: {id(self.fixtures[0])}")
        self.assertTrue(aus0 == self.fixtures[0])

        auss = repo.bulk_get(self.fixture_ids)
        actual = list(auss.values())
        excepted = list(self.fixtures)

        self.assertCountEqual(actual, excepted)


if __name__ == "__main__":
    unittest.main()
