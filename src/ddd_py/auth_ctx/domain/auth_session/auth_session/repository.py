import abc

from .auth_session import AuthSession
from .id import Id


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def bulk_get(self, ids: list[Id]) -> list[AuthSession]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_save(self, posts: list[AuthSession]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()
