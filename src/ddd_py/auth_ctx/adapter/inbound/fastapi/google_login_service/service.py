from typing import Annotated

from ddd_py.auth_ctx.usecase import google_login
from fastapi import APIRouter, Depends, HTTPException


def prepare_dependencies():
    raise NotImplementedError("need to inject dependency")


# * Memo
# def mock_dependencies():
#     try:
#         uc = google_login.Usecase(
#             auth_session.RepositoryMock(),
#             ...
#         )
#         yield uc
#     finally:
#         close()

# app.dependency_overrides[prepare_dependencies] = mock_dependencies


router = APIRouter(
    prefix="/auth/google_login",
    tags=["auth"],
)

# TODO: 302


@router.get("/start", status_code=302)
async def start(
    client_state: str,
    dependencies: Annotated[google_login.Usecase, Depends(prepare_dependencies)],
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

    return {"state": start_output.auth_session_id}


@router.get("/callback")
async def callback(
    state: str,
    code: str,
    dependencies: Annotated[google_login.Usecase, Depends(prepare_dependencies)],
):
    try:
        login_output = await dependencies.login(
            google_login.LoginInput(auth_session_id=state, code=code)
        )
    except google_login.RepositoryError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except google_login.PortError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except google_login.DomainError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except google_login.UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

    return {
        "session_id": login_output.session_id,
        "session_token": login_output.session_token,
    }
