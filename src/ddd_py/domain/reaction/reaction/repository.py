import abc
from typing import List

from .id import Id
from .reaction import Reaction

class Repository(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def NewIDs(num: int) -> List[Id]:
        raise NotImplementedError()

    @abc.abstractmethod
    def BulkGet(ids: List[Id]) -> List[Reaction]: 
        raise NotImplementedError()
    
    @abc.abstractmethod
    def BulkSave(posts: List[Reaction]) -> None: 
        raise NotImplementedError()
    
    @abc.abstractmethod
    def BulkDelete(ids: List[Id]) -> None: 
        raise NotImplementedError()