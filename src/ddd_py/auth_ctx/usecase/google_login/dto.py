from dataclasses import dataclass


@dataclass
class StartInput:
    state_value: str


@dataclass
class StartOutput:
    state_id: str


@dataclass
class LoginInput:
    state_id: str
    code: str


@dataclass
class LoginOutput:
    user_id: int
    session_id: str
    session_token: str
