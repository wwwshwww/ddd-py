import abc


class Port(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def call_token_endpoint(self, code: str):
        pass
