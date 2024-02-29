from .id import ID
from .content import Content

class Post:
    def __init__(self, id: ID, content: Content) -> None:
        self._id = id
        self._content = content

    @property
    def id(self) -> ID:
        return self._id

    @property
    def content(self) -> Content:
        return self._content
    
    @content.setter
    def content(self, value: Content) -> None:
        self._content = value