from typing import List

from ddd_py.auth_ctx.domain.auth_session import auth_session


class Repository(auth_session.Repository):
    def __init__(self, db):
        self.db = db

    def bulk_get(
        self, ids: auth_session.List[auth_session.Id]
    ) -> List[auth_session.AuthSession]:
        # TODO
        return []

    def bulk_save(self, posts: auth_session.List[auth_session.AuthSession]) -> None:
        # TODO
        return

    def bulk_delete(self, ids: auth_session.List[auth_session.Id]) -> None:
        # TODO
        return
