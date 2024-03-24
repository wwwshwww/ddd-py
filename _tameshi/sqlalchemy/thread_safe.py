import asyncio
import copy

import conf
import ulid
from models import User
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session

# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html


class Repo:
    count: int = 0

    @classmethod
    def inc(cls) -> None:
        cls.count += 1

    def __init__(self, session: Session) -> None:
        print(f"called: {self.count}")
        self.identifier = copy.deepcopy(self.count)
        self.session = session
        self.inc()

    async def do(self) -> None:
        print(f"[{self.identifier}]: start")
        await self.read()
        await self.write()
        print(f"[{self.identifier}]: done")

    async def read(self) -> None:
        print(f"[{self.identifier}]: read start")
        stmt = select(User)
        result = await self.session.scalars(stmt)
        for r in result:
            print(f"[{self.identifier}]: {r}")
        print(f"[{self.identifier}]: read done")

    async def write(self) -> None:
        print(f"[{self.identifier}]: write start")
        await self.session.execute(
            insert(User),
            [
                # User(id=ulid.new().bytes, google_sub=f"user:{self.identifier}"),
                {"id": ulid.new().bytes, "google_sub": f"user:{self.identifier}"}
            ],
        )
        print(f"[{self.identifier}]: write done")


async def handle(async_session_factory: async_sessionmaker[AsyncSession]) -> None:
    async with async_session_factory() as session:
        async with session.begin():
            r = Repo(session)
            await r.do()


async def main() -> None:
    engine = create_async_engine(
        f"mysql+aiomysql://{conf.user}:{conf.password}@{conf.host}/{conf.database}",
        echo=True,
    )

    async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

    req1 = asyncio.create_task(handle(async_session_factory))
    req2 = asyncio.create_task(handle(async_session_factory))
    await asyncio.gather(req1, req2)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
