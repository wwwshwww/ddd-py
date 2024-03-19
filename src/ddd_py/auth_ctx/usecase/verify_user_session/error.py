from datetime import datetime


class UserSessionDomainError(Exception): ...


class UserSessionRepositoryError(Exception): ...


class SessionExpiredError(Exception):
    def __init__(self, expires_at: datetime, *args: object):
        super().__init__(*args)

        self.expires_at = expires_at


class SessionNotFoundError(Exception): ...


class InvalidSessionTokenError(Exception): ...
