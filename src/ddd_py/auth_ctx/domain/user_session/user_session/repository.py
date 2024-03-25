import abc

from .id import Id
from .user_session import UserSession


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def bulk_get(self, ids: list[Id]) -> dict[Id, UserSession]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get(self, id: Id) -> UserSession:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_save(self, values: list[UserSession]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, value: UserSession) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, id: Id) -> None:
        raise NotImplementedError()
