from abc import ABCMeta, abstractmethod


class Port(metaclass=ABCMeta):
    @abstractmethod
    def verify_session_and_get_user_id(
        self,
        session_id: str,
        session_token: str,
    ) -> int:
        pass
