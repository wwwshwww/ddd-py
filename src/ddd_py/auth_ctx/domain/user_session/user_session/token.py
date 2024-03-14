import secrets
from dataclasses import dataclass

TOKEN_BYTE_LENGTH = 32


@dataclass(frozen=True)
class Token:
    value: str


def generate_token() -> Token:
    return Token(secrets.token_urlsafe(TOKEN_BYTE_LENGTH))
