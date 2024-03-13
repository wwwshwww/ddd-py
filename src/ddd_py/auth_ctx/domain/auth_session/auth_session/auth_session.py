import datetime

from .id import Id
from .app_route import AppRoute
from .error import DomainError

EXPIRATION = datetime.timedelta(minutes=15) # 認証セッションの有効期限

class AuthSession():
    def __init__(self, id: Id, app_route: AppRoute, started_at: datetime.datetime, expired_at: datetime.datetime) -> None:
        if started_at > expired_at:
            raise DomainError('started_at must be before expired_at')
        
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
    def app_route(self) -> AppRoute:
        return self._app_route
    
    @property
    def started_at(self) -> datetime.datetime:
        return self._started_at

    @property
    def expired_at(self) -> datetime.datetime:
        return self._expired_at

def create_auth_session(id: Id, app_route: AppRoute, now: datetime.datetime) -> AuthSession:
    return AuthSession(id, app_route, now, now + EXPIRATION)
