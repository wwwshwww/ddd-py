from dataclasses import dataclass


@dataclass
class StartInput:
    client_state: str


@dataclass
class StartOutput:
    auth_session_id: str


@dataclass
class LoginInput:
    auth_session_id: str
    code: str


@dataclass
class LoginOutput:
    user_id: int
    session_id: str
    session_token: str


@dataclass
class IdpTokenResponse:
    sub: str
