import asyncio


async def producer(queue: asyncio.Queue):
    for i in range(5):
        await asyncio.sleep(1)
        await queue.put(f"item {i}")
        print(f"Produced item {i}")
    await queue.put(None)  # 終了の合図


async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Consumed {item}")
        queue.task_done()


async def main():
    queue: asyncio.Queue = asyncio.Queue()
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))
    await producer_task
    await consumer_task


asyncio.run(main())
