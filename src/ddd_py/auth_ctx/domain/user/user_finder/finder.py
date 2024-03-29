from abc import ABC, abstractmethod

from ddd_py.auth_ctx.domain.user import user

from .filtering_options import FilteringOptions


class Finder(ABC):
    @abstractmethod
    async def find(
        self, filtering_options: FilteringOptions | None = None
    ) -> list[user.Id]:
        raise NotImplementedError()
