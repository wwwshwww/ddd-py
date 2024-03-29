from dataclasses import dataclass
from enum import Enum
from typing import Annotated, Any, Generator

from aiodataloader import DataLoader
from ariadne import (
    EnumType,
    InputType,
    ObjectType,
    QueryType,
    gql,
    make_executable_schema,
)
from ariadne.asgi import GraphQL
from fastapi import Depends, FastAPI
from graphql import GraphQLResolveInfo
from starlette.requests import Request

type_defs = gql("""
    type Query {
        findUser(samples: [Sample!]): [User!]!
    }

    type User {
        id: ID!
        name: String
        posts(sample2: Sample2, sample3: Sample3): [Post!]
    }

    type Post {
        id: ID!
        content: String
    }
    
    enum SampleType {
        ONE
        TWO
    }

    input Sample {
        sampleType: SampleType!
        asc: Boolean!
    }
                
    input Sample2 {
        value: Int!
    }
                
    input Sample3 {
        value: Int!
    }
    
""")


@dataclass
class User:
    id: str
    name: str


@dataclass
class Post:
    id: str
    content: str


class SampleType(Enum):
    ONE = 1
    TWO = 2


@dataclass(frozen=True)
class Sample:
    sample_type: SampleType
    asc: bool


@dataclass(frozen=True)
class Sample2:
    value: int


@dataclass(frozen=True)
class Sample3:
    value: int


query = QueryType()
user = ObjectType("User")
post = ObjectType("Post")
sample = InputType("Sample", lambda i: Sample(**i))
sample_impl = EnumType("SampleType", SampleType)


@query.field("findUser")
async def resolve_find_user(
    obj: Any,
    info: GraphQLResolveInfo,
    samples: list[Sample] | None = None,
) -> list[User]:
    print(type(samples))
    print(samples)
    return [User("1", "John"), User("2", "Bob")]


@user.field("posts")
async def resolve_posts(
    obj: User,
    info: GraphQLResolveInfo,
    sample2: Sample2 | None = None,
    sample3: Sample3 | None = None,
) -> list[Post]:
    print(obj)
    # return [Post("1", "Hello World")]
    ctx: Ctx = info.context
    # result = await ctx.post_loader.load(obj.id)
    result = await ctx.post_loader3.load((sample2, sample3))
    return result


schema = make_executable_schema(
    type_defs,
    *[
        query,
        user,
        post,
        sample,
        sample_impl,
    ],
    convert_names_case=True,
)


@dataclass
class Dependencies:
    dep1: str


def prepare_dependencies() -> Generator[Dependencies, None, None]:
    raise NotImplementedError("need to inject dependency")


async def post_loader(user_ids: list[str]) -> list[list[Post]]:
    print(user_ids)
    return [
        [Post("i1", f"user {ui} content 1"), Post("i2", f"user {ui} content 2")]
        for ui in user_ids
    ]


async def post_loader2(
    keys: list[tuple[Sample2 | None, Sample3 | None]],
) -> list[list[Post]]:
    print(keys)
    return [[] for _ in range(len(keys))]


class Loaders:
    def __init__(self, dependencies: Dependencies):
        self.dependencies = dependencies

    async def post_loader3(
        self, keys: list[tuple[Sample2 | None, Sample3 | None]]
    ) -> list[list[Post]]:
        print(keys)
        return [[] for _ in range(len(keys))]


@dataclass
class Ctx:
    request: Request
    post_loader: DataLoader[str, list[Post]]
    post_loader2: DataLoader[tuple[Sample2 | None, Sample3 | None], list[Post]]
    post_loader3: DataLoader[tuple[Sample2 | None, Sample3 | None], list[Post]]


def get_context_value(request: Request) -> Ctx:
    # return {"request": request, "post_loader": DataLoader(post_loader)}
    l = Loaders(request.scope["dep"])

    return Ctx(
        request=request,
        post_loader=DataLoader(post_loader),
        post_loader2=DataLoader(post_loader2),
        post_loader3=DataLoader(l.post_loader3),
    )


graphql_app = GraphQL(schema, debug=True, context_value=get_context_value)

app = FastAPI()


@app.get("/graphql")
async def handle_graphql_explorer(request: Request):
    return await graphql_app.handle_request(request)


@app.post("/graphql")
async def handle_graphql_query(
    request: Request,
    dep=Annotated[Dependencies, Depends(prepare_dependencies)],
):
    request.scope["dep"] = dep
    return await graphql_app.handle_request(request)
