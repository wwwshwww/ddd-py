import abc
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum, unique

from ..post.id import Id

@dataclass
class FilteringOptions:
    reaction_num_more: Optional[int] = None
    reaction_num_less: Optional[int] = None

@unique
class SortingType(Enum):
    ID_ASC = 0
    ID_DESC = 1
    REACTION_NUM_ASC = 2
    REACTION_NUM_DESC = 3
    USER_ID_ASC = 4
    USER_ID_DESC = 5

@dataclass
class SortingOptions:
    orders: List[SortingType]

class Finder(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def Find(self, filtering_options: FilteringOptions=None, sorting_options: SortingOptions=None) -> List[Id]:
        raise NotImplementedError()
