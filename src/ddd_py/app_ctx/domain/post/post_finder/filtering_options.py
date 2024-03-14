from dataclasses import dataclass
from typing import Optional


@dataclass
class FilteringOptions:
    reaction_num_more: Optional[int] = None
    reaction_num_less: Optional[int] = None
    # TODO: add option that number of specific reactions
    # specific_reaction_num_more: Optional[Tuple(reaction.Type, int)] = None
