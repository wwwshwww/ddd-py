from abc import ABC, abstractmethod

from .id import Id
from .user_session import UserSession


class Repository(ABC):
    @abstractmethod
    def bulk_get(self, ids: list[Id]) -> dict[Id, UserSession]:
        raise NotImplementedError()

    @abstractmethod
    def get(self, id: Id) -> UserSession:
        raise NotImplementedError()

    @abstractmethod
    def bulk_save(self, values: list[UserSession]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def save(self, value: UserSession) -> None:
        raise NotImplementedError()

    @abstractmethod
    def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: Id) -> None:
        raise NotImplementedError()
