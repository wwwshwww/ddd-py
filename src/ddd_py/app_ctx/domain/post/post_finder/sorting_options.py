import abc
from dataclasses import dataclass


@dataclass
class SortingType(metaclass=abc.ABCMeta):
    asc: bool


@dataclass
class SortingTypeId(SortingType): ...


@dataclass
class SortingTypeReactionNum(SortingType): ...


@dataclass
class SortingTypeUserId(SortingType): ...


@dataclass
class SortingTypeCreatedAt(SortingType): ...


# @dataclass
# class SortingTypeSpecificReactionNum(SortingType):
#     reaction_type: str


@dataclass
class SortingOptions:
    orders: list[SortingType]
