from .id import Id
from .content import Content

from ddd_py.app_ctx.domain.user import user

class Post:
    def __init__(self, id: Id, user_id: user.Id, content: Content) -> None:
        self._id = id
        self._user_id = user_id
        self._content = content

    @property
    def id(self) -> Id:
        return self._id
    
    @property
    def user_id(self) -> user.Id:
        return self._user_id

    @property
    def content(self) -> Content:
        return self._content
    
    def replace_content(self, new_content: Content) -> None:
        self._content = new_content
