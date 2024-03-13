import abc
from ast import List

from .filtering_options import FilteringOptions

from ddd_py.app_ctx.domain.user import user

class Finder(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def Find(self, filtering_options: FilteringOptions=None) -> List[user.Id]:
        raise NotImplementedError()
    