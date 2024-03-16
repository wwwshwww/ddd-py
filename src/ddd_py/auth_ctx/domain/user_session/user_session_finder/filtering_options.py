from dataclasses import dataclass
from typing import Optional


@dataclass
class FilteringOptions:
    id_in: Optional[list[str]] = None
