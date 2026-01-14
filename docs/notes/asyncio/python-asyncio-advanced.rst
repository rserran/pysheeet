.. meta::
    :description lang=en: Python asyncio advanced - synchronization, queues, subprocesses, debugging, patterns
    :keywords: Python, Python3, Asyncio, Synchronization, Queue, Semaphore, Lock, Subprocess, Debugging

=================
Asyncio Advanced
=================

:Source: `src/basic/asyncio_.py <https://github.com/crazyguitar/pysheeet/blob/master/src/basic/asyncio_.py>`_

.. contents:: Table of Contents
    :backlinks: none

Introduction
------------

Beyond basic coroutines and networking, asyncio provides synchronization
primitives, queues, subprocess management, and debugging tools. This section
covers advanced patterns for building robust async applications, including
producer-consumer patterns, rate limiting, graceful shutdown, and integration
with synchronous code.

Locks
-----

``asyncio.Lock`` prevents multiple coroutines from accessing a shared resource
simultaneously. Unlike threading locks, async locks must be used with ``await``
and only work within the same event loop.

.. code-block:: python

    import asyncio

    class SharedCounter:
        def __init__(self):
            self.value = 0
            self._lock = asyncio.Lock()

        async def increment(self):
            async with self._lock:
                current = self.value
                await asyncio.sleep(0.01)  # Simulate work
                self.value = current + 1

    async def worker(counter, name, count):
        for _ in range(count):
            await counter.increment()
        print(f"{name} done")

    async def main():
        counter = SharedCounter()
        await asyncio.gather(
            worker(counter, "A", 100),
            worker(counter, "B", 100),
            worker(counter, "C", 100),
        )
        print(f"Final value: {counter.value}")  # Should be 300

    asyncio.run(main())

Semaphores for Rate Limiting
----------------------------

``asyncio.Semaphore`` limits the number of concurrent operations. This is
essential for rate limiting API calls, limiting database connections, or
controlling resource usage.

