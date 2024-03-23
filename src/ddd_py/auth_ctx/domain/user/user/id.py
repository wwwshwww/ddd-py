import uuid
from dataclasses import dataclass

import ulid


@dataclass(frozen=True)
class Id:
    value: uuid.UUID


def generate_id() -> Id:
    return Id(ulid.new().uuid)
