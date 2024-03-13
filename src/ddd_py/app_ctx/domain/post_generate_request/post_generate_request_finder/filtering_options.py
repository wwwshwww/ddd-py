from dataclasses import dataclass
from typing import Optional

@dataclass
class FilteringOptions:
    user_id: Optional[int] = None
    exclude_uncompleted: bool = False
    exclude_completed: bool = False
