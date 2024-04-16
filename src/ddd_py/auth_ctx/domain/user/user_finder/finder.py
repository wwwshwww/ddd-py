from abc import ABCMeta, abstractmethod

from ddd_py.auth_ctx.domain.user import user

from .filtering_options import FilteringOptions


class Finder(metaclass=ABCMeta):
    @abstractmethod
    async def find(self, fo: FilteringOptions | None = None) -> list[user.Id]:
        raise NotImplementedError()
