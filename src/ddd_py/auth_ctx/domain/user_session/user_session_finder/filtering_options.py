from dataclasses import dataclass
from typing import Optional

from ddd_py.auth_ctx.domain.user_session import user_session


@dataclass
class FilteringOptions:
    id_in: Optional[list[user_session.Id]] = None
