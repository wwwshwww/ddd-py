from pydantic import BaseModel


class LoginResponse(BaseModel):
    user_id: int
    session_token: str
