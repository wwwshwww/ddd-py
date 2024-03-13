import abc
from typing import List
from dataclasses import dataclass

class SortingType(metaclass=abc.ABCMeta):
    def __init__(self, asc: bool):
        self.asc = asc

    def asc(self) -> bool:
        raise self.asc
    
class SortingTypeId(SortingType):...
class SortingTypeReactionNum(SortingType):...
class SortingTypeUserId(SortingType):...
class SortingTypePostTime(SortingType):...

# class SortingTypeSpecificReactionNum(SortingType):
#     def __init__(self, asc: bool, reaction_type: reaction.Type):
#         super().__init__(asc)
#         self.reaction_type = reaction_type

@dataclass
class SortingOptions:
    orders: List[SortingType]