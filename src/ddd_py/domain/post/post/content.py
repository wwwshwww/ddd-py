from dataclasses import dataclass
from . import error

CONTENT_MIN_LENGTH, CONTENT_MAX_LENGTH = 1, 100

@dataclass(frozen=True)
class Content:
    value: str

    def __post_init__(self):
        if (len(self.value) < CONTENT_MIN_LENGTH) or (len(self.value) > CONTENT_MAX_LENGTH):
            raise error.DomainError("invalid content length")
        
    def IsEmpty(self) -> bool:
        return len(self.value) == 0