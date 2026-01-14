.. meta::
    :description lang=en: Python concurrent.futures tutorial covering ThreadPoolExecutor, ProcessPoolExecutor, Future objects, callbacks, and high-level parallel execution patterns
    :keywords: Python, Python3, concurrent.futures, ThreadPoolExecutor, ProcessPoolExecutor, Future, executor, submit, map, as_completed, parallel

==================
concurrent.futures
==================

:Source: `src/basic/concurrency_.py <https://github.com/crazyguitar/pysheeet/blob/master/src/basic/concurrency_.py>`_

.. contents:: Table of Contents
    :backlinks: none

Introduction
------------

The ``concurrent.futures`` module provides a high-level interface for
asynchronously executing callables using threads or processes. It abstracts
the differences between threading and multiprocessing behind a unified API,
making it easy to switch between them. The module introduces two key concepts:
**Executors** that manage pools of workers, and **Futures** that represent
the eventual result of an asynchronous operation.

ThreadPoolExecutor Basics
-------------------------

``ThreadPoolExecutor`` manages a pool of threads that execute tasks concurrently.
Use it for I/O-bound tasks like network requests, file operations, or database
queries where threads spend time waiting for external resources.

.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor
    import time

    def fetch_url(url):
        """Simulate fetching a URL."""
        time.sleep(1)  # Simulate network delay
        return f"Content from {url}"

    urls = ["http://site1.com", "http://site2.com", "http://site3.com"]

    # Sequential - takes ~3 seconds
    start = time.time()
    results = [fetch_url(url) for url in urls]
    print(f"Sequential: {time.time() - start:.2f}s")

    # Concurrent - takes ~1 second
    start = time.time()
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(fetch_url, urls))
    print(f"Concurrent: {time.time() - start:.2f}s")

ProcessPoolExecutor Basics
--------------------------

``ProcessPoolExecutor`` manages a pool of processes for true parallel execution.
Use it for CPU-bound tasks like data processing, calculations, or image
manipulation where you need to utilize multiple CPU cores.

.. code-block:: python

    from concurrent.futures import ProcessPoolExecutor
    import time

    def cpu_intensive(n):
        """CPU-bound computation."""
        return sum(i * i for i in range(n))

    if __name__ == "__main__":
        numbers = [10**7] * 4

        # Sequential
        start = time.time()
        results = [cpu_intensive(n) for n in numbers]
        print(f"Sequential: {time.time() - start:.2f}s")

        # Parallel with processes
        start = time.time()
        with ProcessPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(cpu_intensive, numbers))
        print(f"Parallel: {time.time() - start:.2f}s")

Using submit() and Future Objects
---------------------------------

The ``submit()`` method schedules a callable and returns a ``Future`` object
immediately. The Future represents the pending result and provides methods to
check status, get the result, or cancel the task. This gives more control than
``map()`` for handling individual tasks.

.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor
    import time

    def task(name, duration):
        time.sleep(duration)
        return f"{name} completed in {duration}s"

    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks - returns Future immediately
        future1 = executor.submit(task, "Task A", 2)
        future2 = executor.submit(task, "Task B", 1)
        future3 = executor.submit(task, "Task C", 3)

        # Check if done (non-blocking)
        print(f"Task A done: {future1.done()}")

        # Get result (blocking)
        print(future2.result())  # Waits for completion
        print(future1.result())
        print(future3.result())

Processing Results as They Complete
-----------------------------------

``as_completed()`` yields futures as they complete, regardless of submission
order. This is useful when you want to process results as soon as they're
available rather than waiting for all tasks to finish.

.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time
    import random

    def fetch_data(source_id):
        delay = random.uniform(0.5, 2.0)
        time.sleep(delay)
        return f"Data from source {source_id} (took {delay:.2f}s)"

    sources = range(5)

    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all tasks
        future_to_source = {
            executor.submit(fetch_data, src): src
            for src in sources
        }

        # Process results as they complete
        for future in as_completed(future_to_source):
            source = future_to_source[future]
            try:
                result = future.result()
                print(f"Source {source}: {result}")
            except Exception as e:
                print(f"Source {source} failed: {e}")

Using wait() for Completion Control
-----------------------------------

``wait()`` blocks until specified futures complete. You can wait for all tasks,
the first task, or the first exception. This provides fine-grained control
over when to proceed.

.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, ALL_COMPLETED
    import time

    def task(task_id, duration):
        time.sleep(duration)
        return f"Task {task_id} done"

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(task, 1, 3),
            executor.submit(task, 2, 1),
            executor.submit(task, 3, 2),
        ]

        # Wait for first to complete
        done, not_done = wait(futures, return_when=FIRST_COMPLETED)
        print(f"First completed: {done.pop().result()}")
        print(f"Still running: {len(not_done)}")

        # Wait for all remaining
        done, not_done = wait(not_done, return_when=ALL_COMPLETED)
        for f in done:
            print(f"Completed: {f.result()}")

Adding Callbacks to Futures
---------------------------

Callbacks are functions that execute automatically when a future completes.
They're useful for processing results without blocking the main thread or
for chaining operations. The callback receives the future as its argument.

