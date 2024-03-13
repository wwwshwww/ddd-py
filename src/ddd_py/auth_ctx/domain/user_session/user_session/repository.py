import abc
from typing import List

from .id import Id
from .user_session import UserSession

class Repository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def BulkGet(ids: List[Id]) -> List[UserSession]: 
        raise NotImplementedError()
    
    @abc.abstractmethod
    def BulkSave(posts: List[UserSession]) -> None: 
        raise NotImplementedError()
    
    @abc.abstractmethod
    def BulkDelete(ids: List[Id]) -> None: 
        raise NotImplementedError()