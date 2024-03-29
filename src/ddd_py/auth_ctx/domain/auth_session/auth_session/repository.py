from abc import ABC, abstractmethod

from .auth_session import AuthSession
from .id import Id


class Repository(ABC):
    @abstractmethod
    async def bulk_get(self, ids: list[Id]) -> dict[Id, AuthSession]:
        raise NotImplementedError()

    @abstractmethod
    async def get(self, id: Id) -> AuthSession:
        raise NotImplementedError()

    @abstractmethod
    async def bulk_save(self, values: list[AuthSession]) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def save(self, value: AuthSession) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: Id) -> None:
        raise NotImplementedError()
