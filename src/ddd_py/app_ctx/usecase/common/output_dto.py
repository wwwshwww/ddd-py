from dataclasses import dataclass

from ddd_py.app_ctx.domain.post import post
from ddd_py.app_ctx.domain.post_generate_request import post_generate_request
from ddd_py.app_ctx.domain.reaction import reaction
from ddd_py.app_ctx.domain.reaction_preset import reaction_preset
from ddd_py.app_ctx.domain.user import user


@dataclass
class PostDTO:
    id: post.Id
    content: str
    user_id: user.Id


@dataclass
class PostGenerateRequestDTO:
    id: post_generate_request.Id


@dataclass
class ReactionDTO:
    id: reaction.Id


@dataclass
class ReactionPresetDTO:
    id: reaction_preset.Id


@dataclass
class UserDTO:
    id: user.Id
