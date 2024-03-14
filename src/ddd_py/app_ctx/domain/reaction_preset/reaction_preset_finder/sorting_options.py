import abc
from dataclasses import dataclass
from typing import List


class SortingType(metaclass=abc.ABCMeta):
    def __init__(self, asc: bool):
        self.asc = asc

    def is_asc(self) -> bool:
        raise self.asc


class SortingTypeId(SortingType): ...


class SortingTypeContent(SortingType): ...


class SortingTypeCreatedAt(SortingType): ...


class SortingTypeReactedCount(SortingType): ...


@dataclass
class SortingOptions:
    orders: List[SortingType]
