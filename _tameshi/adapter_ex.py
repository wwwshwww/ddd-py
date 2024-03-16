import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI

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


def gen_dependencies():
    raise NotImplementedError("need to inject dependency")


def mock_dependencies():
    try:
        print("mock だよ")
        yield Usecase1("mock"), Usecase2("mock")
    finally:
        print("clean up mock")


@router.get("/")
async def read_root(
    deps: Annotated[tuple[Usecase1, Usecase2], Depends(gen_dependencies)],
):
    uc1, uc2 = deps
    out1, out2 = await asyncio.gather(uc1.get1(), uc2.get2())
    return {"Hello": out1, "World": out2}


app.include_router(router)
app.dependency_overrides[gen_dependencies] = mock_dependencies
