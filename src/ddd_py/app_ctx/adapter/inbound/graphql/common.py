from dataclasses import dataclass

from aiodataloader import DataLoader
from starlette.requests import Request

from ddd_py.app_ctx.common.dependencies import Dependencies

from .dataloader import PostFindOptionSet
from .dto import Post


@dataclass
class Context:
    request: Request
    dependencies: Dependencies
    loader_posts_by_user: DataLoader[tuple[str, PostFindOptionSet], list[Post]]
