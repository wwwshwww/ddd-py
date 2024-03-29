from datetime import datetime
from enum import Enum

from ddd_py.app_ctx.domain.post import post
from ddd_py.app_ctx.domain.user import user

from .error import DomainError
from .id import Id
from .keyword import Keyword

KEYWORDS_NUM_MIN, KEYWORDS_NUM_MAX = 1, 3


class GenerationStatus(Enum):
    UNCOMPLETED = 1
    COMPLETED = 2


class PostGenerateRequest:
    def __init__(
        self,
        id: Id,
        user_id: user.Id,
        keywords: list[Keyword],
        requested_at: datetime,
        generated_post_id: post.Id | None,
    ) -> None:
        if (len(keywords) < KEYWORDS_NUM_MIN) or (len(keywords) > KEYWORDS_NUM_MAX):
            raise DomainError(
                f"keywords must be between {KEYWORDS_NUM_MIN} and {KEYWORDS_NUM_MAX}"
            )

        self._id = id
        self._user_id = user_id
        self._keywords = keywords
        self._requested_at = requested_at
        self._generated_post_id = generated_post_id

    @property
    def id(self) -> Id:
        return self._id

    @property
    def user_id(self) -> user.Id:
        return self._user_id

    @property
    def keywords(self) -> list[Keyword]:
        return self._keywords

    @property
    def requested_at(self) -> datetime:
        return self._requested_at

    @property
    def generated_post_id(self) -> post.Id | None:
        return self._generated_post_id

    @property
    def generation_status(self) -> GenerationStatus:
        if self._generated_post_id is None:
            return GenerationStatus.UNCOMPLETED
        else:
            return GenerationStatus.COMPLETED


def create_post_generate_request_id(
    id: Id, user_id: user.Id, keywords: list[Keyword], now: datetime
) -> PostGenerateRequest:
    return PostGenerateRequest(id, user_id, keywords, now, None)
