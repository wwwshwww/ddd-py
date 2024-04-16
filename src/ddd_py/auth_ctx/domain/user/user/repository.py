from abc import ABCMeta, abstractmethod

from .id import Id
from .user import User


class Repository(metaclass=ABCMeta):
    @abstractmethod
    async def bulk_get(self, ids: list[Id]) -> dict[Id, User]:
        raise NotImplementedError()

    @abstractmethod
    async def get(self, id: Id) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def bulk_save(self, values: list[User]) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def save(self, value: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: Id) -> None:
        raise NotImplementedError()
