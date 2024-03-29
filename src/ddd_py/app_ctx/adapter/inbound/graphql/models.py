import enum
from dataclasses import dataclass

from ariadne import EnumType, InputType, ObjectType


@dataclass
class User:
    id: str
    name: str


user = ObjectType("User")


@dataclass
class Post:
    id: str
    content: str
    creator_id: str


post = ObjectType("Post")


@dataclass
class PostGenerateRequest:
    id: str
    creator_id: str
    keywords: list[str]
    generation_status: "PostGenerateRequestGenStatus"
    requested_at: str
    generated_post_id: str | None


post_generate_request = ObjectType("PostGenerateRequest")


class PostGenerateRequestGenStatus(enum.Enum):
    UNCOMPLETED = 1
    COMPLETED = 2


post_generate_request_gen_status = EnumType(
    "PostGenerateRequestGenStatus", PostGenerateRequestGenStatus
)


@dataclass
class Reaction:
    id: str
    reaction_preset_id: str
    target_post_id: str
    reactor_id: str
    reacted_at: str
    is_approved: bool


reaction = ObjectType("Reaction")


@dataclass
class ReactionPreset:
    id: str
    content: str
    created_at: str
    creator_id: str


reaction_preset = ObjectType("ReactionPreset")


@dataclass
class Page:
    offset: int
    limit: int | None


page = InputType("Page", lambda x: Page(**x))


@dataclass
class UserFilteringOptions:
    name_exact: str | None
    name_front: str | None
    name_partial: str | None
    name_back: str | None


user_filtering_options = InputType(
    "UserFilteringOptions", lambda x: UserFilteringOptions(**x)
)


class UserSortingType(enum.Enum):
    NAME = 1
    GET_REACTION_NUM = 2
    GIVE_REACTION_NUM = 3


user_sorting_type = EnumType("UserSortingType", UserSortingType)


@dataclass
class UserSortingOption:
    type: UserSortingType
    asc: bool


user_sorting_option = InputType("UserSortingOption", lambda x: UserSortingOption(**x))


@dataclass
class PostFilteringOptions:
    creator_ids: list[str] | None
    reaction_num_more: int | None
    reaction_num_less: int | None


post_filtering_options = InputType(
    "PostFilteringOptions", lambda x: PostFilteringOptions(**x)
)


class PostSortingType(enum.Enum):
    ID = 1
    REACTION_NUM = 2
    CREATOR_ID = 3
    CREATED_AT = 4


post_sorting_type = EnumType("PostSortingType", PostSortingType)


@dataclass
class PostSortingOption:
    type: PostSortingType
    asc: bool


post_sorting_option = InputType("PostSortingOption", lambda x: PostSortingOption(**x))
