import asyncio
from functools import partial
from typing import Any, Dict

async def handler(key, waiter, message):
    print(key, message)
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
        (2, "g"),
        (2, "h"),
        (2, "i"),
    ]):
        async def task(index, key, message):
            await asyncio.sleep(index)
            await dispatcher.dispatch(
                key, message, partial(handler, key)
            )
        tasks.append(task(index, key, message))
    await asyncio.gather(*tasks)

class Waiter:

    def __init__(self):
        self._queue = []
        self._event = asyncio.Event()

    async def _wait(self):
        await self._event.wait()
        item, *self._queue = self._queue
        if not self._queue:
            self._event.clear()
        return item

    def __await__(self):
        return self._wait().__await__()

class Dispatcher:

    def __init__(self):
        self._waiters: Dict[Any, Waiter] = {}

    async def dispatch(self, key, message, handler):
        try:
            waiter = self._waiters[key]
        except KeyError:
            waiter = Waiter()
            self._waiters[key] = waiter

            async def wrapped_handler():
                try:
                    return await handler(waiter, message)
                finally:
                    if not waiter._queue:
                        del self._waiters[key]

            return await wrapped_handler()
        else:
            waiter._queue.append(message)
            waiter._event.set()

asyncio.run(simulate_messages_coming_in())
