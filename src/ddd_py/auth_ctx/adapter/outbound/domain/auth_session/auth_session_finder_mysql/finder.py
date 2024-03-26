from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ddd_py.auth_ctx.adapter.outbound.domain.auth_session.auth_session_mysql.models import (
    AuthSession,
)
from ddd_py.auth_ctx.domain.auth_session import auth_session_finder
from ddd_py.auth_ctx.domain.auth_session.auth_session.auth_session import Id


class Finder(auth_session_finder.Finder):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find(
        self,
        fo: auth_session_finder.FilteringOptions = None,
    ) -> list[Id]:
        try:
            q = select(AuthSession.id).select_from(AuthSession)
            if fo:
                if (fo.id_in is not None) and len(fo.id_in) > 0:
                    q = q.where(AuthSession.id.in_([i.value for i in fo.id_in]))

            rows = await self.db.scalars(q)

        except Exception as e:
            raise auth_session_finder.FinderError("failed to find") from e

        return [Id(i) for i in rows]
