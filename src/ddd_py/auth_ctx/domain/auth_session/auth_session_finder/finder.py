import abc

from ddd_py.auth_ctx.domain.auth_session import auth_session

from .filtering_options import FilteringOptions


class Finder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find(self, filtering_options: FilteringOptions = None) -> list[auth_session.Id]:
        raise NotImplementedError()
