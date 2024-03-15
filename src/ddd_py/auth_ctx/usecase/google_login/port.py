import abc

from .dto import IdpTokenResponse


class Port(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def code2token(self, code: str) -> IdpTokenResponse:
        pass
