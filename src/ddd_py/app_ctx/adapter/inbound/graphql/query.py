from typing import Any

from ariadne import EnumType, InputType, ObjectType, QueryType

from graphql import GraphQLResolveInfo

from .dto import (
    Page,
    Post,
    PostFilteringOptions,
    PostGenerateRequestGenStatus,
    PostSortingOption,
    PostSortingType,
    User,
    UserFilteringOptions,
    UserSortingOption,
    UserSortingType,
)
from .general import Context

query = QueryType()
user = ObjectType("User")
post = ObjectType("Post")
post_generate_request = ObjectType("PostGenerateRequest")
post_generate_request_gen_status = EnumType(
    "PostGenerateRequestGenStatus", PostGenerateRequestGenStatus
)
reaction = ObjectType("Reaction")
reaction_preset = ObjectType("ReactionPreset")
page = InputType("Page", lambda x: Page(**x))
user_filtering_options = InputType(
    "UserFilteringOptions", lambda x: UserFilteringOptions(**x)
)
user_sorting_type = EnumType("UserSortingType", UserSortingType)
user_sorting_option = InputType("UserSortingOption", lambda x: UserSortingOption(**x))
post_filtering_options = InputType(
    "PostFilteringOptions", lambda x: PostFilteringOptions(**x)
)
post_sorting_type = EnumType("PostSortingType", PostSortingType)
post_sorting_option = InputType("PostSortingOption", lambda x: PostSortingOption(**x))


@query.field("users")
async def resolve_users(
    obj: Any,
    info: GraphQLResolveInfo,
    ids: list[str],
) -> list[User]:
    ctx: Context = info.context
    print(ids)
    return [User("u1", "Sam"), User("u2", "Bob")]


@user.field("posts")
async def resolve_posts(
    obj: User,
    info: GraphQLResolveInfo,
    fo: PostFilteringOptions | None = None,
    so: list[PostSortingOption] | None = None,
) -> list[Post]:
    ctx: Context = info.context
    print(ctx)
    print(fo, so)
    # res = await ctx.loader_posts_by_user.load(
    #     (
    #         obj.id,
    #         PostFindOptionSet(fo, tuple(s for s in so) if so is not None else None),
    #     )
    # )
    # print(res)
    # return res

    return [Post(f"p_{obj.id}", f"post by {obj.name}", obj.id)]
