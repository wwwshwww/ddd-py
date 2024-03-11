import abc
from ast import List

from .filtering_options import FilteringOptions
from .sorting_options import SortingOptions

from ddd_py.domain.reaction_preset import reaction_preset

class Finder(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def Find(self, filtering_options: FilteringOptions=None, sorting_options: SortingOptions=None) -> List[reaction_preset.Id]:
        raise NotImplementedError()