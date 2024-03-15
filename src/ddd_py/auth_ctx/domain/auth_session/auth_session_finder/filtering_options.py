from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FilteringOptions:
    id_in: Optional[List[str]] = None
