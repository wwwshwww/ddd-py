from dataclasses import dataclass

from ddd_py.app_ctx.usecase import (
    find_post,
    find_post_generate_request,
    find_reaction,
    find_reaction_preset,
    find_user,
    retrieve_user,
)


@dataclass
class Dependencies:
    usecase_find_post: find_post.Usecase
    usecase_find_post_generate_request: find_post_generate_request.Usecase
    usecase_find_reaction: find_reaction.Usecase
    usecase_find_reaction_preset: find_reaction_preset.Usecase
    usecase_find_user: find_user.Usecase

    usecase_retrieve_user: retrieve_user.Usecase
