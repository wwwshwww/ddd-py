import enum
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: str
    name: str


@dataclass(frozen=True)
class Post:
    id: str
    content: str
    creator_id: str


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class Reaction:
    id: str
    reaction_preset_id: str
    target_post_id: str
    reactor_id: str
    reacted_at: str
    is_approved: bool


@dataclass(frozen=True)
class ReactionPreset:
    id: str
    content: str
    created_at: str
    creator_id: str


@dataclass(frozen=True)
class Page:
    offset: int
    limit: int | None = None


@dataclass(frozen=True)
class UserFilteringOptions:
    name_exact: str | None = None
    name_front: str | None = None
    name_partial: str | None = None
    name_back: str | None = None


# TODO: oneOf ディレクティブの制約を実装するかどうか検討する
@dataclass(frozen=True)
class UserSortingOption:
    name_asc: bool | None = None
    get_reaction_num_asc: bool | None = None
    give_reaction_num_asc: bool | None = None


@dataclass(frozen=True)
class PostFilteringOptions:
    creator_ids: tuple[str] | None = None
    reaction_num_more: int | None = None
    reaction_num_less: int | None = None


# TODO: oneOf ディレクティブの制約を実装するかどうか検討する
@dataclass(frozen=True)
class PostSortingOption:
    id_asc: bool | None = None
    reaction_num_asc: bool | None = None
    creator_id_asc: bool | None = None
    created_at_asc: bool | None = None
