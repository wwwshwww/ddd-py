import copy
import uuid
from typing import TypeVar

from conf import database, host, password, user
from models import Base, User
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import Insert, insert
from sqlalchemy.orm import Session

RDBModel = TypeVar("RDBModel", bound=Base)


def simple_upsert_stmt(
    values: list[RDBModel],
    ignore_keys: list[str] = None,
) -> Insert:
    if len(values) == 0:
        raise ValueError("No values provided")

    if ignore_keys is None:
        ignore_keys = ["id"]

    fields = [k for k in values[0].extract_fields().keys() if k not in ignore_keys]
    stmt = insert(values[0].__class__).values([u.extract_fields() for u in values])

    return stmt.on_duplicate_key_update(**{f: stmt.inserted[f] for f in fields})


if __name__ == "__main__":
    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{database}",
        echo=True,
    )

    with Session(engine) as session:
        sub = uuid.uuid4()

        us1 = [
            User(id=uuid.uuid4(), google_sub=f"test_{str(sub)[:5]}_{i}")
            for i in range(3)
        ]
        us2 = list(
            map(
                lambda u: User(id=u.id, google_sub=u.google_sub + "_ex"),
                copy.deepcopy(us1),
            )
        )

        stmt1 = insert(User).values([u.extract_fields() for u in us1])
        session.execute(stmt1)

        # stmt2 = insert(User).values([u.extract_fields() for u in us2])
        # upd = stmt2.on_duplicate_key_update(
        #     google_sub=stmt2.inserted["google_sub"],
        # )
        upd = simple_upsert_stmt(us2)
        session.execute(upd)

        print("done")
        session.commit()

    engine.dispose()
