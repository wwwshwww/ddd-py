from abc import ABC
from dataclasses import dataclass


@dataclass
class SortingType(ABC):
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
