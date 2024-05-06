import uuid
from datetime import datetime
from typing import Any

import dateutil
import dateutil.parser
from ariadne import EnumType, InputType, ObjectType, QueryType, ScalarType
from graphql import GraphQLResolveInfo

from ddd_py.app_ctx.domain.user import user as user_domain

from .common import Context
from .dataloader import PostFindOptionSet
from .dto import (
    Page,
    Post,
    PostFilteringOptions,
    PostSortingOption,
    User,
    UserFilteringOptions,
    UserSortingOption,
)

datetime_scalar = ScalarType("Datetime")

query = QueryType()
user = ObjectType("User")
post = ObjectType("Post")

page = InputType("Page", lambda x: Page(**x))

user_filtering_options = InputType(
    "UserFilteringOptions", lambda x: UserFilteringOptions(**x)
)
user_sorting_option = InputType("UserSortingOption", lambda x: UserSortingOption(**x))


# * クライアントから配列データを渡されると問答無用で list型 として扱ってしまうので、hashable な tuple型 に変換している
# * （マッピング先の型ヒントに自動で合わせてほしい。動的型付けの限界）
def _parse_post_filtering_options(x: dict[str, Any]) -> PostFilteringOptions:
    if "creator_ids" in x:
        x["creator_ids"] = tuple(x["creator_ids"])
    return PostFilteringOptions(**x)


post_filtering_options = InputType(
    "PostFilteringOptions", _parse_post_filtering_options
)
post_sorting_option = InputType("PostSortingOption", lambda x: PostSortingOption(**x))


@datetime_scalar.serializer
def serialize_datetime(value: datetime):
    return value.isoformat()


@datetime_scalar.value_parser
def parse_datetime_value(value: str) -> datetime:
    try:
        return dateutil.parser.parse(value)
    except Exception as e:
        raise ValueError(f"Can not parse datetime value: {value}") from e


@query.field("users")
async def resolve_users(
    obj: Any,
    info: GraphQLResolveInfo,
    ids: list[str],
) -> list[User | None]:
    ctx: Context = info.context
    print(ids)
    users = await ctx.dependencies.usecase_retrieve_user.retrieve_by_ids(
        [user_domain.Id(uuid.UUID(i)) for i in ids]
    )
    return [User(str(u.id.value), u.name) for u in users]


# ! user.posts においては、所持者ユーザのID指定を意味する filteringOption.creatorIds は無視される
# ?: 初期時点で、サブリソース取得に find と同等レベルのフィルタリングやソーティングを搭機する意味は薄いかもしれない。
# ?: 後から徐々にクライアントの要件に合わせて追加していく場合、input type を find と共通で利用する必要もない。
# TODO: ↑ 対応。ケースに応じて指定無効なフィールドが発生するようなパターンは混乱しやすいため
@user.field("posts")
async def resolve_posts(
    obj: User,
    info: GraphQLResolveInfo,
    filtering_options: PostFilteringOptions | None = None,
    sorting_options: list[PostSortingOption] | None = None,
) -> list[Post]:
    ctx: Context = info.context
    print(ctx)
    print(filtering_options, sorting_options)
    res = await ctx.loader_posts_by_user.load(
        (
            obj.id,
            PostFindOptionSet(
                filtering_options,
                tuple(sorting_options) if sorting_options is not None else None,
            ),
        )
    )
    print(res)
    return res

    # return [Post(f"p_{obj.id}", f"post by {obj.name}", obj.id)]
