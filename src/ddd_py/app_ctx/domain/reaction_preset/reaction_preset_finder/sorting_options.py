from abc import ABC
from dataclasses import dataclass


@dataclass
class SortingType(ABC):
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
