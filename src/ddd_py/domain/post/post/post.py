from .id import Id
from .content import Content

from ddd_py.domain.user.user.id import Id as UserId

class Post:
    def __init__(self, id: Id, user_id: UserId, content: Content) -> None:
        self._id = id
        self._user_id = user_id
        self._content = content

    @property
    def id(self) -> Id:
        return self._id
    
    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def content(self) -> Content:
        return self._content
    
    def replace_content(self, new_content: Content) -> None:
        self._content = new_content
