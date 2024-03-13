import abc
from typing import List

from .id import Id
from .post_generate_request import PostGenerateRequest

class Repository(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def NewIDs(num: int) -> List[Id]:
        raise NotImplementedError()

    @abc.abstractmethod
    def BulkGet(ids: List[Id]) -> List[PostGenerateRequest]: 
        raise NotImplementedError()
    
    @abc.abstractmethod
    def BulkSave(posts: List[PostGenerateRequest]) -> None: 
        raise NotImplementedError()
    
    @abc.abstractmethod
    def BulkDelete(ids: List[Id]) -> None: 
        raise NotImplementedError()