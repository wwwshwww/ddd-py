from abc import ABCMeta, abstractmethod

from ddd_py.app_ctx.common.context import ctx_requested_user_id
from ddd_py.app_ctx.common.types import Page
from ddd_py.app_ctx.domain.post import post, post_finder
from ddd_py.app_ctx.usecase.common import output_dto


class Usecase(metaclass=ABCMeta):
    @abstractmethod
    async def find(
        self,
        fo: post_finder.FilteringOptions,
        so: post_finder.SortingOptions,
        page: Page,
    ) -> list[output_dto.Post]:
        pass


# TODO:
class UsecaseImpl(Usecase):
    def __init__(self, pf: post_finder.Finder, pr: post.Repository):
        self.pf = pf
        self.pr = pr

    async def find(
        self,
        fo: post_finder.FilteringOptions,
        so: post_finder.SortingOptions,
        page: Page,
    ) -> list[output_dto.Post]:
        print(f"[{__name__}] called")
        requester = ctx_requested_user_id.get()
        if requester is None:
            return []
        print(f"[{__name__}]: requester: {requester}")
        return []
