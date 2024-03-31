from abc import ABCMeta, abstractmethod

from ddd_py.auth_ctx.domain.user_session import user_session

from .filtering_options import FilteringOptions


class Finder(metaclass=ABCMeta):
    @abstractmethod
    async def find(
        self, filtering_options: FilteringOptions | None = None
    ) -> list[user_session.Id]:
        raise NotImplementedError()
