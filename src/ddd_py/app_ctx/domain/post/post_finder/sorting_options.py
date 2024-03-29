from abc import ABC
from dataclasses import dataclass


@dataclass
class SortingType(ABC):
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
