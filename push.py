import asyncio

class Waiter:
    def __await__(self):
        yield from ["abc"]

async def b(waiter):
    await waiter
    raise Exception()

async def a(waiter):
    print(123, end=" -> ")
    await waiter
    print(456, end=" -> ")
    await asyncio.sleep(0)
    print(789, end=" -> ")
    await waiter
    print(0, end=" -> ")
    await b(waiter)
    print(1, end=" -> ")

coro = a(Waiter())
while True:
    try:
        print(coro.send(None))
    except StopIteration:
        break
