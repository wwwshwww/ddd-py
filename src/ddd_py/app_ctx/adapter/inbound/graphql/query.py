from typing import Any

from ariadne import (
    QueryType,
)
from graphql import GraphQLResolveInfo

from ddd_py.app_ctx.adapter.inbound.graphql.models import User

query = QueryType()


@query.field("users")
async def resolve_users(
    obj: Any,
    info: GraphQLResolveInfo,
    ids: list[str],
) -> list[User]:
    return []
