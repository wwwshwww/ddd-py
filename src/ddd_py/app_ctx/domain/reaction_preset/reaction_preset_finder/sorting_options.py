from abc import ABCMeta
from dataclasses import dataclass


@dataclass
class SortingType(metaclass=ABCMeta):
    asc: bool


@dataclass
class SortingTypeId(SortingType): ...


@dataclass
class SortingTypeContent(SortingType): ...


@dataclass
class SortingTypeCreatedAt(SortingType): ...


@dataclass
class SortingTypeReactedCount(SortingType): ...


@dataclass
class SortingOptions:
    orders: list[SortingType]
