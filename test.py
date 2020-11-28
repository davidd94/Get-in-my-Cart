import asyncio
from asyncio import Future


async def test(future, count):
    print("sleeping test 1...")
    while count < 2:
        print("retry test 1...")
        print(f"test count: {count}")
        count += 1
        await asyncio.sleep(2)
    print("finished test 1...")

async def test2(future):
    print("sleeping test 2...")

    await asyncio.sleep(20)
    print("finished test 2...")
    # future.done()
    # future.set_result(None)

async def bar(future, count):
    print("bar will sleep for 3 seconds")
    while count < 3:
        print("bar idling for 3 seconds....")
        print(f"bar count: {count}")
        count += 1
        await asyncio.sleep(3)
    print("bar resolving the future")
    future.done()
    future.set_result("future is resolved")


async def foo(future):
    print("foo will await the future")
    await future
    print("foo finds the future resolved")


async def main():
    future = Future()
    count = 0

    loop = asyncio.get_event_loop()
    t3 = loop.create_task(test(future, count))
    t2 = loop.create_task(foo(future))
    t1 = loop.create_task(bar(future, count))
    t4 = loop.create_task(test2(future))

    await t3, t2, t1, t4


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("main exiting")

    # resume any uncompleted tasks
    pending = asyncio.all_tasks()
    loop.run_until_complete(asyncio.gather(*pending))