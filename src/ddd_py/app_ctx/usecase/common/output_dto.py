from dataclasses import dataclass

from ddd_py.app_ctx.domain.post import post
from ddd_py.app_ctx.domain.post_generate_request import post_generate_request
from ddd_py.app_ctx.domain.reaction import reaction
from ddd_py.app_ctx.domain.reaction_preset import reaction_preset
from ddd_py.app_ctx.domain.user import user


@dataclass
class Post:
    id: post.Id


@dataclass
class PostGenerateRequest:
    id: post_generate_request.Id


@dataclass
class Reaction:
    id: reaction.Id


@dataclass
class ReactionPreset:
    id: reaction_preset.Id


@dataclass
class User:
    id: user.Id
