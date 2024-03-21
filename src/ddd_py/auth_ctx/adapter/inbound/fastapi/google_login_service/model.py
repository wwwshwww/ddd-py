from pydantic import BaseModel

from ddd_py.auth_ctx.domain.user import user


class LoginResponse(BaseModel):
    user_id: user.Id
    session_token: str
