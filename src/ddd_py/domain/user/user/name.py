from dataclasses import dataclass
import re

from . import error

INVALID_NAME_CHARS_REGEX = re.compile(r"[@<>{}]")

NAME_MIN_LENGTH, NAME_MAX_LENGTH = 1, 11

@dataclass(frozen=True)
class Name:
    value: str

    def __post_init__(self):
        if INVALID_NAME_CHARS_REGEX.search(self.value):
            raise error.DomainError("invalid name characters")
        if (len(self.value) < NAME_MIN_LENGTH) or (len(self.value) > NAME_MAX_LENGTH):
            raise error.DomainError("invalid name length")
