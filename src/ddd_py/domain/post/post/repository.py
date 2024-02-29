import abc
from typing import List

from .id import ID
from .post import Post

class Repository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def BulkGet(ids: List[ID]) -> List[Post]: 
        raise NotImplementedError()
    
    @abc.abstractmethod
    def BulkSave(posts: List[Post]) -> None: 
        raise NotImplementedError()
    
    @abc.abstractmethod
    def BulkDelete(ids: List[ID]) -> None: 
        raise NotImplementedError()