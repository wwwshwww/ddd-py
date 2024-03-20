from abc import ABCMeta, abstractmethod

from ddd_py.app_ctx.common.context import ctx_requested_user_id

from .port import Port

# * Middleware には、他ユースケースの前段階に組み込む可能性のある共通処理を記述する。
# * 処理結果は、contextvars を用いてリクエストスコープ上でグローバルに共有する。
# * 動作モード（API Server, gRPC Server, Lambda, 外部API Server など）に関わらず、
# * あらゆる main ファイルから呼ばれる想定。


class Middleware(metaclass=ABCMeta):
    @abstractmethod
    async def set_user_id_from_session(
        self,
        session_id: str,
        session_token: str,
    ) -> None:
        pass


class MiddlewareImpl(Middleware):
    def __init__(self, port: Port) -> None:
        self.port = port

    async def set_user_id_from_session(
        self,
        session_id: str,
        session_token: str,
    ) -> None:
        try:
            user_id = self.port.verify_session_and_get_user_id(
                session_id,
                session_token,
            )
            ctx_requested_user_id.set(user_id)
        except Exception as e:
            raise e
