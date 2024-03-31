from abc import ABCMeta, abstractmethod

from ddd_py.app_ctx.domain.reaction_preset import reaction_preset

from .filtering_options import FilteringOptions
from .sorting_options import SortingOptions


class Finder(metaclass=ABCMeta):
    @abstractmethod
    async def find(
        self,
        filtering_options: FilteringOptions | None = None,
        sorting_options: SortingOptions | None = None,
    ) -> list[reaction_preset.Id]:
        raise NotImplementedError()
