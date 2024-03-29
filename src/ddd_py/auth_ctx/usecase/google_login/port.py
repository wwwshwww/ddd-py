from abc import ABC, abstractmethod

from .dto import IdpTokenResponse


class Port(ABC):
    @abstractmethod
    def code2token(self, code: str) -> IdpTokenResponse:
        pass
