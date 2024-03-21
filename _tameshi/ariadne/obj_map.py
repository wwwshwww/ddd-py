"""query example

{
  user(
    userId: 1,
    num: 1,
    options: {
        optionalToggle: false,
    },
  ) {
    id
    nameCamelCase
  }
}

{
  user {
    id
    nameCamelCase
  }
}
"""

from dataclasses import dataclass
from typing import Any

from ariadne import QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from fastapi import FastAPI, Request
from graphql import GraphQLResolveInfo

type_defs = gql("""
    type Query {
        user(userId: ID, num: Int, options: Options): User!
    }

    type User {
        id: ID!
        nameCamelCase: String!
        email: String
    }
                
    input Options {
        optionalToggle: Boolean
    }
""")


@dataclass
class User:
    id: str
    name_camel_case: str
    email: str


@dataclass
class Options:
    optional_toggle: bool | None = None


query = QueryType()


@query.field("user")
def resolve_user(
    obj: Any,
    info: GraphQLResolveInfo,
    user_id: str | None = None,
    num: int | None = None,
    # options: Options | None = None,
    # *  ↑ make_executable_schema に InputType("Options", lambda data: Options(**data)),
    # *  を渡すことで Python オブジェクトの Options に直接マップできる
    options: dict | None = None,
):
    print(f"\n\n[obj]: {obj}\n\n")
    print(f"[info]: {info}\n\n")
    print(f"[user_id]: {user_id}\n\n")
    print(f"[num]: {num}\n\n")
    print(f"[options]: {options}\n\n")

    print(type(user_id))
    print(type(num))
    if user_id:
        return User(f"dummy-{user_id}", "dummy-name", "abc123@example.com")
    else:
        return User("dummy-unspecified", "unknown", "unknown")


schema = make_executable_schema(
    type_defs,
    query,
    # InputType("Options", lambda data: Options(**data)),
    convert_names_case=True,
)

graphql_app = GraphQL(schema, debug=True)

app = FastAPI()


# Handle GET requests to serve GraphQL explorer
# Handle OPTIONS requests for CORS
@app.get("/graphql/")
@app.options("/graphql/")
async def handle_graphql_explorer(request: Request):
    return await graphql_app.handle_request(request)


# Handle POST requests to execute GraphQL queries
@app.post("/graphql/")
async def handle_graphql_query(request: Request):
    return await graphql_app.handle_request(request)
