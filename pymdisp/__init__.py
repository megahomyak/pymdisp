import asyncio

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
        self._waiters = {}

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
