from contextvars import ContextVar

ctx_requested_user_id: ContextVar[int | None] = ContextVar(
    "ctx_requested_user_id", None
)
