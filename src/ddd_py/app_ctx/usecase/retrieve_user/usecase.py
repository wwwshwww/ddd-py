from abc import ABCMeta, abstractmethod

from ddd_py.app_ctx.domain.user import user
from ddd_py.app_ctx.usecase.common import output_dto


class Usecase(metaclass=ABCMeta):
    @abstractmethod
    async def retrieve_by_ids(
        self,
        ids: list[user.Id],
    ) -> list[output_dto.UserDTO]:
        pass
