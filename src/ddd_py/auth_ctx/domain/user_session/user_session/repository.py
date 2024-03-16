import abc

from .id import Id
from .user_session import UserSession


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def bulk_get(self, ids: list[Id]) -> list[UserSession]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_save(self, posts: list[UserSession]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()
