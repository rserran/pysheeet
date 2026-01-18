.. meta::
    :description lang=en: Python asyncio basics - coroutines, tasks, event loop, async/await syntax
    :keywords: Python, Python3, Asyncio, Coroutines, Event Loop, async await, Asynchronous Programming

================
Asyncio Basics
================

:Source: `src/basic/asyncio_.py <https://github.com/crazyguitar/pysheeet/blob/master/src/basic/asyncio_.py>`_

.. contents:: Table of Contents
    :backlinks: none

Introduction
------------

The ``asyncio`` module, introduced in Python 3.4 and significantly improved in
Python 3.5+ with ``async/await`` syntax, provides a foundation for writing
asynchronous code. Unlike threads which use preemptive multitasking (the OS
decides when to switch), asyncio uses cooperative multitasking where coroutines
explicitly yield control using ``await``. This eliminates race conditions common
in threaded code and makes reasoning about program flow much easier.

Key concepts:

- **Coroutine**: A function defined with ``async def`` that can be paused and resumed
- **Event Loop**: The central scheduler that runs coroutines and handles I/O events
- **Task**: A wrapper around a coroutine that schedules it for execution
- **Future**: A placeholder for a result that will be available later

Running Coroutines with asyncio.run
-----------------------------------

The simplest way to run async code is ``asyncio.run()``, introduced in Python 3.7.
It creates an event loop, runs the coroutine until completion, and cleans up
automatically. This is the recommended entry point for asyncio programs.

.. code-block:: python

    import asyncio

    async def hello():
        print("Hello")
        await asyncio.sleep(1)
        print("World")

    # Python 3.7+
    asyncio.run(hello())

For file I/O or other blocking operations, use ``run_in_executor`` to avoid
blocking the event loop:

.. code-block:: python

    import asyncio
    from concurrent.futures import ThreadPoolExecutor

    async def read_file(path):
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            with open(path) as f:
                return await loop.run_in_executor(pool, f.read)

    content = asyncio.run(read_file('/etc/hosts'))

Creating and Managing Tasks
---------------------------

Tasks allow multiple coroutines to run concurrently. When you create a task,
it's scheduled to run on the event loop immediately. Use ``asyncio.create_task()``
(Python 3.7+) or ``loop.create_task()`` to create tasks.

.. code-block:: python

    import asyncio

    async def fetch(name, delay):
        await asyncio.sleep(delay)
        return f"{name} done"

    async def main():
        # Create tasks - they start running immediately
        task1 = asyncio.create_task(fetch("A", 2))
        task2 = asyncio.create_task(fetch("B", 1))

        # Wait for both to complete
        result1 = await task1
        result2 = await task2
        print(result1, result2)

    asyncio.run(main())

Gathering Multiple Coroutines
-----------------------------

``asyncio.gather()`` runs multiple coroutines concurrently and collects their
results in order. This is the most common way to run multiple async operations
in parallel and wait for all of them to complete.

.. code-block:: python

    import asyncio

    async def fetch(url, delay):
        await asyncio.sleep(delay)
        return f"Response from {url}"

    async def main():
        urls = ["site1.com", "site2.com", "site3.com"]
        coros = [fetch(url, i * 0.5) for i, url in enumerate(urls)]

        # Run all concurrently, results in same order as input
        results = await asyncio.gather(*coros)
        for r in results:
            print(r)

    asyncio.run(main())

Waiting with Timeout
--------------------

Use ``asyncio.wait_for()`` to set a timeout on async operations. This is
essential for network operations where you don't want to wait indefinitely
for a response that may never come.

.. code-block:: python

    import asyncio

    async def slow_operation():
        await asyncio.sleep(10)
        return "done"

    async def main():
        try:
            result = await asyncio.wait_for(slow_operation(), timeout=2.0)
        except asyncio.TimeoutError:
            print("Operation timed out!")

    asyncio.run(main())

Waiting for First Completed
---------------------------

``asyncio.wait()`` provides more control than ``gather()``. You can wait for
the first task to complete, first exception, or all tasks. This is useful
when you want to process results as they become available.

.. code-block:: python

    import asyncio

    async def fetch(name, delay):
        await asyncio.sleep(delay)
        return f"{name}: {delay}s"

    async def main():
        tasks = [
            asyncio.create_task(fetch("fast", 1)),
            asyncio.create_task(fetch("slow", 3)),
        ]

        # Wait for first to complete
        done, pending = await asyncio.wait(
            tasks, return_when=asyncio.FIRST_COMPLETED
        )

        for task in done:
            print(f"Completed: {task.result()}")
        print(f"Still pending: {len(pending)}")

        # Cancel pending tasks
        for task in pending:
            task.cancel()

    asyncio.run(main())

Asynchronous Iteration
----------------------

Async iterators allow you to iterate over data that arrives asynchronously,
such as streaming responses or database cursors. Implement ``__aiter__`` and
``__anext__`` methods to create custom async iterators.

