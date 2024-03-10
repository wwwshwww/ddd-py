from dataclasses import dataclass

from . import error

KEYWORD_MIN_LENGTH, KEYWORD_MAX_LENGTH = 1, 10

@dataclass(frozen=True)
class Keyword:
    value: str

    def __post_init__(self):
        if (len(self.value) < KEYWORD_MIN_LENGTH) or (len(self.value) > KEYWORD_MAX_LENGTH):
            raise error.DomainError("invalid keyword length")
