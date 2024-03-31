from abc import ABCMeta, abstractmethod

from ddd_py.app_ctx.common.context import ctx_requested_user_id
from ddd_py.app_ctx.common.types import Page
from ddd_py.app_ctx.domain.reaction import reaction, reaction_finder
from ddd_py.app_ctx.usecase.common import output_dto


class Usecase(metaclass=ABCMeta):
    @abstractmethod
    async def find(
        self,
        fo: reaction_finder.FilteringOptions,
        so: reaction_finder.SortingOptions,
        page: Page,
    ) -> list[output_dto.ReactionDTO]:
        pass


# TODO:
class UsecaseImpl(Usecase):
    def __init__(self, rf: reaction.Repository, rr: reaction_finder.Finder) -> None:
        self.rf = rf
        self.rr = rr

    async def find(
        self,
        fo: reaction_finder.FilteringOptions,
        so: reaction_finder.SortingOptions,
        page: Page,
    ) -> list[output_dto.ReactionDTO]:
        print(f"[{__name__}] called")
        requester = ctx_requested_user_id.get()
        if requester is None:
            return []
        print(f"[{__name__}]: requester: {requester}")
        return []
