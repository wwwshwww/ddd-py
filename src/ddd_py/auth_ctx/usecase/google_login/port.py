from abc import ABCMeta, abstractmethod

from .dto import IdpTokenResponse


class Port(metaclass=ABCMeta):
    @abstractmethod
    def code2token(self, code: str) -> IdpTokenResponse:
        pass
