from dataclasses import dataclass
from typing import Optional


@dataclass
class FilteringOptions:
    name_exact: Optional[str] = None
    name_front: Optional[str] = None
    name_partial: Optional[str] = None
    name_back: Optional[str] = None
