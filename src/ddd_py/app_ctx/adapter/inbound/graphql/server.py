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
from ddd_py.app_ctx.domain.post import post_finder
from ddd_py.app_ctx.domain.user import user as user_domain
from ddd_py.app_ctx.domain.user import user_finder
from ddd_py.app_ctx.usecase import (
    find_post,
    find_user,
    retrieve_user,
)
from ddd_py.app_ctx.usecase.common.output_dto import PostDTO, UserDTO

from .common import Context
from .dataloader import Loader
from .query import (
    page,
    post,
    post_filtering_options,
    post_sorting_option,
    query,
    user,
)

schema_path = os.getenv("GRAPHQL_SCHEMA_PATH_1")
schema_text: str = ""
if schema_path:
    with open(schema_path, encoding="utf-8") as f:
        schema_text = f.read()


def _get_context_value(request: Request) -> Context:
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
    post,
    page,
    post_filtering_options,
    post_sorting_option,
]
schema = make_executable_schema(schema_text, *binds, convert_names_case=True)


graphql_app = GraphQL(schema, debug=True, context_value=_get_context_value)


def prepare_dependencies() -> Generator[Dependencies, None, None]:
    raise NotImplementedError("need to inject dependency")


def _mock_dependencies() -> Generator[Dependencies, None, None]:
    class MockFindPostUsecase(find_post.Usecase):
        async def find(
            self,
            fo: post_finder.FilteringOptions | None = None,
            so: post_finder.SortingOptions | None = None,
            page: Page | None = None,
        ) -> list[PostDTO]:
            if fo is None:
                return []
            elif (fo is not None) and (fo.user_id_in is None):
                return []
            else:
                return [
                    PostDTO(post_domain.Id(uuid.uuid4()), "ぬ", ui)
                    for ui in fo.user_id_in
                ]

    class MockFindUserUsecase(find_user.Usecase):
        async def find(
            self,
            fo: user_finder.FilteringOptions,
            so: user_finder.SortingOptions,
            page: Page,
        ) -> list[UserDTO]:
            return [
                UserDTO(user_domain.Id(uuid.uuid4()), f"ユーザ_{i}") for i in range(3)
            ]

    class MockRetrieveUserUsecase(retrieve_user.Usecase):
        async def retrieve_by_ids(self, ids: list[user_domain.Id]) -> list[UserDTO]:
            return [UserDTO(i, f"ユーザ_{i}") for i in ids]

    try:
        yield Dependencies(
            usecase_find_post=MockFindPostUsecase(),
            usecase_find_post_generate_request=None,
            usecase_find_reaction=None,
            usecase_find_reaction_preset=None,
            usecase_find_user=MockFindUserUsecase(),
            usecase_retrieve_user=MockRetrieveUserUsecase(),
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


app.dependency_overrides[prepare_dependencies] = _mock_dependencies

""" デバッグ用クエリ
{
  users(
    ids: ["267feef0-8853-49e2-961e-1d0e9ff07263", "29639428-dcd1-4a71-b4e5-005ca04df7cb"]
  ) {
    id,
    name,
    posts(
      filteringOptions: {
        creatorIds: ["u1", "u2"], # user.posts では無視される
      },
      sortingOptions: [
        {idAsc: true}, 
        {reactionNumAsc: false},
      ],
    ) {
      id
      content
    }
  }
}
"""
