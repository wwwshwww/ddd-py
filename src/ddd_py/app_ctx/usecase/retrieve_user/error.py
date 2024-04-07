from typing import Any

from ddd_py.app_ctx.domain.user.user import Id


class NotFoundError(Exception):
    def __init__(self, message: Any, notfound_ids: list[Id]) -> None:
        super().__init__(message)
        self.notfound_ids = notfound_ids
