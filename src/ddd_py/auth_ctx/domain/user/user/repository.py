from abc import ABCMeta, abstractmethod

from .id import Id
from .user import User


class Repository(metaclass=ABCMeta):
    @abstractmethod
    def bulk_get(self, ids: list[Id]) -> dict[Id, User]:
        raise NotImplementedError()

    @abstractmethod
    def get(self, id: Id) -> User:
        raise NotImplementedError()

    @abstractmethod
    def bulk_save(self, values: list[User]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def save(self, value: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: Id) -> None:
        raise NotImplementedError()
