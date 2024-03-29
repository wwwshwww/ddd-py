import uuid
from dataclasses import dataclass
from typing import Any

from aiodataloader import DataLoader
from graphql import GraphQLResolveInfo
from starlette.requests import Request

from ddd_py.app_ctx.adapter.inbound.graphql.models import (
    Post,
    PostFilteringOptions,
    PostSortingOption,
    PostSortingType,
    User,
    query,
)
from ddd_py.app_ctx.adapter.inbound.graphql.models import (
    user as user_type,
)
from ddd_py.app_ctx.common.dependencies import Dependencies
from ddd_py.app_ctx.domain.post import post_finder
from ddd_py.app_ctx.domain.user import user


@dataclass
class Context:
    request: Request
    load_posts_by_user: DataLoader[tuple[str, "PostFindOptionSet"], list[Post]]


@query.field("users")
async def resolve_users(
    obj: Any,
    info: GraphQLResolveInfo,
    ids: list[str],
) -> list[User]:
    return []


@user_type.field("")
@dataclass(frozen=True)
class PostFindOptionSet:
    fo: PostFilteringOptions | None
    so: tuple[PostSortingOption, ...] | None


def marshal_post_sorting_option(dto: PostSortingOption) -> post_finder.SortingType:
    if dto.type == PostSortingType.ID:
        return post_finder.SortingTypeId(dto.asc)
    elif dto.type == PostSortingType.REACTION_NUM:
        return post_finder.SortingTypeReactionNum(dto.asc)
    elif dto.type == PostSortingType.CREATOR_ID:
        return post_finder.SortingTypeUserId(dto.asc)
    elif dto.type == PostSortingType.CREATED_AT:
        return post_finder.SortingTypeCreatedAt(dto.asc)

    raise TypeError("invalid sorting type")


class Loader:
    def __init__(self, dependencies: Dependencies) -> None:
        self.dependencies = dependencies

    async def load_posts_by_user(
        self,
        keys: list[tuple[str, PostFindOptionSet]],
    ) -> list[list[Post]]:
        key_group = {key[1] for key in keys}
        result_map: dict[PostFindOptionSet, list[Post]] = {}
        for g in key_group:
            user_ids: list[user.Id] = [
                user.Id(uuid.UUID(key[0])) for key in keys if key[1] == g
            ]

            fo: post_finder.FilteringOptions | None = None
            so: post_finder.SortingOptions | None = None
            if g.fo is not None:
                fo = post_finder.FilteringOptions(
                    user_id_in=user_ids,
                    reaction_num_less=g.fo.reaction_num_less,
                    reaction_num_more=g.fo.reaction_num_more,
                )
            if g.so is not None:
                so = post_finder.SortingOptions(
                    [marshal_post_sorting_option(d) for d in g.so]
                )

            result = await self.dependencies.usecase_find_post.find(
                fo=fo,
                so=so,
            )
            result_map[g] = [
                Post(
                    id=str(r.id.value),
                    content=r.content,
                    creator_id=str(r.user_id.value),
                )
                for r in result
            ]

        return [
            [r for r in result_map[key[1]] if r.creator_id == key[0]] for key in keys
        ]
