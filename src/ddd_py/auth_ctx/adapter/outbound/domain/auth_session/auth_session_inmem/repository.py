import copy

from ddd_py.auth_ctx.domain.auth_session import auth_session


class Repository(auth_session.Repository):
    def __init__(self, data_store: dict[auth_session.Id, auth_session.AuthSession]):
        self.data_store = data_store

    def bulk_get(
        self, ids: list[auth_session.Id]
    ) -> dict[auth_session.Id, auth_session.AuthSession]:
        result: dict[auth_session.Id, auth_session.AuthSession] = {}
        not_found_ids: list[auth_session.Id] = []
        for i in ids:
            d = self.data_store.get(i, None)
            if d is None:
                not_found_ids.append(i)
            result[i] = copy.deepcopy(d)

        if len(not_found_ids) > 0:
            raise auth_session.RepositoryError(
                f"missing IDs: {[v.value() for v in not_found_ids]}"
            )

        return result

    def get(self, id: auth_session.Id) -> auth_session.AuthSession:
        return self.bulk_get([id])[id]

    def bulk_save(self, posts: list[auth_session.AuthSession]) -> None:
        for d in posts:
            self.data_store[d.id] = copy.deepcopy(d)
        return

    def save(self, post: auth_session.AuthSession) -> None:
        return self.bulk_save([post])

    def bulk_delete(self, ids: list[auth_session.Id]) -> None:
        not_found_ids: list[auth_session.Id] = []
        for i in ids:
            if i not in self.data_store:
                not_found_ids.append(i)

            del self.data_store[i]

        if len(not_found_ids) > 0:
            raise auth_session.RepositoryError(
                f"missing IDs: {[v.value() for v in not_found_ids]}"
            )

        return

    def delete(self, id: auth_session.Id) -> None:
        return self.bulk_delete([id])
