.. meta::
    :description lang=en: Python multiprocessing tutorial covering process creation, pools, shared memory, inter-process communication, and parallel CPU-bound task execution
    :keywords: Python, Python3, multiprocessing, Process, Pool, Queue, Pipe, shared memory, parallel, CPU-bound, GIL bypass

===============
Multiprocessing
===============

:Source: `src/basic/concurrency_.py <https://github.com/crazyguitar/pysheeet/blob/master/src/basic/concurrency_.py>`_

.. contents:: Table of Contents
    :backlinks: none

Introduction
------------

The ``multiprocessing`` module enables true parallel execution by spawning
separate Python processes, each with its own Python interpreter and memory
space. Unlike threads, processes bypass the Global Interpreter Lock (GIL),
making multiprocessing ideal for CPU-bound tasks that need to utilize multiple
CPU cores. The trade-off is higher overhead for process creation and
inter-process communication compared to threads.

Creating Processes
------------------

Creating processes is similar to creating threads. Each process runs in its
own memory space, so changes to variables in one process don't affect others.
Use ``start()`` to begin execution and ``join()`` to wait for completion.

.. code-block:: python

    from multiprocessing import Process
    import os

    def worker(name):
        print(f"Worker {name}, PID: {os.getpid()}")

    if __name__ == "__main__":
        processes = []
        for i in range(4):
            p = Process(target=worker, args=(i,))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        print(f"Main process PID: {os.getpid()}")

Process Pool
------------

A ``Pool`` manages a collection of worker processes and distributes tasks among
them. This is more efficient than creating a new process for each task, as
processes are reused. The pool provides methods like ``map()``, ``apply()``,
and their async variants for different use cases.

.. code-block:: python

    from multiprocessing import Pool
    import time

    def cpu_intensive(n):
        """Simulate CPU-bound work."""
        total = 0
        for i in range(n):
            total += i * i
        return total

    if __name__ == "__main__":
        numbers = [10**6, 10**6, 10**6, 10**6]

        # Sequential execution
        start = time.time()
        results = [cpu_intensive(n) for n in numbers]
        print(f"Sequential: {time.time() - start:.2f}s")

        # Parallel execution with Pool
        start = time.time()
        with Pool(4) as pool:
            results = pool.map(cpu_intensive, numbers)
        print(f"Parallel: {time.time() - start:.2f}s")

Pool Methods
------------

The Pool class provides several methods for distributing work. ``map()`` applies
a function to each item in an iterable and returns results in order. ``apply()``
calls a function with arguments and blocks until complete. The ``_async``
variants return immediately with an ``AsyncResult`` object.

.. code-block:: python

    from multiprocessing import Pool

    def square(x):
        return x * x

    def add(a, b):
        return a + b

    if __name__ == "__main__":
        with Pool(4) as pool:
            # map - apply function to iterable
            results = pool.map(square, range(10))
            print(f"map: {results}")

            # starmap - unpack arguments from iterable
            pairs = [(1, 2), (3, 4), (5, 6)]
            results = pool.starmap(add, pairs)
            print(f"starmap: {results}")

            # apply_async - non-blocking single call
            result = pool.apply_async(square, (10,))
            print(f"apply_async: {result.get()}")

            # map_async - non-blocking map
            result = pool.map_async(square, range(5))
            print(f"map_async: {result.get()}")

Sharing Data with Queue
-----------------------

Processes don't share memory by default. ``multiprocessing.Queue`` provides a
thread and process-safe way to exchange data between processes. It's the
recommended approach for most inter-process communication scenarios.

.. code-block:: python

    from multiprocessing import Process, Queue

    def producer(q, items):
        for item in items:
            q.put(item)
            print(f"Produced: {item}")
        q.put(None)  # Sentinel

    def consumer(q):
        while True:
            item = q.get()
            if item is None:
                break
            print(f"Consumed: {item}")

    if __name__ == "__main__":
        q = Queue()
        items = list(range(5))

        p1 = Process(target=producer, args=(q, items))
        p2 = Process(target=consumer, args=(q,))

        p1.start()
        p2.start()
        p1.join()
        p2.join()

Sharing Data with Pipe
----------------------

A ``Pipe`` creates a two-way communication channel between two processes. It's
simpler and faster than Queue for point-to-point communication but only
supports two endpoints. Each end can send and receive data.

.. code-block:: python

    from multiprocessing import Process, Pipe

    def sender(conn):
        conn.send("Hello from sender")
        conn.send([1, 2, 3])
        response = conn.recv()
        print(f"Sender received: {response}")
        conn.close()

    def receiver(conn):
        msg = conn.recv()
        print(f"Receiver got: {msg}")
        data = conn.recv()
        print(f"Receiver got: {data}")
        conn.send("Thanks!")
        conn.close()

    if __name__ == "__main__":
        parent_conn, child_conn = Pipe()

        p1 = Process(target=sender, args=(parent_conn,))
        p2 = Process(target=receiver, args=(child_conn,))

        p1.start()
        p2.start()
        p1.join()
        p2.join()

Shared Memory with Value and Array
----------------------------------

For simple shared state, ``Value`` and ``Array`` provide shared memory that
multiple processes can access. These are faster than Queue/Pipe for frequently
accessed data but require careful synchronization to avoid race conditions.

