import datetime
from typing import Self

from .client_state import ClientState
from .error import DomainError
from .id import Id, generate_id

EXPIRATION = datetime.timedelta(minutes=10)  # 認証セッションの有効期限


class AuthSession:
    def __init__(
        self,
        id: Id,
        client_state: ClientState,
        started_at: datetime.datetime,
        expires_at: datetime.datetime,
    ) -> None:
        if started_at > expires_at:
            raise DomainError("started_at must be before expired_at")

        self._id = id
        self._client_state = client_state
        self._started_at = started_at
        self._expires_at = expires_at

    def is_expired(self, now: datetime.datetime) -> bool:
        return self._expires_at < now

    @property
    def id(self) -> Id:
        return self._id

    @property
    def client_state(self) -> ClientState:
        return self._client_state

    @property
    def started_at(self) -> datetime.datetime:
        return self._started_at

    @property
    def expires_at(self) -> datetime.datetime:
        return self._expires_at

    def is_equivalent(self, other: Self) -> bool:
        return (
            self.id == other.id
            and self.client_state == other.client_state
            and self.started_at == other.started_at
            and self.expires_at == other.expires_at
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AuthSession):
            return False

        return (
            self._id == other._id
            and self._client_state == other._client_state
            and self._started_at == other._started_at
            and self._expires_at == other._expires_at
        )


def generate_auth_session(
    client_state: ClientState, now: datetime.datetime
) -> AuthSession:
    i = generate_id()
    return AuthSession(i, client_state, now, now + EXPIRATION)
