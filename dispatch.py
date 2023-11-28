import asyncio

async def handler(waiter, msg):
    print(msg)
    print(await waiter)
    print(await waiter)

async def test():
    dispatcher = Dispatcher()
    for key, message in [
        (1, "a"),
        (2, "b"),
        (1, "c"),
        (2, "d"),
        (1, "e"),
        (2, "f"),
    ]:
        asyncio.create_task(
            dispatcher.dispatch(
                key, message, handler
            )
        )

class Waiter:

    def __init__(self):
        self._queue = []

    async def _wait(self):
        while True:
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

loop = asyncio.new_event_loop()
loop.run_until_complete(test())
