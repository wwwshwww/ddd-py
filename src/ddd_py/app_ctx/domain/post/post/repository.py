import abc

from .id import Id
from .post import Post


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def bulk_get(self, ids: list[Id]) -> dict[Id, Post]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def bulk_save(self, values: list[Post]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()
