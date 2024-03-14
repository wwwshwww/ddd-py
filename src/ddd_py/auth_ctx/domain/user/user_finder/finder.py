import abc
from ast import List

from ddd_py.app_ctx.domain.user import user

from .filtering_options import FilteringOptions


class Finder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find(self, filtering_options: FilteringOptions = None) -> List[user.Id]:
        raise NotImplementedError()
