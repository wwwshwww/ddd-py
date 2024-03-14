from datetime import datetime

from ddd_py.app_ctx.domain.post import post
from ddd_py.app_ctx.domain.reaction_preset import reaction_preset
from ddd_py.app_ctx.domain.user import user

from .id import Id


class Reaction:
    def __init__(
        self,
        id: Id,
        reaction_preset_id: reaction_preset.Id,
        post_id: post.Id,
        user_id: user.Id,
        reacted_at: datetime,
        is_approved: bool,
    ) -> None:
        self._id = id
        self._reaction_preset_id = reaction_preset_id
        self._post_id = post_id
        self._user_id = user_id
        self._reacted_at = reacted_at
        self._is_approved = is_approved

    @property
    def id(self) -> Id:
        return self._id

    @property
    def reaction_preset_id(self) -> reaction_preset.Id:
        return self._reaction_preset_id

    @property
    def post_id(self) -> post.Id:
        return self._post_id

    @property
    def user_id(self) -> user.Id:
        return self._user_id

    @property
    def reacted_at(self) -> datetime:
        return self._reacted_at

    @property
    def is_approved(self) -> bool:
        return self._is_approved

    def approve(self) -> None:
        self._is_approved = True

    def disapprove(self) -> None:
        self._is_approved = False
