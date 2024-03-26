import abc
from dataclasses import dataclass


@dataclass
class SortingType(metaclass=abc.ABCMeta):
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
