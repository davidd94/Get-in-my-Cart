from threading import Thread
from threading import current_thread
from asyncio import Future
import asyncio
import time


async def asleep(sleep_for):
   future = Future()
   current_loop = asyncio.get_event_loop()
   Thread(target=sync_sleep, args=(sleep_for, future, current_loop)).start()

   await future


def sync_sleep(sleep_for, future, loop):
   # sleep synchronously
   time.sleep(sleep_for)

   # define a nested coroutine to resolve the future
   async def sleep_future_resolver():
       # resolve the future
       future.set_result(None)

   asyncio.run_coroutine_threadsafe(sleep_future_resolver(), loop)
   print("Sleeping completed in {0}\n".format(current_thread().getName()), flush=True)


if __name__ == "__main__":
   start = time.time()
   work = list()
   work.append(asleep(5))
   work.append(asleep(5))
   work.append(asleep(5))
   work.append(asleep(5))
   work.append(asleep(5))

   loop = asyncio.get_event_loop()
   loop.run_until_complete(asyncio.wait(work, return_when=asyncio.ALL_COMPLETED))
   print("main program exiting after running for {0}".format(time.time() - start))