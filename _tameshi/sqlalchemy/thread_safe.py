import asyncio
import contextvars
import copy
import uuid

import conf
import ulid
from models import User
from sqlalchemy import case, func, insert, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

# * https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html

ctx = contextvars.ContextVar("ctx", default="default")


class Repo:
    count: int = 0

    @classmethod
    def inc(cls) -> None:
        cls.count += 1

    def __init__(self, session: AsyncSession) -> None:
        self.identifier = copy.deepcopy(self.count)
        self.session = session
        print(f"[{self.identifier}]: called")
        self.inc()

    async def do(self) -> None:
        print(f"[{self.identifier}]: started")
        print(f"[{self.identifier}]: ctx: {ctx.get()}")
        await self.read()
        await self.write()
        print(f"[{self.identifier}]: done")

    async def read(self) -> None:
        print(f"[{self.identifier}]: read started")
        # * SELECT count(user.id) AS id_count, left(user.google_sub, %s) AS prefix, count(CASE WHEN (user.google_sub LIKE %s) THEN %s END) AS count_1 FROM user GROUP BY prefix
        count_query = (
            select(
                # User.google_sub,
                func.count(User.id).label("id_count"),  # pylint: disable=E1102
                func.left(User.google_sub, 1).label("prefix"),
                # * prefixが自身のidentifierと一致する場合は数え上げる
                func.count(  # pylint: disable=E1102
                    case(
                        (User.google_sub.like(f"{self.identifier}-%"), 1),
                        else_=None,
                    )
                ),
            )
            .select_from(
                User,
            )
            .group_by(
                # User.google_sub,
                "prefix"
            )
        )
        count_result = await self.session.execute(count_query)
        print(f"[{self.identifier}]: count read: {count_result.all()}")

        fetch_query = select(User)
        result = await self.session.scalars(fetch_query)
        for r in result:
            print(f"[{self.identifier}]: read elements: {r}")
        print(f"[{self.identifier}]: read done")

    async def write(self) -> None:
        print(f"[{self.identifier}]: write start")
        await self.session.execute(
            insert(User),
            [
                # User(id=ulid.new(), google_sub=f"user:{self.identifier}"),
                {
                    "id": ulid.new(),
                    "google_sub": f"{self.identifier}-{str(uuid.uuid4())}",
                }
            ],
        )
        print(f"[{self.identifier}]: write done")


async def handle(
    async_scoped_session_factory: async_scoped_session[AsyncSession],
) -> None:
    async with async_scoped_session_factory() as session:
        ctx.set(str(uuid.uuid4()))
        async with session.begin():
            r = Repo(session)
            await r.do()


async def main() -> None:
    engine = create_async_engine(
        f"mysql+aiomysql://{conf.user}:{conf.password}@{conf.host}/{conf.database}",
        echo=True,
    )

    async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async_scoped_session_factory = async_scoped_session(
        async_session_factory,
        scopefunc=asyncio.current_task,
    )

    req1 = asyncio.create_task(handle(async_scoped_session_factory))
    req2 = asyncio.create_task(handle(async_scoped_session_factory))
    await asyncio.gather(req1, req2)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
