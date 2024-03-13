
from .id import Id
from .google_profile import GoogleProfile

class User():
    def __init__(self, id: Id, google_profile: GoogleProfile):
        self._id = id
        self._google_profile = google_profile
