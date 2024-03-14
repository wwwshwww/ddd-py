import abc
from typing import List

from .id import Id
from .post import Post


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def new_ids(self, num: int) -> List[Id]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_get(self, ids: List[Id]) -> List[Post]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_save(self, posts: List[Post]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_delete(self, ids: List[Id]) -> None:
        raise NotImplementedError()
