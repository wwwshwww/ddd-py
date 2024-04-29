from fastapi.background import P
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ddd_py.app_ctx.domain.post import post

from .models import Post, decode, encode


class RepositoryMysql(post.Repository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def bulk_get(self, ids: list[post.Id]) -> dict[post.Id, post.Post]:
        if len(ids) == 0:
            return {}

        try:
            query = select(Post).where(Post.id.in_([i.value for i in ids]))
            rows = await self.db.scalars(query)
            result = {post.Id(row.id): decode(row) for row in rows}

            if len(result) != len(ids):
                found_ids = [post.Id(row.id) for row in rows]
                raise post.RepositoryGetError(
                    "one or more specified IDs do not exist",
                    [i for i in ids if i not in found_ids],
                )
        except post.RepositoryGetError as e:
            raise e
        except Exception as e:
            raise post.RepositoryGetError("failed to get", []) from e

        return result
