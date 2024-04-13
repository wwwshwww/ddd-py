from abc import ABCMeta, abstractmethod

from .dto import IdpTokenResponse


class Port(metaclass=ABCMeta):
    @abstractmethod
    async def code2token(self, code: str) -> IdpTokenResponse:
        pass
