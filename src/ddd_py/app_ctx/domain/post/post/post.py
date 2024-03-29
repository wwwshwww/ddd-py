from datetime import datetime

from ddd_py.app_ctx.domain.user import user

from .content import Content
from .id import Id


class Post:
    def __init__(
        self, id: Id, user_id: user.Id, content: Content, created_at: datetime
    ) -> None:
        self._id = id
        self._user_id = user_id
        self._content = content
        self._created_at = created_at

    @property
    def id(self) -> Id:
        return self._id

    @property
    def user_id(self) -> user.Id:
        return self._user_id

    @property
    def content(self) -> Content:
        return self._content

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def replace_content(self, new_content: Content) -> None:
        self._content = new_content
