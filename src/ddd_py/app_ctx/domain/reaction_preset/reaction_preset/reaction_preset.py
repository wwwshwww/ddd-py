from datetime import datetime
from .error import DomainError

from .id import Id
from .content import Content

from ddd_py.app_ctx.domain.user import user

class ReactionPreset():
    def __init__(self, id: Id, content: Content, created_by_user_id: user.Id, created_at: datetime) -> None:
        self._id = id
        self._content = content
        self._created_by_user_id = created_by_user_id
        self._created_at = created_at

    @property
    def id(self) -> Id:
        return self._id
    
    @property
    def content(self) -> Content:
        return self._content
    
    @property
    def created_by_user_id(self) -> user.Id:
        return self._created_by_user_id
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    