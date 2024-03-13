import abc
from typing import List

from .id import Id
from .user import User

class Repository(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def NewIDs(num: int) -> List[Id]:
        raise NotImplementedError()

    @abc.abstractmethod
    def BulkGet(ids: List[Id]) -> List[User]: 
        raise NotImplementedError()
    
    @abc.abstractmethod
    def BulkSave(posts: List[User]) -> None: 
        raise NotImplementedError()
    
    @abc.abstractmethod
    def BulkDelete(ids: List[Id]) -> None: 
        raise NotImplementedError()