import asyncio
import uuid

from ddd_py.auth_ctx.domain.user import user
from ddd_py.auth_ctx.domain.user_session import user_session
from ddd_py.auth_ctx.usecase import verify_user_session


class Service:
    def __init__(self, usecase: verify_user_session.Usecase):
        self.usecase = usecase

    def verify(self, session_id: str, session_token: str) -> user.Id:
        try:
            result = asyncio.run(
                self.usecase.verify(
                    verify_user_session.Input(
                        session_id=user_session.Id(uuid.UUID(session_id)),
                        session_token=session_token,
                    )
                )
            )
        except Exception as e:
            raise Exception("TODO: add error type") from e  # pylint: disable=W0719

        return result.user_id