.. code-block:: python

    import asyncio

    class AsyncRange:
        """Async iterator that yields numbers with delays."""

        def __init__(self, start, stop):
            self.current = start
            self.stop = stop

        def __aiter__(self):
            return self

        async def __anext__(self):
            if self.current >= self.stop:
                raise StopAsyncIteration
            await asyncio.sleep(0.5)
            value = self.current
            self.current += 1
            return value

    async def main():
        async for num in AsyncRange(0, 5):
            print(num)

    asyncio.run(main())

Asynchronous Context Managers
-----------------------------

Async context managers are essential for managing resources that require
async setup or cleanup, such as database connections, file handles, or
network sessions. Use ``async with`` to ensure proper resource management.

.. code-block:: python

    import asyncio

    class AsyncConnection:
        """Simulated async database connection."""

        async def __aenter__(self):
            print("Connecting...")
            await asyncio.sleep(1)
            print("Connected")
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            print("Disconnecting...")
            await asyncio.sleep(0.5)
            print("Disconnected")

        async def query(self, sql):
            await asyncio.sleep(0.1)
            return f"Result of: {sql}"

    async def main():
        async with AsyncConnection() as conn:
            result = await conn.query("SELECT * FROM users")
            print(result)

    asyncio.run(main())

Using @asynccontextmanager
--------------------------

The ``@asynccontextmanager`` decorator (Python 3.7+) provides a simpler way
to create async context managers using generator syntax, similar to the
synchronous ``@contextmanager`` decorator.

.. code-block:: python

    import asyncio
    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def managed_resource(name):
        print(f"Acquiring {name}")
        await asyncio.sleep(0.5)
        try:
            yield name
        finally:
            print(f"Releasing {name}")
            await asyncio.sleep(0.2)

    async def main():
        async with managed_resource("database") as resource:
            print(f"Using {resource}")

    asyncio.run(main())

Running Blocking Code in Executor
---------------------------------

When you need to call blocking code (file I/O, CPU-intensive operations,
or libraries without async support), use ``run_in_executor()`` to run it
in a thread pool without blocking the event loop.

.. code-block:: python

    import asyncio
    import time
    from concurrent.futures import ThreadPoolExecutor

    def blocking_io():
        """Simulates blocking I/O operation."""
        time.sleep(2)
        return "IO complete"

    def cpu_bound():
        """Simulates CPU-intensive operation."""
        return sum(i * i for i in range(10**6))

    async def main():
        loop = asyncio.get_event_loop()

        # Run in default executor (ThreadPoolExecutor)
        result1 = await loop.run_in_executor(None, blocking_io)
        print(result1)

        # Run in custom executor
        with ThreadPoolExecutor(max_workers=4) as pool:
            result2 = await loop.run_in_executor(pool, cpu_bound)
            print(result2)

    asyncio.run(main())

Async Generators
----------------

Async generators (Python 3.6+) combine generators with async/await, allowing
you to yield values asynchronously. They're useful for streaming data or
implementing async iterators more concisely.

.. code-block:: python

    import asyncio

    async def async_range(start, stop):
        """Async generator that yields numbers with delays."""
        for i in range(start, stop):
            await asyncio.sleep(0.5)
            yield i

    async def main():
        async for num in async_range(0, 5):
            print(num)

        # Async comprehension
        results = [x async for x in async_range(0, 3)]
        print(results)

    asyncio.run(main())

Exception Handling in Tasks
---------------------------

Exceptions in tasks are stored and re-raised when you await the task or
call ``result()``. Unhandled exceptions in tasks that are never awaited
will be logged but may be silently ignored, so always await your tasks.

.. code-block:: python

    import asyncio

    async def failing_task():
        await asyncio.sleep(1)
        raise ValueError("Something went wrong")

    async def main():
        task = asyncio.create_task(failing_task())

        try:
            await task
        except ValueError as e:
            print(f"Caught exception: {e}")

        # Using gather with return_exceptions
        tasks = [
            asyncio.create_task(asyncio.sleep(1)),
            asyncio.create_task(failing_task()),
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, Exception):
                print(f"Task failed: {r}")
            else:
                print(f"Task succeeded: {r}")

    asyncio.run(main())

Cancelling Tasks
----------------

Tasks can be cancelled using ``task.cancel()``. The cancelled task will
raise ``asyncio.CancelledError`` at the next await point. Handle this
exception to perform cleanup when a task is cancelled.

.. code-block:: python

    import asyncio

    async def long_running():
        try:
            while True:
                print("Working...")
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("Task was cancelled, cleaning up...")
            raise  # Re-raise to mark task as cancelled

    async def main():
        task = asyncio.create_task(long_running())

        await asyncio.sleep(3)
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            print("Task cancellation confirmed")

    asyncio.run(main())
