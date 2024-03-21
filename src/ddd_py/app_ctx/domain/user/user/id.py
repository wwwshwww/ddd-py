import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class Id:
    value: uuid.UUID
