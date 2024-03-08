import abc
from typing import List

from .id import Id
from .post import Post

class Repository(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def NewIDs(num: int) -> List[Id]:
        raise NotImplementedError()

    @abc.abstractmethod
    def BulkGet(ids: List[Id]) -> List[Post]: 
        raise NotImplementedError()
    
    @abc.abstractmethod
    def BulkSave(posts: List[Post]) -> None: 
        raise NotImplementedError()
    
    @abc.abstractmethod
    def BulkDelete(ids: List[Id]) -> None: 
        raise NotImplementedError()