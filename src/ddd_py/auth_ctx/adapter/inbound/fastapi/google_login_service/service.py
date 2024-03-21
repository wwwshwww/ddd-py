import uuid
from collections.abc import Generator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse

from ddd_py.auth_ctx.domain.auth_session import auth_session
from ddd_py.auth_ctx.usecase import google_login

from .model import LoginResponse

AUTH_ENDPOINT = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


router = APIRouter(
    prefix="/auth/google_login",
    tags=["auth"],
)


def prepare_dependencies() -> Generator[google_login.Usecase, None, None]:
    raise NotImplementedError("need to inject dependency")


# * Memo
# def mock_dependencies() -> Generator[google_login.Usecase, None, None]:
#     try:
#         uc = google_login.Usecase(
#             auth_session.RepositoryMock(),
#             ...
#         )
#         yield uc
#     finally:
#         close()

# app.dependency_overrides[prepare_dependencies] = mock_dependencies


@router.get(
    path="/",
    status_code=302,
    response_class=RedirectResponse,
    responses={
        302: {
            "description": "OK",
            "content": {
                "text/plain": {},
            },
            "headers": {
                "Location": {
                    "description": "SPAの場合は手動でリダイレクトしてね",
                    "schema": {
                        "type": "string",
                        "example": "https://example.com/v1/auth?state=xxxxxxx",
                    },
                }
            },
        }
    },
)
async def start(
    dependencies: Annotated[google_login.Usecase, Depends(prepare_dependencies)],
    client_state: str = "",
):
    try:
        start_output = await dependencies.start(
            google_login.StartInput(client_state=client_state)
        )
    except google_login.RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except google_login.PortError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except google_login.DomainError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except google_login.UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

    url = f"{AUTH_ENDPOINT}?state={str(start_output.auth_session_id.value)}"

    return RedirectResponse(url=url, status_code=302)


# TODO: write correct OpenAPI


@router.get(
    path="/callback",
    response_model=LoginResponse,
)
async def callback(
    dependencies: Annotated[google_login.Usecase, Depends(prepare_dependencies)],
    state: str,
    code: str,
) -> LoginResponse:
    try:
        login_output = await dependencies.login(
            google_login.LoginInput(
                auth_session_id=auth_session.Id(uuid.UUID(state)),
                code=code,
            )
        )
    except google_login.RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except google_login.PortError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except google_login.DomainError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except google_login.UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

    content = jsonable_encoder(
        LoginResponse(
            user_id=str(login_output.user_id.value),
            session_token=login_output.session_token,
        )
    )
    resp = JSONResponse(content=content)
    resp.set_cookie(
        key="sid",
        value=login_output.auth_session_id,
        secure=True,
        httponly=True,
        samesite="lax",
    )
    return resp
