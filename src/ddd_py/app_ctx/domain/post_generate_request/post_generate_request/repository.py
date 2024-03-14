import abc
from typing import List

from .id import Id
from .post_generate_request import PostGenerateRequest


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def new_ids(self, num: int) -> List[Id]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_get(self, ids: List[Id]) -> List[PostGenerateRequest]:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_save(self, posts: List[PostGenerateRequest]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def bulk_delete(self, ids: List[Id]) -> None:
        raise NotImplementedError()
