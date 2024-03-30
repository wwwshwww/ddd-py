import os
from typing import Annotated, Generator

from aiodataloader import DataLoader
from ariadne import (
    SchemaBindable,
    make_executable_schema,
)
from ariadne.asgi import GraphQL
from fastapi import Depends, FastAPI
from starlette.requests import Request

from ddd_py.app_ctx.common.dependencies import Dependencies

from .dataloader import Loader
from .general import Context
from .query import query, user

schema_path = os.getenv("GRAPHQL_SCHEMA_PATH_1")
schema_text: str = ""
if schema_path:
    with open(schema_path, encoding="utf-8") as f:
        schema_text = f.read()


def get_context_value(request: Request) -> Context:
    loader = Loader(request.scope["dependencies"])

    return Context(
        request=request,
        dependencies=request.scope["dependencies"],
        loader_posts_by_user=DataLoader(loader.load_posts_by_user),
    )


binds: list[SchemaBindable] = [
    query,
    user,
]
schema = make_executable_schema(schema_text, *binds, convert_names_case=True)


graphql_app = GraphQL(schema, debug=True, context_value=get_context_value)


def prepare_dependencies() -> Generator[Dependencies, None, None]:
    raise NotImplementedError("need to inject dependency")


app = FastAPI()


@app.get("/graphql")
async def handle_graphql_explorer(request: Request):
    return await graphql_app.handle_request(request)


@app.post("/graphql")
async def handle_graphql_query(
    request: Request,
    dependencies=Annotated[Dependencies, Depends(prepare_dependencies)],
):
    request.scope["dependencies"] = dependencies
    return await graphql_app.handle_request(request)
