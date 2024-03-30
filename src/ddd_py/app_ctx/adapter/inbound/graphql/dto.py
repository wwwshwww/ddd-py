import enum
from dataclasses import dataclass


@dataclass
class User:
    id: str
    name: str


@dataclass
class Post:
    id: str
    content: str
    creator_id: str


@dataclass
class PostGenerateRequest:
    id: str
    creator_id: str
    keywords: list[str]
    generation_status: "PostGenerateRequestGenStatus"
    requested_at: str
    generated_post_id: str | None


class PostGenerateRequestGenStatus(enum.Enum):
    UNCOMPLETED = 1
    COMPLETED = 2


@dataclass
class Reaction:
    id: str
    reaction_preset_id: str
    target_post_id: str
    reactor_id: str
    reacted_at: str
    is_approved: bool


@dataclass
class ReactionPreset:
    id: str
    content: str
    created_at: str
    creator_id: str


@dataclass
class Page:
    offset: int
    limit: int | None


@dataclass
class UserFilteringOptions:
    name_exact: str | None
    name_front: str | None
    name_partial: str | None
    name_back: str | None


class UserSortingType(enum.Enum):
    NAME = 1
    GET_REACTION_NUM = 2
    GIVE_REACTION_NUM = 3


@dataclass
class UserSortingOption:
    type: UserSortingType
    asc: bool


@dataclass
class PostFilteringOptions:
    creator_ids: list[str] | None
    reaction_num_more: int | None
    reaction_num_less: int | None


class PostSortingType(enum.Enum):
    ID = 1
    REACTION_NUM = 2
    CREATOR_ID = 3
    CREATED_AT = 4


@dataclass
class PostSortingOption:
    type: PostSortingType
    asc: bool
