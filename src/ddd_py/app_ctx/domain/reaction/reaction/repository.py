import abc
from typing import List

from .id import Id
from .reaction import Reaction


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def new_ids(self, num: int) -> List[Id]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_get(self, ids: List[Id]) -> List[Reaction]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_save(self, posts: List[Reaction]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_delete(self, ids: List[Id]) -> None:
        raise NotImplementedError()
