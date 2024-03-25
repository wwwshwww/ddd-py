from .id import Id


class DomainError(Exception): ...


class RepositoryGetError(Exception):
    def __init__(self, message, notfound_ids: list[Id]) -> None:
        super().__init__(message)
        self.notfound_ids = notfound_ids


class RepositorySaveError(Exception): ...


class RepositoryDeleteError(Exception): ...