.. code-block:: python

    from multiprocessing import Process, Value, Array

    def increment(counter, lock_needed=True):
        for _ in range(10000):
            with counter.get_lock():
                counter.value += 1

    def modify_array(arr):
        for i in range(len(arr)):
            arr[i] = arr[i] * 2

    if __name__ == "__main__":
        # Shared integer
        counter = Value('i', 0)  # 'i' = signed int
        processes = [Process(target=increment, args=(counter,)) for _ in range(4)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        print(f"Counter: {counter.value}")  # 40000

        # Shared array
        arr = Array('d', [1.0, 2.0, 3.0, 4.0])  # 'd' = double
        p = Process(target=modify_array, args=(arr,))
        p.start()
        p.join()
        print(f"Array: {list(arr)}")  # [2.0, 4.0, 6.0, 8.0]

Manager for Complex Shared Objects
----------------------------------

A ``Manager`` provides a way to share more complex Python objects (lists, dicts)
between processes. The manager runs a server process that holds the actual
objects, and other processes access them through proxies. This is slower than
Value/Array but supports arbitrary Python objects.

.. code-block:: python

    from multiprocessing import Process, Manager

    def worker(shared_dict, shared_list, worker_id):
        shared_dict[worker_id] = worker_id * 10
        shared_list.append(worker_id)

    if __name__ == "__main__":
        with Manager() as manager:
            shared_dict = manager.dict()
            shared_list = manager.list()

            processes = []
            for i in range(4):
                p = Process(target=worker, args=(shared_dict, shared_list, i))
                processes.append(p)
                p.start()

            for p in processes:
                p.join()

            print(f"Dict: {dict(shared_dict)}")
            print(f"List: {list(shared_list)}")

Process Synchronization
-----------------------

Multiprocessing provides the same synchronization primitives as threading:
``Lock``, ``RLock``, ``Semaphore``, ``Event``, ``Condition``, and ``Barrier``.
These work across processes instead of threads.

.. code-block:: python

    from multiprocessing import Process, Lock, Value

    def safe_increment(counter, lock):
        for _ in range(10000):
            with lock:
                counter.value += 1

    if __name__ == "__main__":
        lock = Lock()
        counter = Value('i', 0)

        processes = [
            Process(target=safe_increment, args=(counter, lock))
            for _ in range(4)
        ]

        for p in processes:
            p.start()
        for p in processes:
            p.join()

        print(f"Counter: {counter.value}")  # 40000

Daemon Processes
----------------

Like daemon threads, daemon processes are terminated when the main process
exits. They're useful for background tasks that shouldn't prevent program
termination. Set ``daemon=True`` before calling ``start()``.

.. code-block:: python

    from multiprocessing import Process
    import time

    def background_task():
        while True:
            print("Background process running...")
            time.sleep(1)

    if __name__ == "__main__":
        p = Process(target=background_task, daemon=True)
        p.start()

        time.sleep(3)
        print("Main process exiting, daemon will be terminated")

Handling Process Termination
----------------------------

Processes can be terminated gracefully using ``terminate()`` or forcefully
using ``kill()``. Always clean up resources properly and consider using
signals for graceful shutdown in production code.

.. code-block:: python

    from multiprocessing import Process
    import time
    import signal

    def long_running_task():
        try:
            while True:
                print("Working...")
                time.sleep(1)
        except KeyboardInterrupt:
            print("Graceful shutdown")

    if __name__ == "__main__":
        p = Process(target=long_running_task)
        p.start()

        time.sleep(3)

        # Graceful termination (SIGTERM)
        p.terminate()
        p.join(timeout=2)

        # Force kill if still alive
        if p.is_alive():
            p.kill()
            p.join()

        print(f"Exit code: {p.exitcode}")

ProcessPoolExecutor
-------------------

``concurrent.futures.ProcessPoolExecutor`` provides a higher-level interface
for process pools that's consistent with ``ThreadPoolExecutor``. It's often
easier to use than ``multiprocessing.Pool`` and integrates well with the
futures pattern.

.. code-block:: python

    from concurrent.futures import ProcessPoolExecutor, as_completed

    def compute(n):
        return sum(i * i for i in range(n))

    if __name__ == "__main__":
        numbers = [10**6, 10**6, 10**6, 10**6]

        with ProcessPoolExecutor(max_workers=4) as executor:
            # Submit individual tasks
            futures = [executor.submit(compute, n) for n in numbers]

            # Process results as they complete
            for future in as_completed(futures):
                print(f"Result: {future.result()}")

            # Or use map for ordered results
            results = list(executor.map(compute, numbers))
            print(f"All results: {results}")

Comparing Threads vs Processes
------------------------------

Choose threads for I/O-bound tasks (network, file I/O) where the GIL is
released during waiting. Choose processes for CPU-bound tasks that need true
parallelism. This example demonstrates the performance difference.

.. code-block:: python

    from threading import Thread
    from multiprocessing import Process, Pool
    import time

    def cpu_bound(n):
        """CPU-intensive task."""
        return sum(i * i for i in range(n))

    if __name__ == "__main__":
        n = 10**7
        count = 4

        # Sequential
        start = time.time()
        for _ in range(count):
            cpu_bound(n)
        print(f"Sequential: {time.time() - start:.2f}s")

        # Threads (limited by GIL)
        start = time.time()
        threads = [Thread(target=cpu_bound, args=(n,)) for _ in range(count)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        print(f"Threads: {time.time() - start:.2f}s")

        # Processes (true parallelism)
        start = time.time()
        with Pool(count) as pool:
            pool.map(cpu_bound, [n] * count)
        print(f"Processes: {time.time() - start:.2f}s")
