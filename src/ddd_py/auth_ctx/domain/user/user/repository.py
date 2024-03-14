import abc
from typing import List

from .id import Id
from .user import User


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def new_ids(self, num: int) -> List[Id]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_get(self, ids: List[Id]) -> List[User]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_save(self, posts: List[User]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_delete(self, ids: List[Id]) -> None:
        raise NotImplementedError()
