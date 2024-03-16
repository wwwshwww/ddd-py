import asyncio


class A:
    async def call(self, i: int):
        await asyncio.sleep(0.5)
        print(f"call {i}")


async def aa():
    a = A()
    tasks = [a.call(i) for i in range(10)]
    await asyncio.gather(*tasks)


async def hello():
    print("hello")
    await asyncio.sleep(1)
    print("world")


async def call_hello():
    await hello()


asyncio.run(aa())
