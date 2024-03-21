from abc import ABCMeta, abstractmethod

from ddd_py.app_ctx.domain.user import user


class Port(metaclass=ABCMeta):
    @abstractmethod
    def verify_session_and_get_user_id(
        self,
        session_id: str,
        session_token: str,
    ) -> user.Id:
        pass
