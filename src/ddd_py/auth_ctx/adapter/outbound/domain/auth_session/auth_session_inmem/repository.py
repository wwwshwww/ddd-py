from ddd_py.auth_ctx.domain.auth_session import auth_session


class Repository(auth_session.Repository):
    def __init__(self, db):
        self.db = db

    def bulk_get(
        self, ids: list[auth_session.Id]
    ) -> dict[auth_session.Id, auth_session.AuthSession]:
        # TODO
        return []

    def get(self, id: auth_session.Id) -> auth_session.AuthSession:
        # TODO
        pass

    def bulk_save(self, posts: list[auth_session.AuthSession]) -> None:
        # TODO
        return

    def save(self, post: auth_session.AuthSession) -> None:
        # TODO
        pass

    def bulk_delete(self, ids: list[auth_session.Id]) -> None:
        # TODO
        return

    def delete(self, id: auth_session.Id) -> None:
        # TODO
        pass
