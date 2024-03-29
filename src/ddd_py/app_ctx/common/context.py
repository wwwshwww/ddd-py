from contextvars import ContextVar

from ddd_py.app_ctx.domain.user import user

ctx_requested_user_id: ContextVar[user.Id | None] = ContextVar(
    "ctx_requested_user_id",
    default=None,
)
