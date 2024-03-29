from abc import ABC, abstractmethod

from ddd_py.app_ctx.common.context import ctx_requested_user_id
from ddd_py.app_ctx.common.types import Page
from ddd_py.app_ctx.domain.post_generate_request import (
    post_generate_request,
    post_generate_request_finder,
)
from ddd_py.app_ctx.usecase.common import output_dto


class Usecase(ABC):
    @abstractmethod
    async def find(
        self,
        fo: post_generate_request_finder.FilteringOptions,
        so: post_generate_request_finder.SortingOptions,
        page: Page,
    ) -> list[output_dto.PostGenerateRequestDTO]:
        pass


# TODO:
class UsecaseImpl(Usecase):
    def __init__(
        self,
        pf: post_generate_request_finder.Finder,
        pr: post_generate_request.Repository,
    ):
        self.pf = pf
        self.pr = pr

    async def find(
        self,
        fo: post_generate_request_finder.FilteringOptions,
        so: post_generate_request_finder.SortingOptions,
        page: Page,
    ) -> list[output_dto.PostGenerateRequestDTO]:
        print(f"[{__name__}] called")
        requester = ctx_requested_user_id.get()
        if requester is None:
            return []
        print(f"[{__name__}]: requester: {requester}")
        return []
