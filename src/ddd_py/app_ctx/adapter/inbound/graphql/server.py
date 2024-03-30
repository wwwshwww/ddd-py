import os
import uuid
from typing import Generator

from aiodataloader import DataLoader
from ariadne import (
    SchemaBindable,
    make_executable_schema,
)
from ariadne.asgi import GraphQL
from fastapi import Depends, FastAPI
from starlette.requests import Request

from ddd_py.app_ctx.common.dependencies import Dependencies
from ddd_py.app_ctx.common.types import Page
from ddd_py.app_ctx.domain.post import post as post_domain
from ddd_py.app_ctx.domain.post.post_finder.filtering_options import (
    FilteringOptions,  # TODO: optiont.py に両方とも置いて良い気がした
)
from ddd_py.app_ctx.domain.post.post_finder.sorting_options import SortingOptions
from ddd_py.app_ctx.usecase import (
    find_post,
)
from ddd_py.app_ctx.usecase.common.output_dto import PostDTO

from .dataloader import Loader
from .general import Context
from .query import query, user

schema_path = os.getenv("GRAPHQL_SCHEMA_PATH_1")
schema_text: str = ""
if schema_path:
    with open(schema_path, encoding="utf-8") as f:
        schema_text = f.read()


def get_context_value(request: Request) -> Context:
    print(request.scope["dependencies"])
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


def mock_dependencies() -> Generator[Dependencies, None, None]:
    class MockUsecase1(find_post.Usecase):
        async def find(
            self,
            fo: FilteringOptions | None = None,
            so: SortingOptions | None = None,
            page: Page | None = None,
        ) -> list[PostDTO]:
            print(fo, so, page)
            if fo is None:
                return []
            elif (fo is not None) and (fo.user_id_in is None):
                return []
            else:
                return [
                    PostDTO(post_domain.Id(uuid.uuid4()), "ぬ", ui)
                    for ui in fo.user_id_in
                ]

    try:
        yield Dependencies(
            usecase_find_post=MockUsecase1(),
            usecase_find_post_generate_request=None,
            usecase_find_reaction=None,
            usecase_find_reaction_preset=None,
            usecase_find_user=None,
        )
    finally:
        print("done")


app = FastAPI()


@app.get("/graphql")
async def handle_graphql_explorer(request: Request):
    return await graphql_app.handle_request(request)


@app.post("/graphql")
async def handle_graphql_query(
    request: Request,
    dependencies=Depends(prepare_dependencies),
):
    print(type(dependencies))
    request.scope["dependencies"] = dependencies
    return await graphql_app.handle_request(request)


app.dependency_overrides[prepare_dependencies] = mock_dependencies