.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor
    import time

    def compute(n):
        time.sleep(1)
        return n * n

    def on_complete(future):
        """Callback executed when future completes."""
        try:
            result = future.result()
            print(f"Callback: result is {result}")
        except Exception as e:
            print(f"Callback: task failed with {e}")

    with ThreadPoolExecutor(max_workers=3) as executor:
        for i in range(5):
            future = executor.submit(compute, i)
            future.add_done_callback(on_complete)

        # Main thread continues while callbacks fire
        print("Main thread: tasks submitted")
        time.sleep(2)
        print("Main thread: done waiting")

Exception Handling
------------------

Exceptions raised in tasks are captured and re-raised when you call
``result()``. You can also check for exceptions using ``exception()``.
Always handle exceptions to prevent silent failures.

.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor, as_completed

    def risky_task(n):
        if n == 3:
            raise ValueError(f"Bad value: {n}")
        return n * 2

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(risky_task, i): i for i in range(5)}

        for future in as_completed(futures):
            n = futures[future]
            try:
                result = future.result()
                print(f"Task {n}: {result}")
            except ValueError as e:
                print(f"Task {n} failed: {e}")

        # Alternative: check exception without raising
        future = executor.submit(risky_task, 3)
        future.result()  # Wait for completion
        if future.exception() is not None:
            print(f"Exception occurred: {future.exception()}")

Timeout Handling
----------------

Both ``result()`` and ``as_completed()`` accept timeout parameters. If a task
doesn't complete within the timeout, a ``TimeoutError`` is raised. This
prevents indefinite blocking on slow or stuck tasks.

.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
    import time

    def slow_task(duration):
        time.sleep(duration)
        return f"Completed after {duration}s"

    with ThreadPoolExecutor(max_workers=2) as executor:
        future = executor.submit(slow_task, 5)

        try:
            # Wait max 2 seconds for result
            result = future.result(timeout=2)
            print(result)
        except TimeoutError:
            print("Task timed out!")
            # Note: task continues running in background

        # Timeout with as_completed
        futures = [executor.submit(slow_task, i) for i in [1, 3, 5]]
        try:
            for future in as_completed(futures, timeout=2):
                print(future.result())
        except TimeoutError:
            print("Some tasks didn't complete in time")

Cancelling Tasks
----------------

Tasks can be cancelled before they start executing using ``cancel()``. Once
a task has started, it cannot be cancelled. Check ``cancelled()`` to see if
cancellation succeeded.

.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor
    import time

    def long_task(n):
        time.sleep(2)
        return n

    with ThreadPoolExecutor(max_workers=1) as executor:
        # Submit multiple tasks to single worker
        future1 = executor.submit(long_task, 1)
        future2 = executor.submit(long_task, 2)  # Queued, not started
        future3 = executor.submit(long_task, 3)  # Queued, not started

        time.sleep(0.1)  # Let first task start

        # Try to cancel queued tasks
        cancelled2 = future2.cancel()
        cancelled3 = future3.cancel()

        print(f"Future 2 cancelled: {cancelled2}")  # True
        print(f"Future 3 cancelled: {cancelled3}")  # True
        print(f"Future 1 cancelled: {future1.cancel()}")  # False (already running)

Executor Context Manager
------------------------

Using executors as context managers (``with`` statement) ensures proper cleanup.
When exiting the context, ``shutdown(wait=True)`` is called automatically,
which waits for all pending tasks to complete before returning.

.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor
    import time

    def task(n):
        time.sleep(1)
        return n * 2

    # Context manager - automatic cleanup
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(task, i) for i in range(5)]
        # Executor waits for all tasks when exiting 'with' block

    print("All tasks completed")

    # Manual management (not recommended)
    executor = ThreadPoolExecutor(max_workers=3)
    try:
        futures = [executor.submit(task, i) for i in range(5)]
    finally:
        executor.shutdown(wait=True)  # Must call explicitly

Map with Chunking
-----------------

For large iterables, ``map()`` can be more efficient with chunking. The
``chunksize`` parameter groups items together, reducing overhead from
inter-process communication when using ``ProcessPoolExecutor``.

.. code-block:: python

    from concurrent.futures import ProcessPoolExecutor
    import time

    def process_item(x):
        return x * x

    if __name__ == "__main__":
        items = range(100000)

        # Without chunking - more IPC overhead
        start = time.time()
        with ProcessPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(process_item, items))
        print(f"No chunking: {time.time() - start:.2f}s")

        # With chunking - less IPC overhead
        start = time.time()
        with ProcessPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(process_item, items, chunksize=1000))
        print(f"With chunking: {time.time() - start:.2f}s")

Real-World Example: Parallel Downloads
--------------------------------------

This example demonstrates a practical use case: downloading multiple files
concurrently with progress tracking, error handling, and timeout management.

.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor, as_completed
    import urllib.request
    import time

    def download(url, timeout=10):
        """Download URL content with timeout."""
        try:
            with urllib.request.urlopen(url, timeout=timeout) as response:
                content = response.read()
                return url, len(content), None
        except Exception as e:
            return url, 0, str(e)

    urls = [
        "https://www.python.org",
        "https://www.github.com",
        "https://www.google.com",
        "https://httpbin.org/delay/5",  # Slow endpoint
    ]

    print("Starting downloads...")
    start = time.time()

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_url = {executor.submit(download, url): url for url in urls}

        for future in as_completed(future_to_url, timeout=15):
            url, size, error = future.result()
            if error:
                print(f"FAILED: {url} - {error}")
            else:
                print(f"OK: {url} - {size} bytes")

    print(f"Total time: {time.time() - start:.2f}s")
