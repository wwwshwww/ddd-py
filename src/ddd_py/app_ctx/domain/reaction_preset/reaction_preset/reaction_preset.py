from datetime import datetime

from ddd_py.app_ctx.domain.user import user

from .content import Content
from .id import Id


class ReactionPreset:
    def __init__(
        self,
        id: Id,
        content: Content,
        creator_id: user.Id,
        created_at: datetime,
    ) -> None:
        self._id = id
        self._content = content
        self._creator_id = creator_id
        self._created_at = created_at

    @property
    def id(self) -> Id:
        return self._id

    @property
    def content(self) -> Content:
        return self._content

    @property
    def creator_id(self) -> user.Id:
        return self._creator_id

    @property
    def created_at(self) -> datetime:
        return self._created_at
