from dataclasses import dataclass

from ddd_py.auth_ctx.domain.auth_session import auth_session
from ddd_py.auth_ctx.domain.user import user
from ddd_py.auth_ctx.domain.user_session import user_session


@dataclass
class StartInput:
    client_state: str


@dataclass
class StartOutput:
    auth_session_id: auth_session.Id


@dataclass
class LoginInput:
    auth_session_id: auth_session.Id
    code: str


@dataclass
class LoginOutput:
    user_id: user.Id
    session_id: user_session.Id
    session_token: str


@dataclass
class IdpTokenResponse:
    sub: str
