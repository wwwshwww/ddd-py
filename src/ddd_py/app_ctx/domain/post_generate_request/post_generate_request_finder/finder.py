import abc

from ddd_py.app_ctx.domain.post_generate_request import post_generate_request

from .filtering_options import FilteringOptions
from .sorting_options import SortingOptions


class Finder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find(
        self,
        filtering_options: FilteringOptions = None,
        sorting_options: SortingOptions = None,
    ) -> list[post_generate_request.Id]:
        raise NotImplementedError()
