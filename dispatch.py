import asyncio
from functools import partial

async def handler(key, waiter, msg):
    print(key, msg)
    print(key, await waiter)
    print(key, await waiter)

async def simulate_messages_coming_in():
    dispatcher = Dispatcher()
    tasks = []
    for index, (key, message) in enumerate([
        (1, "a"),
        (2, "b"),
        (1, "c"),
        (2, "d"),
        (1, "e"),
        (2, "f"),
    ]):
        async def task(number, key, message):
            await asyncio.sleep((number ** 2) / 5)
            await dispatcher.dispatch(
                key, message, partial(handler, key)
            )
        tasks.append(task(index + 1, key, message))
    await asyncio.gather(*tasks)

class Waiter:

    def __init__(self):
        self._queue = []
        self._polls_amt = 0

    async def _wait(self):
        while True:
            self._polls_amt += 1
            if self._queue:
                item, *self._queue = self._queue
                return item
            await asyncio.sleep(0)

    def __await__(self):
        return self._wait().__await__()

class Dispatcher:

    def __init__(self):
        self._waiters = {}

    async def dispatch(self, key, message, handler):
        try:
            waiter = self._waiters[key]
        except KeyError:
            waiter = Waiter()
            self._waiters[key] = waiter
            await handler(waiter, message)
        else:
            waiter._queue.append(message)
        print("Polls amount:", waiter._polls_amt, "(horrible, right?)")

asyncio.run(simulate_messages_coming_in())
