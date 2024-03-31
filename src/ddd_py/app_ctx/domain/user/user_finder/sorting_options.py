from abc import ABCMeta
from dataclasses import dataclass


@dataclass
class SortingType(metaclass=ABCMeta):
    asc: bool


@dataclass
class SortingTypeName(SortingType): ...


@dataclass
class SortingTypeGetReactionNum(SortingType): ...


@dataclass
class SortingTypeGiveReactionNum(SortingType): ...


@dataclass
class SortingOptions:
    orders: list[SortingType]
