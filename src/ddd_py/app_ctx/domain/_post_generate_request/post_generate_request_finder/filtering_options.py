from dataclasses import dataclass
from typing import Optional

from ddd_py.app_ctx.domain.user import user


@dataclass
class FilteringOptions:
    user_id: Optional[user.Id] = None
    exclude_uncompleted: bool = False
    exclude_completed: bool = False
