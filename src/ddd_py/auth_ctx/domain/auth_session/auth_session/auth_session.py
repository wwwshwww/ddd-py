import datetime

from .client_state import ClientState
from .error import DomainError
from .id import Id, generate_id

EXPIRATION = datetime.timedelta(minutes=15)  # 認証セッションの有効期限


class AuthSession:
    def __init__(
        self,
        id: Id,
        app_route: ClientState,
        started_at: datetime.datetime,
        expired_at: datetime.datetime,
    ) -> None:
        if started_at > expired_at:
            raise DomainError("started_at must be before expired_at")

        self._id = id
        self._app_route = app_route
        self._started_at = started_at
        self._expired_at = expired_at

    def is_expired(self, now: datetime.datetime) -> bool:
        return self._expired_at < now

    @property
    def id(self) -> Id:
        return self._id

    @property
    def app_route(self) -> ClientState:
        return self._app_route

    @property
    def started_at(self) -> datetime.datetime:
        return self._started_at

    @property
    def expired_at(self) -> datetime.datetime:
        return self._expired_at


def generate_auth_session(
    client_state: ClientState, now: datetime.datetime
) -> AuthSession:
    i = generate_id()
    return AuthSession(i, client_state, now, now + EXPIRATION)
