import abc
from typing import List

from .id import Id
from .auth_session import AuthSession

class Repository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def BulkGet(ids: List[Id]) -> List[AuthSession]: 
        raise NotImplementedError()
    
    @abc.abstractmethod
    def BulkSave(posts: List[AuthSession]) -> None: 
        raise NotImplementedError()
    
    @abc.abstractmethod
    def BulkDelete(ids: List[Id]) -> None: 
        raise NotImplementedError()