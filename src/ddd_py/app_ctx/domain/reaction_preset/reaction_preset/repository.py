from abc import ABC, abstractmethod

from .id import Id
from .reaction_preset import ReactionPreset


class Repository(ABC):
    @abstractmethod
    def bulk_get(self, ids: list[Id]) -> dict[Id, ReactionPreset]:
        raise NotImplementedError()

    @abstractmethod
    def bulk_save(self, values: list[ReactionPreset]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def bulk_delete(self, ids: list[Id]) -> None:
        raise NotImplementedError()
