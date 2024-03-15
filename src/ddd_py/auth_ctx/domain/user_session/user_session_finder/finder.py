import abc
from ast import List

from ddd_py.auth_ctx.domain.user_session import user_session

from .filtering_options import FilteringOptions


class Finder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find(self, filtering_options: FilteringOptions = None) -> List[user_session.Id]:
        raise NotImplementedError()
