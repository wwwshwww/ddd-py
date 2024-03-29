from abc import ABC, abstractmethod

from .id import Id
from .post import Post


class Repository(ABC):
    @abstractmethod
    async def bulk_get(self, ids: list[Id]) -> dict[Id, Post]:
        raise NotImplementedError()

    @abstractmethod
    async def bulk_save(self, values: list[Post]) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()
