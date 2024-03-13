
from .id import Id
from .name import Name

class User():
    def __init__(self, id: Id, name: Name) -> None:
        self._id = id
        self._name = name

    @property
    def id(self) -> Id:
        return self._id
    
    @property
    def name(self) -> Name:
        return self._name
    
    def change_name(self, name: Name) -> None:
        self._name = name
    