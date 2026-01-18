.. meta::
    :description lang=en: Python threading tutorial covering thread creation, synchronization primitives, locks, semaphores, events, conditions, and thread-safe data structures
    :keywords: Python, Python3, threading, Thread, Lock, RLock, Semaphore, Event, Condition, synchronization, GIL, concurrent, parallel

=========
Threading
=========

:Source: `src/basic/concurrency_.py <https://github.com/crazyguitar/pysheeet/blob/master/src/basic/concurrency_.py>`_

.. contents:: Table of Contents
    :backlinks: none

Introduction
------------

The ``threading`` module provides a high-level interface for creating and
managing threads in Python. Threads are lightweight units of execution that
share the same memory space within a process, making them efficient for I/O-bound
tasks where the program spends time waiting for external resources. However,
due to Python's Global Interpreter Lock (GIL), threads cannot achieve true
parallelism for CPU-bound tasks—only one thread can execute Python bytecode
at a time. For CPU-intensive work, consider using ``multiprocessing`` instead.

Creating Threads
----------------

There are two primary ways to create threads: subclassing ``Thread`` or passing
a target function. The function-based approach is more flexible and commonly
used, while subclassing is useful when you need to encapsulate thread state
and behavior in a class.

.. code-block:: python

    from threading import Thread

    # Method 1: Subclass Thread
    class Worker(Thread):
        def __init__(self, worker_id):
            super().__init__()
            self.worker_id = worker_id

        def run(self):
            print(f"Worker {self.worker_id} running")

    # Method 2: Pass target function (preferred)
    def task(worker_id):
        print(f"Task {worker_id} running")

    # Using subclass
    t1 = Worker(1)
    t1.start()
    t1.join()

    # Using target function
    t2 = Thread(target=task, args=(2,))
    t2.start()
    t2.join()

Thread with Return Value
------------------------

Threads don't directly return values from their target functions. To get results
back, you can use shared mutable objects, queues, or store results as instance
attributes when subclassing Thread.

