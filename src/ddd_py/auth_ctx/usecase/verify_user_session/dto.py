from dataclasses import dataclass

from ddd_py.auth_ctx.domain.user import user
from ddd_py.auth_ctx.domain.user_session import user_session


@dataclass
class Input:
    session_id: user_session.Id
    session_token: str


@dataclass
class Output:
    user_id: user.Id
