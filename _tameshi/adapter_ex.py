import asyncio
from collections.abc import Generator
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()
router = APIRouter()


class Usecase1:
    def __init__(self, repo: str):
        self.repo = repo

    async def get1(self) -> str:
        return f"{self.repo}1"


class Usecase2:
    def __init__(self, repo: str):
        self.repo = repo

    async def get2(self) -> str:
        return f"{self.repo}2"


def gen_dependencies() -> Generator[tuple[Usecase1, Usecase2], None, None]:
    raise NotImplementedError("need to inject dependency")


def mock_dependencies() -> Generator[tuple[Usecase1, Usecase2], None, None]:
    try:
        print("mock だよ")
        yield Usecase1("mock"), Usecase2("mock")
    finally:
        print("clean up mock")


class MyResponse(BaseModel):
    hello: str
    world: str


@router.get(
    "/",
    status_code=302,
    responses={
        302: {
            "description": "ほげ",
            "model": MyResponse,
            "headers": {"Location": {"schema": {"type": "string"}}},
        }
    },
)
async def read_root(
    deps: Annotated[tuple[Usecase1, Usecase2], Depends(gen_dependencies)],
    p: str | None = None,
):
    print(p)
    uc1, uc2 = deps
    out1, out2 = await asyncio.gather(uc1.get1(), uc2.get2())
    headers = {"Location": "/docs"}
    content = MyResponse(hello=out1, world=out2)
    return JSONResponse(
        status_code=302, content=jsonable_encoder(content), headers=headers
    )


app.include_router(router)
app.dependency_overrides[gen_dependencies] = mock_dependencies
