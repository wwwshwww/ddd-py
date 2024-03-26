import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from ddd_py.auth_ctx.domain.auth_session import auth_session
from ddd_py.common.adapter.mysql import types


class AuthSession(types.Base):
    __tablename__ = "auth_session"

    id: Mapped[uuid.UUID] = mapped_column(types.UUIDBinary(), primary_key=True)
    client_state: Mapped[str] = mapped_column(String(255))
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id!r}, client_state={self.client_state!r}, expires_at={self.expires_at!r}>"

    def extract_fields(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "client_state": self.client_state,
            "started_at": self.started_at,
            "expires_at": self.expires_at,
        }


def decode(dto: AuthSession) -> auth_session.AuthSession:
    return auth_session.AuthSession(
        id=auth_session.Id(dto.id),
        client_state=auth_session.ClientState(dto.client_state),
        started_at=dto.started_at,
        expires_at=dto.expires_at,
    )


def encode(aggregate: auth_session.AuthSession) -> AuthSession:
    try:
        return AuthSession(
            id=aggregate.id.value,
            client_state=aggregate.client_state.value,
            started_at=aggregate.started_at,
            expires_at=aggregate.expires_at,
        )
    except Exception as e:
        raise e
