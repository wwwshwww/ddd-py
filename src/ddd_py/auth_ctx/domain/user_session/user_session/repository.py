import abc
from typing import List

from .id import Id
from .user_session import UserSession


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def bulk_get(self, ids: List[Id]) -> List[UserSession]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_save(self, posts: List[UserSession]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_delete(self, ids: List[Id]) -> None:
        raise NotImplementedError()
