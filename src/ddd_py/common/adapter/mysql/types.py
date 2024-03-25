import uuid
from abc import abstractmethod
from typing import Any, TypeVar

from sqlalchemy import BINARY, Dialect, TypeDecorator
from sqlalchemy.orm import (
    DeclarativeBase,
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


RDBModel = TypeVar("RDBModel", bound=Base)
