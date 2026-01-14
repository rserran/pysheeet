"""Tests for asyncio examples."""

import asyncio
import pytest


class TestAsyncioBasics:
    """Test basic asyncio operations."""

    def test_asyncio_run(self):
        """Test basic coroutine execution."""

        async def hello():
            return "hello"

        result = asyncio.run(hello())
        assert result == "hello"

    def test_create_task(self):
        """Test task creation and execution."""

        async def compute(x):
            await asyncio.sleep(0.01)
            return x * 2

        async def main():
            task = asyncio.create_task(compute(5))
            return await task

        result = asyncio.run(main())
        assert result == 10

    def test_gather(self):
        """Test gathering multiple coroutines."""

        async def fetch(n):
            await asyncio.sleep(0.01)
            return n

        async def main():
            return await asyncio.gather(fetch(1), fetch(2), fetch(3))

        results = asyncio.run(main())
        assert results == [1, 2, 3]

    def test_wait_for_timeout(self):
        """Test timeout handling."""

        async def slow():
            await asyncio.sleep(10)

        async def main():
            await asyncio.wait_for(slow(), timeout=0.01)

        with pytest.raises(asyncio.TimeoutError):
            asyncio.run(main())

    def test_wait_first_completed(self):
        """Test waiting for first completed task."""

        async def fast():
            await asyncio.sleep(0.01)
            return "fast"

        async def slow():
            await asyncio.sleep(1)
            return "slow"

        async def main():
            tasks = [asyncio.create_task(fast()), asyncio.create_task(slow())]
            done, pending = await asyncio.wait(
                tasks, return_when=asyncio.FIRST_COMPLETED
            )
            for task in pending:
                task.cancel()
            return len(done), len(pending)

        done_count, pending_count = asyncio.run(main())
        assert done_count == 1
        assert pending_count == 1


class TestAsyncIterator:
    """Test async iterators."""

    def test_async_iterator(self):
        """Test custom async iterator."""

        class AsyncRange:
            def __init__(self, stop):
                self.current = 0
                self.stop = stop

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self.current >= self.stop:
                    raise StopAsyncIteration
                await asyncio.sleep(0.001)
                value = self.current
                self.current += 1
                return value

        async def main():
            results = []
            async for num in AsyncRange(3):
                results.append(num)
            return results

        results = asyncio.run(main())
        assert results == [0, 1, 2]

    def test_async_generator(self):
        """Test async generator."""

        async def async_range(stop):
            for i in range(stop):
                await asyncio.sleep(0.001)
                yield i

        async def main():
            return [x async for x in async_range(3)]

        results = asyncio.run(main())
        assert results == [0, 1, 2]


class TestAsyncContextManager:
    """Test async context managers."""

    def test_async_context_manager(self):
        """Test custom async context manager."""
        state = {"entered": False, "exited": False}

        class AsyncCtx:
            async def __aenter__(self):
                await asyncio.sleep(0.001)
                state["entered"] = True
                return self

            async def __aexit__(self, *args):
                await asyncio.sleep(0.001)
                state["exited"] = True

        async def main():
            async with AsyncCtx():
                assert state["entered"]
                assert not state["exited"]

        asyncio.run(main())
        assert state["exited"]

    def test_asynccontextmanager_decorator(self):
        """Test @asynccontextmanager decorator."""
        from contextlib import asynccontextmanager

        @asynccontextmanager
        async def managed():
            await asyncio.sleep(0.001)
            yield "resource"
            await asyncio.sleep(0.001)

        async def main():
            async with managed() as r:
                return r

        result = asyncio.run(main())
        assert result == "resource"


