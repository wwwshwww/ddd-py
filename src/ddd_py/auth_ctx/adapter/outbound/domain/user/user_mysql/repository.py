from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ddd_py.auth_ctx.adapter.outbound.domain.user.user_mysql.models import (
    User,
    decode,
    encode,
)
from ddd_py.auth_ctx.domain.user import user
from ddd_py.common.adapter.mysql.utils import simple_upsert_stmt


class Repository(user.Repository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def bulk_get(self, ids: list[user.Id]) -> dict[user.Id, user.User]:
        if len(ids) == 0:
            return {}

        try:
            query = select(User).where(User.id.in_([i.value for i in ids]))
            rows = await self.db.scalars(query)
            result = {user.Id(row.id): decode(row) for row in rows}

            if len(result) != len(ids):
                found_ids = [user.Id(row.id) for row in rows]
                raise user.RepositoryGetError(
                    "one or more specified IDs do not exist",
                    [i for i in ids if i not in found_ids],
                )
        except user.RepositoryGetError as e:
            raise e
        except Exception as e:
            raise user.RepositoryGetError("failed to get", []) from e

        return result

    async def bulk_save(self, values: list[user.User]) -> None:
        if len(values) == 0:
            return
        try:
            data = [encode(value) for value in values]
            command = simple_upsert_stmt(data)
            await self.db.execute(command)
        except Exception as e:
            raise user.RepositorySaveError("failed to save") from e
        return

    async def bulk_delete(self, ids: list[user.Id]) -> None:
        if len(ids) == 0:
            return
        try:
            command = delete(User).where(User.id.in_([i.value for i in ids]))
            await self.db.execute(command)
        except Exception as e:
            raise user.RepositoryDeleteError("failed to delete") from e
        return

    async def get(self, id: user.Id) -> user.User:
        result_map = await self.bulk_get([id])
        return result_map[id]

    async def save(self, value: user.User) -> None:
        await self.bulk_save([value])

    async def delete(self, id: user.Id) -> None:
        await self.bulk_delete([id])
