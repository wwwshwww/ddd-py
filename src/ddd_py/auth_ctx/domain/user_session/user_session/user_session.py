import copy
import datetime

import bcrypt

from ddd_py.auth_ctx.domain.user import user

from .error import DomainError
from .id import Id, generate_id
from .token import Token, generate_token

EXPIRES_DURATION = datetime.timedelta(
    days=1
)  # 最後のアクティビティからセッションが切れるまでの時間
LIFE_SPAN = datetime.timedelta(days=14)  # セッションの生存期間上限
HASH_COST = 4


class UserSession:
    def __init__(
        self,
        id: Id,
        user_id: user.Id,
        hashed_token: str,
        created_at: datetime.datetime,
        last_activity_at: datetime.datetime,
        expires_at: datetime.datetime,
    ):
        if (expires_at - created_at) > LIFE_SPAN:
            raise DomainError("expires_at must be less than LIFE_SPAN")

        self._id = id
        self._user_id = user_id
        self._hashed_token = hashed_token
        self._created_at = created_at
        self._last_activity_at = last_activity_at
        self._expires_at = expires_at

    def activity(self, now: datetime.datetime):
        self._last_activity_at = now
        expected_expires_at = self._last_activity_at + EXPIRES_DURATION

        if (expected_expires_at - self._created_at) > LIFE_SPAN:
            self._expires_at = self._created_at + LIFE_SPAN
        else:
            self._expires_at = expected_expires_at

    def invalidate(self, now: datetime.datetime):
        self._expires_at = now
        self._last_activity_at = now

    def is_expired(self, now: datetime.datetime):
        return self._expires_at > now

    def check_token(self, token: Token):
        return bcrypt.checkpw(token.value.encode(), self._hashed_token.encode())

    @property
    def id(self):
        return self._id

    @property
    def user_id(self):
        return self._user_id

    @property
    def hashed_token(self):
        return self._hashed_token

    @property
    def created_at(self):
        return self._created_at

    @property
    def last_activity_at(self):
        return self._last_activity_at

    @property
    def expires_at(self):
        return self._expires_at


def generate(user_id: user.Id, now: datetime.datetime) -> tuple[UserSession, Token]:
    i = generate_id()
    token = generate_token()
    hashed_token = bcrypt.hashpw(token.value.encode(), bcrypt.gensalt(rounds=HASH_COST))

    try:
        session = UserSession(
            i,
            user_id,
            hashed_token.decode(),
            copy.deepcopy(now),
            copy.deepcopy(now),
            copy.deepcopy(now) + EXPIRES_DURATION,
        )
    except DomainError as e:
        raise e

    return session, token
