from abc import ABC, abstractmethod

from ddd_py.app_ctx.common.context import ctx_requested_user_id
from ddd_py.app_ctx.common.types import Page
from ddd_py.app_ctx.domain.reaction_preset import (
    reaction_preset,
    reaction_preset_finder,
)
from ddd_py.app_ctx.usecase.common import output_dto


class Usecase(ABC):
    @abstractmethod
    async def find(
        self,
        fo: reaction_preset_finder.FilteringOptions,
        so: reaction_preset_finder.SortingOptions,
        page: Page,
    ) -> list[output_dto.ReactionPresetDTO]:
        pass


# TODO:
class UsecaseImpl(Usecase):
    def __init__(
        self, rf: reaction_preset.Repository, rr: reaction_preset_finder.Finder
    ) -> None:
        self.rf = rf
        self.rr = rr

    async def find(
        self,
        fo: reaction_preset_finder.FilteringOptions,
        so: reaction_preset_finder.SortingOptions,
        page: Page,
    ) -> list[output_dto.ReactionPresetDTO]:
        print(f"[{__name__}] called")
        requester = ctx_requested_user_id.get()
        if requester is None:
            return []
        print(f"[{__name__}]: requester: {requester}")
        return []
