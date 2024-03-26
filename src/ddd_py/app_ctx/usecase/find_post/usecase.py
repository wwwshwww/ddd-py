from abc import ABCMeta, abstractmethod

from ddd_py.app_ctx.common.types import Page
from ddd_py.app_ctx.domain.post import post, post_finder
from ddd_py.app_ctx.usecase.common import dto


class Usecase(metaclass=ABCMeta):
    @abstractmethod
    async def find(
        self,
        fo: post_finder.FilteringOptions,
        so: post_finder.SortingOptions,
        page: Page,
    ) -> list[dto.Post]:
        pass


class UsecaseImpl(Usecase):
    def __init__(self, pf: post_finder.Finder, pr: post.Repository):
        self.pf = pf
        self.pr = pr

    async def find(
        self,
        fo: post_finder.FilteringOptions,
        so: post_finder.SortingOptions,
        page: Page,
    ) -> list[dto.Post]:
        return []
