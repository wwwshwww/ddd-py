import abc

from .id import Id
from .user import User


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def bulk_get(self, ids: list[Id]) -> list[User]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_save(self, posts: list[User]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()
