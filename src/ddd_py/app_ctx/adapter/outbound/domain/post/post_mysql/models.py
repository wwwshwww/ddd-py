import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

from ddd_py.app_ctx.domain.post.post import post
from ddd_py.app_ctx.domain.user import user
from ddd_py.common.adapter.mysql import types


class Post(types.Base):
    __tablename__ = "post"

    id: Mapped[uuid.UUID] = mapped_column(types.UUIDBinary(), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(types.UUIDBinary(), nullable=False)
    content: Mapped[str] = mapped_column(String(1024), nullable=False)
    posted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def __repr__(self) -> str:
        return f"<Post(id={self.id!r}, user_id={self.user_id!r}, content={self.content!r}, posted_at={self.posted_at!r}>"

    def extract_fields(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "posted_at": self.posted_at,
        }


def decode(dto: Post) -> post.Post:
    return post.Post(
        id=post.Id(dto.id),
        user_id=user.Id(dto.user_id),
        content=post.Content(dto.content),
        posted_at=dto.posted_at,
    )


def encode(aggregate: post.Post) -> Post:
    return Post(
        id=aggregate.id.value,
        user_id=aggregate.user_id.value,
        content=aggregate.content.value,
        posted_at=aggregate.posted_at,
    )


class PostUserVersion(DeclarativeBase):
    __tablename__ = "post_user_version"

    post_id: Mapped[uuid.UUID] = mapped_column(types.UUIDBinary(), nullable=False)
    user_version_id: Mapped[uuid.UUID] = mapped_column(
        types.UUIDBinary(), nullable=False
    )
