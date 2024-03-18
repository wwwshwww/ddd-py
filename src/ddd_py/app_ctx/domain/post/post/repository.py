import abc

from .id import Id
from .post import Post


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def new_ids(self, num: int) -> list[Id]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_get(self, ids: list[Id]) -> dict[Id, Post]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_save(self, posts: list[Post]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()
