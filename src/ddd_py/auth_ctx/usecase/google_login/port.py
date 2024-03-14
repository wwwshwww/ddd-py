import abc

from .dto import TokenRequest


class Port(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def call_token_endpoint(self, request: TokenRequest):
        pass