.. code-block:: python

    import asyncio

    async def fetch(url, semaphore):
        async with semaphore:
            print(f"Fetching {url}")
            await asyncio.sleep(1)  # Simulate network request
            return f"Response from {url}"

    async def main():
        # Limit to 3 concurrent requests
        semaphore = asyncio.Semaphore(3)

        urls = [f"https://api.example.com/{i}" for i in range(10)]
        tasks = [fetch(url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)

        for r in results:
            print(r)

    asyncio.run(main())

Events for Signaling
--------------------

``asyncio.Event`` allows coroutines to wait for a signal from another coroutine.
This is useful for coordinating startup, shutdown, or state changes between
multiple tasks.

.. code-block:: python

    import asyncio

    async def waiter(event, name):
        print(f"{name} waiting for event")
        await event.wait()
        print(f"{name} got the event!")

    async def setter(event):
        print("Setting event in 2 seconds...")
        await asyncio.sleep(2)
        event.set()
        print("Event set!")

    async def main():
        event = asyncio.Event()

        await asyncio.gather(
            waiter(event, "Task 1"),
            waiter(event, "Task 2"),
            waiter(event, "Task 3"),
            setter(event),
        )

    asyncio.run(main())

Conditions for Complex Synchronization
--------------------------------------

``asyncio.Condition`` combines a lock with the ability to wait for a condition.
This is useful for producer-consumer patterns where consumers need to wait
for specific conditions.

.. code-block:: python

    import asyncio

    class Buffer:
        def __init__(self, size):
            self.buffer = []
            self.size = size
            self.condition = asyncio.Condition()

        async def put(self, item):
            async with self.condition:
                while len(self.buffer) >= self.size:
                    await self.condition.wait()
                self.buffer.append(item)
                self.condition.notify()

        async def get(self):
            async with self.condition:
                while not self.buffer:
                    await self.condition.wait()
                item = self.buffer.pop(0)
                self.condition.notify()
                return item

    async def producer(buffer, name):
        for i in range(5):
            await buffer.put(f"{name}-{i}")
            print(f"Produced: {name}-{i}")
            await asyncio.sleep(0.1)

    async def consumer(buffer, name):
        for _ in range(5):
            item = await buffer.get()
            print(f"{name} consumed: {item}")
            await asyncio.sleep(0.2)

    async def main():
        buffer = Buffer(size=2)
        await asyncio.gather(
            producer(buffer, "P1"),
            consumer(buffer, "C1"),
            consumer(buffer, "C2"),
        )

    asyncio.run(main())

Queues for Producer-Consumer
----------------------------

``asyncio.Queue`` is the preferred way to implement producer-consumer patterns.
It handles synchronization internally and provides blocking get/put operations
with optional timeouts.

.. code-block:: python

    import asyncio

    async def producer(queue, name):
        for i in range(5):
            item = f"{name}-item-{i}"
            await queue.put(item)
            print(f"Produced: {item}")
            await asyncio.sleep(0.5)

    async def consumer(queue, name):
        while True:
            try:
                item = await asyncio.wait_for(queue.get(), timeout=2.0)
                print(f"{name} consumed: {item}")
                queue.task_done()
                await asyncio.sleep(0.1)
            except asyncio.TimeoutError:
                print(f"{name} timed out, exiting")
                break

    async def main():
        queue = asyncio.Queue(maxsize=3)

        producers = [
            asyncio.create_task(producer(queue, "P1")),
            asyncio.create_task(producer(queue, "P2")),
        ]
        consumers = [
            asyncio.create_task(consumer(queue, "C1")),
            asyncio.create_task(consumer(queue, "C2")),
        ]

        await asyncio.gather(*producers)
        await queue.join()  # Wait for all items to be processed

        for c in consumers:
            c.cancel()

    asyncio.run(main())

Priority Queue
--------------

``asyncio.PriorityQueue`` processes items by priority. Lower priority values
are processed first. Items must be comparable or wrapped in tuples with
priority as the first element.

.. code-block:: python

    import asyncio

    async def producer(queue):
        items = [
            (3, "low priority"),
            (1, "high priority"),
            (2, "medium priority"),
        ]
        for priority, item in items:
            await queue.put((priority, item))
            print(f"Added: {item} (priority {priority})")

    async def consumer(queue):
        while not queue.empty():
            priority, item = await queue.get()
            print(f"Processing: {item} (priority {priority})")
            await asyncio.sleep(0.5)
            queue.task_done()

    async def main():
        queue = asyncio.PriorityQueue()
        await producer(queue)
        await consumer(queue)

    asyncio.run(main())

Running Subprocesses
--------------------

Asyncio can run and communicate with subprocesses asynchronously. This is
useful for running shell commands, external tools, or parallel processes
without blocking the event loop.

.. code-block:: python

    import asyncio

    async def run_command(cmd):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        return {
            'cmd': cmd,
            'returncode': proc.returncode,
            'stdout': stdout.decode().strip(),
            'stderr': stderr.decode().strip()
        }

    async def main():
        commands = [
            "echo 'Hello World'",
            "python --version",
            "date",
        ]

        results = await asyncio.gather(*[run_command(c) for c in commands])

        for r in results:
            print(f"Command: {r['cmd']}")
            print(f"Output: {r['stdout']}")
            print()

    asyncio.run(main())

Subprocess with Streaming Output
--------------------------------

For long-running processes, you can stream output line by line instead of
waiting for the process to complete. This is useful for monitoring logs or
progress.

.. code-block:: python

    import asyncio

    async def stream_subprocess(cmd):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        while True:
            line = await proc.stdout.readline()
            if not line:
                break
            print(f"[{cmd[:20]}] {line.decode().strip()}")

        await proc.wait()
        return proc.returncode

    async def main():
        # Run multiple commands and stream their output
        await asyncio.gather(
            stream_subprocess("for i in 1 2 3; do echo $i; sleep 1; done"),
            stream_subprocess("for i in a b c; do echo $i; sleep 0.5; done"),
        )

    asyncio.run(main())

Graceful Shutdown
-----------------

Proper shutdown handling ensures all tasks complete cleanly and resources
are released. Use signal handlers to catch SIGINT/SIGTERM and cancel tasks
gracefully.

.. code-block:: python

    import asyncio
    import signal

    async def worker(name):
        try:
            while True:
                print(f"{name} working...")
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print(f"{name} cancelled, cleaning up...")
            await asyncio.sleep(0.5)  # Cleanup time
            print(f"{name} cleanup done")
            raise

    async def main():
        loop = asyncio.get_event_loop()
        tasks = [
            asyncio.create_task(worker("Worker-1")),
            asyncio.create_task(worker("Worker-2")),
        ]

        def shutdown():
            print("\nShutdown requested...")
            for task in tasks:
                task.cancel()

        loop.add_signal_handler(signal.SIGINT, shutdown)
        loop.add_signal_handler(signal.SIGTERM, shutdown)

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            print("All tasks cancelled")

    asyncio.run(main())

Running Async Code in Threads
-----------------------------

When you need to run async code from synchronous code (e.g., in a callback
or from another thread), use ``asyncio.run_coroutine_threadsafe()``.

.. code-block:: python

    import asyncio
    import threading
    import time

    async def async_task(value):
        await asyncio.sleep(1)
        return value * 2

    def thread_function(loop):
        # Run async code from a different thread
        future = asyncio.run_coroutine_threadsafe(
            async_task(21), loop
        )
        result = future.result(timeout=5)
        print(f"Thread got result: {result}")

    async def main():
        loop = asyncio.get_event_loop()

        # Start a thread that will call async code
        thread = threading.Thread(target=thread_function, args=(loop,))
        thread.start()

        # Keep the event loop running
        await asyncio.sleep(2)
        thread.join()

    asyncio.run(main())

Debugging Asyncio
-----------------

Enable debug mode to catch common mistakes like blocking calls, unawaited
coroutines, and slow callbacks. Debug mode adds overhead so use it only
during development.

.. code-block:: python

    import asyncio
    import logging

    # Enable debug logging
    logging.basicConfig(level=logging.DEBUG)

    async def slow_callback():
        import time
        time.sleep(0.2)  # This will trigger a warning in debug mode

    async def main():
        await slow_callback()

    # Method 1: Environment variable
    # PYTHONASYNCIODEBUG=1 python script.py

    # Method 2: asyncio.run with debug=True
    asyncio.run(main(), debug=True)

Custom Event Loop
-----------------

You can customize the event loop behavior by subclassing or patching. This
is useful for debugging, profiling, or adding custom functionality.

.. code-block:: python

    import asyncio

    class DebugEventLoop(asyncio.SelectorEventLoop):
        def _run_once(self):
            # Track number of scheduled callbacks
            num_ready = len(self._ready)
            num_scheduled = len(self._scheduled)
            if num_ready or num_scheduled:
                print(f"Ready: {num_ready}, Scheduled: {num_scheduled}")
            super()._run_once()

    async def task(n):
        await asyncio.sleep(n)
        print(f"Task {n} done")

    # Use custom event loop
    loop = DebugEventLoop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(asyncio.gather(
            task(0.1),
            task(0.2),
            task(0.3),
        ))
    finally:
        loop.close()

Timeout Patterns
----------------

Different timeout patterns for various use cases: per-operation timeout,
overall timeout, and timeout with fallback.

.. code-block:: python

    import asyncio

    async def fetch(url, delay):
        await asyncio.sleep(delay)
        return f"Response from {url}"

    async def fetch_with_timeout(url, delay, timeout):
        """Per-operation timeout."""
        try:
            return await asyncio.wait_for(fetch(url, delay), timeout)
        except asyncio.TimeoutError:
            return f"Timeout for {url}"

    async def fetch_all_with_timeout(urls, timeout):
        """Overall timeout for all operations."""
        async def fetch_all():
            return await asyncio.gather(*[fetch(u, i) for i, u in enumerate(urls)])

        try:
            return await asyncio.wait_for(fetch_all(), timeout)
        except asyncio.TimeoutError:
            return ["Overall timeout"]

    async def fetch_with_fallback(url, delay, timeout, fallback):
        """Timeout with fallback value."""
        try:
            return await asyncio.wait_for(fetch(url, delay), timeout)
        except asyncio.TimeoutError:
            return fallback

    async def main():
        # Per-operation timeout
        result = await fetch_with_timeout("slow.com", 5, 1)
        print(result)

        # Timeout with fallback
        result = await fetch_with_fallback("slow.com", 5, 1, "cached response")
        print(result)

    asyncio.run(main())

Retry Pattern
-------------

Implement retry logic for transient failures with exponential backoff.
This is essential for robust network clients.

.. code-block:: python

    import asyncio
    import random

    class RetryError(Exception):
        pass

    async def unreliable_operation():
        """Simulates an operation that fails randomly."""
        if random.random() < 0.7:
            raise ConnectionError("Network error")
        return "Success!"

    async def retry(coro_func, max_retries=3, base_delay=1.0):
        """Retry with exponential backoff."""
        last_exception = None

        for attempt in range(max_retries):
            try:
                return await coro_func()
            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    jitter = random.uniform(0, 0.1 * delay)
                    print(f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s")
                    await asyncio.sleep(delay + jitter)

        raise RetryError(f"Failed after {max_retries} attempts") from last_exception

    async def main():
        try:
            result = await retry(unreliable_operation, max_retries=5)
            print(f"Result: {result}")
        except RetryError as e:
            print(f"All retries failed: {e}")

    asyncio.run(main())

Async Context Variable
----------------------

Context variables (Python 3.7+) provide task-local storage, similar to
thread-local storage but for async tasks. Useful for request IDs, user
context, or database connections.

.. code-block:: python

    import asyncio
    import contextvars

    # Create context variable
    request_id = contextvars.ContextVar('request_id', default=None)

    async def process_request(rid):
        request_id.set(rid)
        await step1()
        await step2()

    async def step1():
        rid = request_id.get()
        print(f"[{rid}] Step 1")
        await asyncio.sleep(0.1)

    async def step2():
        rid = request_id.get()
        print(f"[{rid}] Step 2")
        await asyncio.sleep(0.1)

    async def main():
        await asyncio.gather(
            process_request("req-001"),
            process_request("req-002"),
            process_request("req-003"),
        )

    asyncio.run(main())

TaskGroup (Python 3.11+)
------------------------

``TaskGroup`` provides structured concurrency, ensuring all tasks complete
or are cancelled together. Exceptions in any task cancel all other tasks
in the group.

.. code-block:: python

    import asyncio

    async def task(name, delay, should_fail=False):
        await asyncio.sleep(delay)
        if should_fail:
            raise ValueError(f"{name} failed!")
        return f"{name} done"

    async def main():
        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(task("A", 1))
                tg.create_task(task("B", 2))
                tg.create_task(task("C", 0.5, should_fail=True))
        except* ValueError as eg:
            for exc in eg.exceptions:
                print(f"Caught: {exc}")

    # Python 3.11+
    asyncio.run(main())
