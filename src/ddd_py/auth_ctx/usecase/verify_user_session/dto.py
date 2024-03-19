from dataclasses import dataclass


@dataclass
class Input:
    session_id: str
    session_token: str


@dataclass
class Output:
    user_id: int
