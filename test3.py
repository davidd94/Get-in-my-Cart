from threading import Thread
from threading import current_thread
import time


def sync_sleep(sleep_for):
   time.sleep(sleep_for)
   print("Sleeping completed in {0}".format(current_thread().getName()))


if __name__ == "__main__":
   start = time.time()

   threads = list()

   for _ in range(0, 5):
       threads.append(Thread(target=sync_sleep, args=(5,)))

   for thread in threads:
       thread.start()

   for thread in threads:
       thread.join()

   print("main program exiting after running for {0}".format(time.time() - start))