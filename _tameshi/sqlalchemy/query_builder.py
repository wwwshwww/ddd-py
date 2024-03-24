import uuid

from conf import database, host, password, user
from models import User
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

if __name__ == "__main__":
    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{database}",
        echo=True,
    )

    with Session(engine) as session:
        PARAM = "asd"
        stmt = select(User).where(User.google_sub.like(f"%{PARAM}%"))

        result = session.scalars(stmt)

        for r in result:
            print(uuid.UUID(bytes=r.id))
            print(r.google_sub)

        print("done")
        session.commit()

    engine.dispose()
