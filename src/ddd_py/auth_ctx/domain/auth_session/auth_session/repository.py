import abc

from .auth_session import AuthSession
from .id import Id


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def bulk_get(self, ids: list[Id]) -> dict[Id, AuthSession]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get(self, id: Id) -> AuthSession:
        raise NotImplementedError()

    @abc.abstractmethod
    async def bulk_save(self, values: list[AuthSession]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def save(self, value: AuthSession) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, id: Id) -> None:
        raise NotImplementedError()
