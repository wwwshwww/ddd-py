from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ddd_py.auth_ctx.adapter.outbound.domain.user.user_mysql.models import User
from ddd_py.auth_ctx.domain.user import user, user_finder


class Finder(user_finder.Finder):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find(self, fo: user_finder.FilteringOptions | None = None):
        try:
            q = select(User.id).select_from(user.User)
            if fo:
                if fo.provider_subject_google is not None:
                    q = q.where(User.google_sub == fo.provider_subject_google)

            rows = await self.db.scalars(q)

        except Exception as e:
            raise user_finder.FinderError("failed to find") from e

        return [user.Id(i) for i in rows]
