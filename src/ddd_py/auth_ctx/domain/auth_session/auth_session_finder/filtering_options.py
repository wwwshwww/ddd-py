from dataclasses import dataclass
from typing import Optional

from ddd_py.auth_ctx.domain.auth_session import auth_session


@dataclass
class FilteringOptions:
    id_in: Optional[list[auth_session.Id]] = None
