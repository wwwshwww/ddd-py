import uuid
from typing import Any

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from ddd_py.auth_ctx.domain.user import user
from ddd_py.common.adapter.mysql import types


class User(types.Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(types.UUIDBinary(), primary_key=True)
    google_sub: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id!r}, google_sub={self.google_sub!r}>"

    def extract_fields(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "google_sub": self.google_sub,
        }


def decode(dto: User) -> user.User:
    return user.User(
        id=user.Id(dto.id),
        google_profile=user.GoogleProfile(user.ProviderSubject(dto.google_sub)),
    )


def encode(aggregate: user.User) -> User:
    return User(
        id=aggregate.id.value,
        google_sub=aggregate.google_profile.provider_subject.value,
    )