.. code-block:: python

    from threading import Thread
    from queue import Queue

    def compute(n, results):
        """Store result in shared dict."""
        results[n] = n * n

    # Using shared dictionary
    results = {}
    threads = []
    for i in range(5):
        t = Thread(target=compute, args=(i, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(results)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

    # Using Queue (thread-safe)
    def compute_queue(n, q):
        q.put((n, n * n))

    q = Queue()
    threads = []
    for i in range(5):
        t = Thread(target=compute_queue, args=(i, q))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    while not q.empty():
        n, result = q.get()
        print(f"{n}: {result}")

Daemon Threads
--------------

Daemon threads run in the background and are automatically terminated when all
non-daemon threads have finished. They're useful for background tasks that
shouldn't prevent the program from exiting, such as monitoring or cleanup tasks.

.. code-block:: python

    from threading import Thread
    import time

    def background_task():
        while True:
            print("Background task running...")
            time.sleep(1)

    # Daemon thread - won't prevent program exit
    t = Thread(target=background_task, daemon=True)
    t.start()

    # Main thread work
    time.sleep(3)
    print("Main thread done, daemon will be killed")

Lock - Mutual Exclusion
-----------------------

A ``Lock`` is the simplest synchronization primitive that prevents multiple
threads from accessing a shared resource simultaneously. Always use locks when
modifying shared state to prevent race conditions. The context manager syntax
(``with lock:``) is preferred as it guarantees the lock is released even if
an exception occurs.

.. code-block:: python

    from threading import Thread, Lock

    counter = 0
    lock = Lock()

    def increment(n):
        global counter
        for _ in range(n):
            with lock:  # Acquire and release automatically
                counter += 1

    threads = [Thread(target=increment, args=(100000,)) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Counter: {counter}")  # Always 500000 with lock

RLock - Reentrant Lock
----------------------

An ``RLock`` (reentrant lock) can be acquired multiple times by the same thread
without causing a deadlock. This is essential when a thread needs to call
methods that also acquire the same lock, such as in recursive functions or
when methods call other methods on the same object.

.. code-block:: python

    from threading import Thread, RLock

    class Counter:
        def __init__(self):
            self.value = 0
            self.lock = RLock()

        def increment(self):
            with self.lock:
                self.value += 1

        def increment_twice(self):
            with self.lock:  # First acquisition
                self.increment()  # Second acquisition - OK with RLock
                self.increment()

    counter = Counter()
    threads = [Thread(target=counter.increment_twice) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Value: {counter.value}")  # 200

Semaphore - Resource Limiting
-----------------------------

A ``Semaphore`` limits the number of threads that can access a resource
concurrently. Unlike a lock which allows only one thread, a semaphore with
count N allows up to N threads to proceed. This is useful for connection pools,
rate limiting, or controlling access to limited resources.

.. code-block:: python

    from threading import Thread, Semaphore
    import time

    # Allow max 3 concurrent connections
    connection_pool = Semaphore(3)

    def access_database(thread_id):
        print(f"Thread {thread_id} waiting for connection...")
        with connection_pool:
            print(f"Thread {thread_id} connected")
            time.sleep(1)  # Simulate database work
            print(f"Thread {thread_id} disconnected")

    threads = [Thread(target=access_database, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

Event - Thread Signaling
------------------------

An ``Event`` is a simple signaling mechanism that allows one thread to signal
other threads that something has happened. Threads can wait for the event to
be set, and one thread can set or clear the event. This is useful for
coordinating startup, shutdown, or state changes between threads.

.. code-block:: python

    from threading import Thread, Event
    import time

    ready = Event()

    def worker(worker_id):
        print(f"Worker {worker_id} waiting for signal...")
        ready.wait()  # Block until event is set
        print(f"Worker {worker_id} starting work")

    def coordinator():
        print("Coordinator preparing...")
        time.sleep(2)
        print("Coordinator: All systems go!")
        ready.set()  # Signal all waiting threads

    threads = [Thread(target=worker, args=(i,)) for i in range(3)]
    threads.append(Thread(target=coordinator))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

Condition - Complex Synchronization
-----------------------------------

A ``Condition`` combines a lock with the ability to wait for and notify about
state changes. It's essential for producer-consumer patterns where threads
need to wait for specific conditions (like "buffer not empty" or "buffer not
full") before proceeding.

.. code-block:: python

    from threading import Thread, Condition
    import time

    items = []
    condition = Condition()

    def producer():
        for i in range(5):
            time.sleep(0.5)
            with condition:
                items.append(i)
                print(f"Produced: {i}")
                condition.notify()  # Wake up one waiting consumer

    def consumer():
        while True:
            with condition:
                while not items:  # Wait until items available
                    condition.wait()
                item = items.pop(0)
                print(f"Consumed: {item}")
                if item == 4:
                    break

    t1 = Thread(target=producer)
    t2 = Thread(target=consumer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

Barrier - Synchronization Point
-------------------------------

A ``Barrier`` blocks a specified number of threads until all of them have
reached the barrier point, then releases them all simultaneously. This is
useful when you need multiple threads to complete a phase before any can
proceed to the next phase.

.. code-block:: python

    from threading import Thread, Barrier
    import time
    import random

    barrier = Barrier(3)

    def worker(worker_id):
        # Phase 1: Initialization
        print(f"Worker {worker_id} initializing...")
        time.sleep(random.uniform(0.5, 2))
        print(f"Worker {worker_id} waiting at barrier")

        barrier.wait()  # Wait for all threads

        # Phase 2: All threads proceed together
        print(f"Worker {worker_id} proceeding")

    threads = [Thread(target=worker, args=(i,)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

Timer - Delayed Execution
-------------------------

A ``Timer`` is a thread that executes a function after a specified delay.
It can be cancelled before it fires. This is useful for timeouts, delayed
cleanup, or scheduling one-time tasks.

.. code-block:: python

    from threading import Timer

    def delayed_task():
        print("Task executed after delay")

    # Execute after 2 seconds
    timer = Timer(2.0, delayed_task)
    timer.start()

    # Can be cancelled before it fires
    # timer.cancel()

Thread-Local Data
-----------------

``threading.local()`` provides thread-local storage where each thread has its
own independent copy of the data. This is useful for storing per-thread state
without passing it through function arguments, such as database connections
or request context in web applications.

.. code-block:: python

    from threading import Thread, local

    # Each thread gets its own 'data' attribute
    thread_data = local()

    def worker(worker_id):
        thread_data.value = worker_id
        process()

    def process():
        # Access thread-local data without passing as argument
        print(f"Processing with value: {thread_data.value}")

    threads = [Thread(target=worker, args=(i,)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

Producer-Consumer with Queue
----------------------------

The ``queue.Queue`` class provides a thread-safe FIFO queue that handles all
locking internally. This is the recommended way to communicate between threads
in a producer-consumer pattern, as it eliminates the need for manual
synchronization.

.. code-block:: python

    from threading import Thread
    from queue import Queue
    import time

    def producer(q, items):
        for item in items:
            time.sleep(0.1)
            q.put(item)
            print(f"Produced: {item}")
        q.put(None)  # Sentinel to signal completion

    def consumer(q):
        while True:
            item = q.get()
            if item is None:
                break
            print(f"Consumed: {item}")
            q.task_done()

    q = Queue(maxsize=5)  # Bounded queue
    items = list(range(10))

    t1 = Thread(target=producer, args=(q, items))
    t2 = Thread(target=consumer, args=(q,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

Deadlock Example and Prevention
-------------------------------

Deadlock occurs when two or more threads are waiting for each other to release
locks, creating a circular dependency. The classic example is when thread A
holds lock 1 and waits for lock 2, while thread B holds lock 2 and waits for
lock 1. Prevent deadlocks by always acquiring locks in a consistent order.

.. code-block:: python

    from threading import Thread, Lock
    import time

    lock1 = Lock()
    lock2 = Lock()

    # DEADLOCK EXAMPLE - DON'T DO THIS
    def task_a_bad():
        with lock1:
            print("Task A acquired lock1")
            time.sleep(0.1)
            with lock2:  # Waits for lock2
                print("Task A acquired lock2")

    def task_b_bad():
        with lock2:
            print("Task B acquired lock2")
            time.sleep(0.1)
            with lock1:  # Waits for lock1 - DEADLOCK!
                print("Task B acquired lock1")

    # CORRECT - Always acquire locks in same order
    def task_a_good():
        with lock1:
            with lock2:
                print("Task A acquired both locks")

    def task_b_good():
        with lock1:  # Same order as task_a
            with lock2:
                print("Task B acquired both locks")

Understanding the GIL
---------------------

The Global Interpreter Lock (GIL) is a mutex that protects access to Python
objects, preventing multiple threads from executing Python bytecode
simultaneously. This means threads don't provide speedup for CPU-bound tasks.
However, the GIL is released during I/O operations, making threads effective
for I/O-bound tasks.

.. code-block:: python

    from threading import Thread
    import time

    def cpu_bound(n):
        """CPU-bound task - GIL limits parallelism."""
        count = 0
        for i in range(n):
            count += i
        return count

    def io_bound(seconds):
        """I/O-bound task - GIL released during sleep."""
        time.sleep(seconds)

    # CPU-bound: threads won't help (may be slower due to GIL contention)
    start = time.time()
    threads = [Thread(target=cpu_bound, args=(10**7,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"CPU-bound threaded: {time.time() - start:.2f}s")

    # I/O-bound: threads help significantly
    start = time.time()
    threads = [Thread(target=io_bound, args=(1,)) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"I/O-bound threaded: {time.time() - start:.2f}s")  # ~1s, not 4s
