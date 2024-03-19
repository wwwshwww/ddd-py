import asyncio
from typing import Annotated

from ddd_py.auth_ctx.usecase import verify_user_session


class Service:
    def __init__(self, usecase: verify_user_session.Usecase):
        self.usecase = usecase

    def verify(self, session_id: str, session_token: str) -> Annotated[int, "user_id"]:
        try:
            result = asyncio.run(
                self.usecase.verify(
                    verify_user_session.Input(
                        session_id=session_id,
                        session_token=session_token,
                    )
                )
            )
        except Exception as e:
            raise Exception("TODO: add error type") from e  # pylint: disable=W0719

        return result.user_id
