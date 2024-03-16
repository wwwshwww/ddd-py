import abc
from dataclasses import dataclass


class SortingType(metaclass=abc.ABCMeta):
    def __init__(self, asc: bool):
        self.asc = asc

    def is_asc(self) -> bool:
        raise self.asc


class SortingTypeId(SortingType): ...


class SortingTypeReactionPresetId(SortingType): ...


class SortingTypeReactedAt(SortingType): ...


@dataclass
class SortingOptions:
    orders: list[SortingType]
