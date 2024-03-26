import abc
from dataclasses import dataclass


@dataclass
class SortingType(metaclass=abc.ABCMeta):
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
