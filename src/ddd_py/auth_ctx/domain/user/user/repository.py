import abc

from .id import Id
from .user import User


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def bulk_get(self, ids: list[Id]) -> dict[Id, User]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get(self, id: Id) -> User:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_save(self, values: list[User]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, value: User) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def delete(self, id: Id) -> None:
        raise NotImplementedError()
