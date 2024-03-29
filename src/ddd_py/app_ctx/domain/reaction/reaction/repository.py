from abc import ABC, abstractmethod

from .id import Id
from .reaction import Reaction


class Repository(ABC):
    @abstractmethod
    def bulk_get(self, ids: list[Id]) -> dict[Id, Reaction]:
        raise NotImplementedError()

    @abstractmethod
    def bulk_save(self, values: list[Reaction]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()
