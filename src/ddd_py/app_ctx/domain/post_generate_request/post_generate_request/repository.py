from abc import ABC, abstractmethod

from .id import Id
from .post_generate_request import PostGenerateRequest


class Repository(ABC):
    @abstractmethod
    def bulk_get(self, ids: list[Id]) -> dict[Id, PostGenerateRequest]:
        raise NotImplementedError()

    @abstractmethod
    def bulk_save(self, values: list[PostGenerateRequest]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()
