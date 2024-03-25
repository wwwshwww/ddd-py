from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ddd_py.auth_ctx.domain.auth_session import auth_session

from .models import AuthSession, restore


class Repository(auth_session.Repository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def bulk_get(
        self, ids: list[auth_session.Id]
    ) -> dict[auth_session.Id, auth_session.AuthSession]:
        if len(ids) == 0:
            return {}
        query = select(AuthSession).where(AuthSession.id.in_(ids))
        rows = await self.db.scalars(query)
        result = {auth_session.Id(row.id): restore(row) for row in rows}

        if len(result) != len(ids):
            found_ids = [auth_session.Id(row.id) for row in rows]
            raise auth_session.RepositoryGetError(
                "one or more specified IDs do not exist",
                [i for i in ids if i not in found_ids],
            )

        return result

    async def bulk_save(self, values: list[auth_session.AuthSession]) -> None:
        pass

    async def bulk_delete(self, ids: list[auth_session.Id]) -> None:
        pass

    async def get(self, id: auth_session.Id) -> auth_session.AuthSession:
        try:
            result_map = await self.bulk_get([id])
        except auth_session.RepositoryGetError as e:
            raise e

        return result_map[id]

    async def save(self, value: auth_session.AuthSession) -> None:
        pass

    async def delete(self, id: auth_session.Id) -> None:
        pass
