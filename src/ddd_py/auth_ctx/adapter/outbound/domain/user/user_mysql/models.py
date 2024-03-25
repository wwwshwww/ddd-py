from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from ddd_py.common.adapter.mysql import my_base


class User(my_base.Base):
    __tablename__ = "user"

    id: Mapped[bytes] = mapped_column(my_base.UUIDBinary(length=16), primary_key=True)
    google_sub: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id!r}, google_sub={self.google_sub!r}>"
