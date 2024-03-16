from typing import Tuple

from ddd_py.common import transaction_manager as tm


class SampleRepo:
    def __init__(self, db: str) -> None:
        self.db = db

    def get(self, i: int) -> str:
        if i < 1:
            raise ValueError("error")
        return "a" * i


class SampleUsecase:
    def __init__(self, repo: SampleRepo):
        self.repo = repo

    def get(self, i: int) -> str:
        try:
            return self.repo.get(i)
        except Exception as e:
            raise ValueError("usecase error") from e


class SampleTransactionSlave(tm.TransactionSlave):
    def __init__(self, db: str) -> None:
        self.db = db

    async def begin(self):
        pass

    async def commit(self):
        pass

    async def rollback(self):
        pass


def new_usecase() -> Tuple[SampleUsecase, SampleTransactionSlave]:
    tx_slave_1 = SampleTransactionSlave("db_connection")
    uc = SampleUsecase(SampleRepo("db_connection"))

    return uc, tx_slave_1


def get_adapter(id: int):
    return


# class SampleAdapter:
#     def __init__(self, new_usecase: Callable[[], SampleUsecase]):
#         self.new_usecase = new_usecase

#     def get(self):
#         try:
#             usecase = self.new_usecase()
#             result = usecase.get()
#             print(result)
#         except Exception as e:
#             raise ValueError("example error") from e


# def example():
#     transaction_manager = {}

#     def nu() -> SampleUsecase:
#         tx_slave_1 = SampleTransactionSlave("db_connection")
#         return SampleUsecase(SampleRepo("db_connection"))

#     adapter = SampleAdapter(nu)


# example()
