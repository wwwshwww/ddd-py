from ddd_py.auth_ctx.domain.auth_session import auth_session

from .port import Port


class Usecase:
    def __init__(
        self,
        usecase_port: Port,
        auth_session_repository: auth_session.Repository,
    ) -> None:
        self.usecase_port = usecase_port
        self.auth_session_repository = auth_session_repository

    def start(self):
        pass

    def login(self):
        pass
