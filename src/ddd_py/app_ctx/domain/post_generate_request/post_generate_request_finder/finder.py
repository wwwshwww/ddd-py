import abc
from ast import List

from .filtering_options import FilteringOptions
from .sorting_options import SortingOptions

from ddd_py.app_ctx.domain.post_generate_request import post_generate_request

class Finder(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def Find(self, filtering_options: FilteringOptions=None, sorting_options: SortingOptions=None) -> List[post_generate_request.Id]:
        raise NotImplementedError()
