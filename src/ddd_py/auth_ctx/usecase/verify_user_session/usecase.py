from datetime import datetime

from ddd_py.auth_ctx.domain.user_session import user_session
from ddd_py.auth_ctx.usecase.verify_user_session.error import (
    InvalidSessionTokenError,
    SessionExpiredError,
    SessionNotFoundError,
    UserSessionDomainError,
)

from .dto import Input, Output


class Usecase:
    def __init__(self, usr: user_session.Repository):
        self.user_session_repository = usr

    def verify(self, target: Input) -> Output:
        now = datetime.now()

        try:
            usi = user_session.Id(target.session_id)

            # パフォーマンスを考慮し finder を使わず1回のクエリでの取得を試みる
            us = self.user_session_repository.get(usi)
            if not us.is_expired(now):
                raise SessionExpiredError(
                    us.expires_at,
                    f"session expired: {us.expires_at.isoformat()}",
                )

            ust = user_session.Token(target.session_token)
            if not us.check_token(ust):
                raise InvalidSessionTokenError()

        except user_session.DomainError as e:
            raise UserSessionDomainError() from e
        except user_session.RepositoryGetError as e:
            # repo.get() でエラー ＝ 未発見とみなす
            raise SessionNotFoundError() from e
        except SessionExpiredError as e:
            raise e
        except InvalidSessionTokenError as e:
            raise e

        return Output(user_id=us.user_id.value)
