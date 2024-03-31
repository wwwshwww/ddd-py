from abc import ABCMeta
from dataclasses import dataclass


@dataclass
class SortingType(metaclass=ABCMeta):
    asc: bool


@dataclass
class SortingTypeId(SortingType): ...


@dataclass
class SortingTypeReactionPresetId(SortingType): ...


@dataclass
class SortingTypeReactedAt(SortingType): ...


@dataclass
class SortingOptions:
    orders: list[SortingType]
