import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class Id:
    value: uuid.UUID


def generate_id() -> Id:
    return Id(uuid.uuid4())
