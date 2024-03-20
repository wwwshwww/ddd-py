import asyncio
from contextvars import ContextVar

my_var: ContextVar[int] = ContextVar("my_var")

my_var.set(100)
print(my_var.get())  # 100


async def task():
    my_var.set(123)
    print(f"task: {my_var.get()}")
    taskk()


def taskk():
    print(f"taskk: {my_var.get()}")


if __name__ == "__main__":
    asyncio.run(task())
    print(my_var.get())
