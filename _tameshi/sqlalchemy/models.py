from sqlalchemy import LargeBinary, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[bytes] = mapped_column(LargeBinary(16), primary_key=True)
    google_sub: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id!r}, google_sub={self.google_sub!r}>"
