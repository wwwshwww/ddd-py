import abc
from typing import List

from .auth_session import AuthSession
from .id import Id


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def bulk_get(self, ids: List[Id]) -> List[AuthSession]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_save(self, posts: List[AuthSession]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_delete(self, ids: List[Id]) -> None:
        raise NotImplementedError()
