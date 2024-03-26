import abc

from ddd_py.app_ctx.domain.reaction import reaction

from .filtering_options import FilteringOptions
from .sorting_options import SortingOptions


class Finder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def find(
        self,
        filtering_options: FilteringOptions | None = None,
        sorting_options: SortingOptions | None = None,
    ) -> list[reaction.Id]:
        raise NotImplementedError()
