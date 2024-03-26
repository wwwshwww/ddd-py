import abc
from dataclasses import dataclass


@dataclass
class SortingType(metaclass=abc.ABCMeta):
    asc: bool


@dataclass
class SortingTypeId(SortingType): ...


@dataclass
class SortingOptions:
    orders: list[SortingType]
