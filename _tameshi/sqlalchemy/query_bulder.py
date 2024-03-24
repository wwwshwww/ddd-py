import uuid

from sqlalchemy import LargeBinary, String, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
)

user = "example"
password = "pass"
host = "localhost"
port = 3306
database = "my-db"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[bytes] = mapped_column(LargeBinary(16), primary_key=True)
    google_sub: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id!r}, google_sub={self.google_sub!r}>"


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
