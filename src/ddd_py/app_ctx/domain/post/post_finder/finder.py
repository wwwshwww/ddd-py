from abc import ABC, abstractmethod

from ddd_py.app_ctx.domain.post import post

from .filtering_options import FilteringOptions
from .sorting_options import SortingOptions


class Finder(ABC):
    @abstractmethod
    async def find(
        self,
        filtering_options: FilteringOptions | None = None,
        sorting_options: SortingOptions | None = None,
    ) -> list[post.Id]:
        raise NotImplementedError()
