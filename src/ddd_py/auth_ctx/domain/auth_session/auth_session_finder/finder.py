from abc import ABCMeta, abstractmethod

from ddd_py.auth_ctx.domain.auth_session import auth_session

from .filtering_options import FilteringOptions


class Finder(metaclass=ABCMeta):
    @abstractmethod
    async def find(self, fo: FilteringOptions | None = None) -> list[auth_session.Id]:
        raise NotImplementedError()
