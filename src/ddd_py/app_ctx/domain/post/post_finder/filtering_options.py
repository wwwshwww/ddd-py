from dataclasses import dataclass

from ddd_py.app_ctx.domain.user import user


@dataclass
class FilteringOptions:
    user_id_in: list[user.Id] | None = None
    reaction_num_more: int | None = None
    reaction_num_less: int | None = None
    # TODO: add option that number of specific reactions
    # specific_reaction_num_more: Optional[Tuple(reaction.Type, int)] = None
