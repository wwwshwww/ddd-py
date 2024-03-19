import asyncio


class A:
    async def call(self, i: int):
        await asyncio.sleep(0.5)
        print(f"call {i}")


async def aa() -> str:
    a = A()
    tasks = [a.call(i) for i in range(10)]
    await asyncio.gather(*tasks)
    return "123"


async def hello():
    print("hello")
    await asyncio.sleep(1)
    print("world")


async def call_hello():
    await hello()


def main():
    print("start")
    out = asyncio.run(aa())
    print(f"result: {out}")


main()
