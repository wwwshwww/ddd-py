from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ddd_py.auth_ctx.domain.auth_session import auth_session
from ddd_py.common.adapter.mysql.utils import simple_upsert_stmt

from .models import AuthSession, decode, encode


class Repository(auth_session.Repository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def bulk_get(
        self, ids: list[auth_session.Id]
    ) -> dict[auth_session.Id, auth_session.AuthSession]:
        if len(ids) == 0:
            return {}

        try:
            query = select(AuthSession).where(
                AuthSession.id.in_([i.value for i in ids])
            )
            rows = await self.db.scalars(query)
            result = {auth_session.Id(row.id): decode(row) for row in rows}

            if len(result) != len(ids):
                found_ids = [auth_session.Id(row.id) for row in rows]
                raise auth_session.RepositoryGetError(
                    "one or more specified IDs do not exist",
                    [i for i in ids if i not in found_ids],
                )
        except auth_session.RepositoryGetError as e:
            raise e
        except Exception as e:
            raise auth_session.RepositoryGetError("failed to get", ids) from e

        return result

    async def bulk_save(self, values: list[auth_session.AuthSession]) -> None:
        if len(values) == 0:
            return
        try:
            data = [encode(value) for value in values]
            command = simple_upsert_stmt(data)
            await self.db.execute(command)
        except Exception as e:
            raise auth_session.RepositorySaveError("failed to save") from e

        return

    async def bulk_delete(self, ids: list[auth_session.Id]) -> None:
        if len(ids) == 0:
            return

        try:
            command = delete(AuthSession).where(
                AuthSession.id.in_([i.value for i in ids])
            )
            await self.db.execute(command)

        except Exception as e:
            raise auth_session.RepositoryDeleteError("failed to delete") from e

        return

    async def get(self, id: auth_session.Id) -> auth_session.AuthSession:
        try:
            result_map = await self.bulk_get([id])
        except auth_session.RepositoryGetError as e:
            raise e

        return result_map[id]

    async def save(self, value: auth_session.AuthSession) -> None:
        try:
            await self.bulk_save([value])
        except auth_session.RepositorySaveError as e:
            raise e

    async def delete(self, id: auth_session.Id) -> None:
        try:
            await self.bulk_delete([id])
        except auth_session.RepositoryDeleteError as e:
            raise e
