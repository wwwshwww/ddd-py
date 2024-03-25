import abc

from .id import Id
from .reaction import Reaction


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def bulk_get(self, ids: list[Id]) -> dict[Id, Reaction]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_save(self, values: list[Reaction]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()
