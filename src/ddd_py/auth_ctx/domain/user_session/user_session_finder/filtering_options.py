from dataclasses import dataclass

from ddd_py.auth_ctx.domain.user_session import user_session


@dataclass
class FilteringOptions:
    id_in: list[user_session.Id] | None = None