class TestSynchronization:
    """Test asyncio synchronization primitives."""

    def test_lock(self):
        """Test asyncio.Lock."""

        async def main():
            lock = asyncio.Lock()
            counter = [0]

            async def increment():
                async with lock:
                    current = counter[0]
                    await asyncio.sleep(0.001)
                    counter[0] = current + 1

            await asyncio.gather(*[increment() for _ in range(10)])
            return counter[0]

        result = asyncio.run(main())
        assert result == 10

    def test_semaphore(self):
        """Test asyncio.Semaphore for rate limiting."""

        async def main():
            semaphore = asyncio.Semaphore(2)
            concurrent = [0]
            max_concurrent = [0]

            async def task():
                async with semaphore:
                    concurrent[0] += 1
                    max_concurrent[0] = max(max_concurrent[0], concurrent[0])
                    await asyncio.sleep(0.01)
                    concurrent[0] -= 1

            await asyncio.gather(*[task() for _ in range(5)])
            return max_concurrent[0]

        max_conc = asyncio.run(main())
        assert max_conc <= 2

    def test_event(self):
        """Test asyncio.Event for signaling."""

        async def main():
            event = asyncio.Event()
            results = []

            async def waiter(name):
                await event.wait()
                results.append(name)

            async def setter():
                await asyncio.sleep(0.01)
                event.set()

            await asyncio.gather(waiter("A"), waiter("B"), setter())
            return results

        results = asyncio.run(main())
        assert set(results) == {"A", "B"}


class TestQueue:
    """Test asyncio queues."""

    def test_queue(self):
        """Test asyncio.Queue."""

        async def main():
            queue = asyncio.Queue()
            results = []

            async def producer():
                for i in range(3):
                    await queue.put(i)

            async def consumer():
                for _ in range(3):
                    item = await queue.get()
                    results.append(item)
                    queue.task_done()

            await asyncio.gather(producer(), consumer())
            return results

        results = asyncio.run(main())
        assert results == [0, 1, 2]

    def test_priority_queue(self):
        """Test asyncio.PriorityQueue."""

        async def main():
            queue = asyncio.PriorityQueue()

            await queue.put((3, "low"))
            await queue.put((1, "high"))
            await queue.put((2, "medium"))

            results = []
            while not queue.empty():
                _, item = await queue.get()
                results.append(item)
            return results

        results = asyncio.run(main())
        assert results == ["high", "medium", "low"]


class TestExceptionHandling:
    """Test exception handling in asyncio."""

    def test_task_exception(self):
        """Test exception propagation from tasks."""

        async def failing():
            raise ValueError("test error")

        async def main():
            task = asyncio.create_task(failing())
            await task

        with pytest.raises(ValueError, match="test error"):
            asyncio.run(main())

    def test_gather_return_exceptions(self):
        """Test gather with return_exceptions."""

        async def ok():
            return "ok"

        async def fail():
            raise ValueError("error")

        async def main():
            return await asyncio.gather(ok(), fail(), return_exceptions=True)

        results = asyncio.run(main())
        assert results[0] == "ok"
        assert isinstance(results[1], ValueError)


class TestCancellation:
    """Test task cancellation."""

    def test_cancel_task(self):
        """Test cancelling a task."""

        async def main():
            cleanup_done = [False]

            async def long_running():
                try:
                    await asyncio.sleep(10)
                except asyncio.CancelledError:
                    cleanup_done[0] = True
                    raise

            task = asyncio.create_task(long_running())
            await asyncio.sleep(0.01)
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                pass

            return cleanup_done[0]

        result = asyncio.run(main())
        assert result


class TestExecutor:
    """Test running blocking code in executor."""

    def test_run_in_executor(self):
        """Test run_in_executor for blocking code."""
        import time

        def blocking():
            time.sleep(0.01)
            return "done"

        async def main():
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, blocking)

        result = asyncio.run(main())
        assert result == "done"


class TestSubprocess:
    """Test asyncio subprocess."""

    def test_subprocess(self):
        """Test running subprocess."""

        async def main():
            proc = await asyncio.create_subprocess_shell(
                "echo hello",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await proc.communicate()
            return stdout.decode().strip(), proc.returncode

        output, code = asyncio.run(main())
        assert output == "hello"
        assert code == 0


class TestTimeout:
    """Test timeout patterns."""

    def test_wait_for_timeout(self):
        """Test asyncio.wait_for timeout."""

        async def slow():
            await asyncio.sleep(10)

        async def main():
            try:
                await asyncio.wait_for(slow(), timeout=0.01)
                return False
            except asyncio.TimeoutError:
                return True

        result = asyncio.run(main())
        assert result
