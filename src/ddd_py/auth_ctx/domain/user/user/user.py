from .google_profile import GoogleProfile
from .id import Id


class User:
    def __init__(self, id: Id, google_profile: GoogleProfile):
        self._id = id
        self._google_profile = google_profile

    @property
    def id(self) -> Id:
        return self._id

    @property
    def google_profile(self) -> GoogleProfile:
        return self._google_profile
