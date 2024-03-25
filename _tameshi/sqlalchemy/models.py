import uuid
from abc import abstractmethod
from typing import Any

from sqlalchemy import BINARY, Dialect, String, TypeDecorator
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class UUIDBinary(TypeDecorator):
    impl = BINARY(16)

    def process_bind_param(
        self, value: uuid.UUID | None, dialect: Dialect
    ) -> bytes | None:
        if value is not None:
            return value.bytes
        return None

    def process_result_value(
        self, value: bytes | None, dialect: Dialect
    ) -> uuid.UUID | None:
        if value is not None:
            return uuid.UUID(bytes=value)
        return None

    def process_literal_param(self, value, dialect):
        raise NotImplementedError("Literal binds are not supported for UUIDs")

    @property
    def python_type(self):
        return uuid.UUID


class Base(DeclarativeBase):
    @abstractmethod
    def extract_fields(self) -> dict[str, Any]:
        pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(UUIDBinary(), primary_key=True)
    google_sub: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id!r}, google_sub={self.google_sub!r}>"

    def extract_fields(self) -> dict[str, Any]:
        return {"id": self.id, "google_sub": self.google_sub}
