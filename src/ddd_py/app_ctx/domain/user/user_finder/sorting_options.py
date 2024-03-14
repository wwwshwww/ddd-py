import abc
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


class SortingType(metaclass=abc.ABCMeta):
    def __init__(self, asc: bool):
        self.asc = asc

    def is_asc(self) -> bool:
        raise self.asc


class SortingTypeId(SortingType): ...


class SortingTypeName(SortingType): ...


class SortingTypeGetReactionNum(SortingType):
    def __init__(
        self,
        asc: bool,
        start_range_incl: Optional[datetime] = None,
        end_range_excl: Optional[datetime] = None,
    ) -> None:
        super().__init__(asc)
        self.start_range_incl = start_range_incl
        self.end_range_excl = end_range_excl


class SortingTypeGiveReactionNum(SortingType):
    def __init__(
        self,
        asc: bool,
        start_range_incl: Optional[datetime] = None,
        end_range_excl: Optional[datetime] = None,
    ) -> None:
        super().__init__(asc)
        self.start_range_incl = start_range_incl
        self.end_range_excl = end_range_excl


@dataclass
class SortingOptions:
    orders: List[SortingType]
