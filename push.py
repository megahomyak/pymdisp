import asyncio

# THIS DOES NOT WORK AT THE MOMENT, LOOK AT THE PREVIOUS COMMIT, I AM EXPERIMENTING HERE!

class Waiter:
    def __await__(self):
        while True:
            yield self
        return "message"

async def b(waiter):
    print("e", await waiter)

async def a(waiter):
    print(123, end=" -> ")
    print("a", await waiter)
    print(456, end=" -> ")
    print("b", await asyncio.sleep(0))
    print(789, end=" -> ")
    print("c", await waiter)
    print(0, end=" -> ")
    print("d", await b(waiter))
    print(1)

coro = a(Waiter())
while True:
    try:
        print(coro.send(None))
    except StopIteration:
        break
