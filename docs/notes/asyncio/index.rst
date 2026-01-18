.. meta::
    :description lang=en: Python asyncio tutorial covering coroutines, event loops, tasks, async/await syntax, networking, and asynchronous programming patterns
    :keywords: Python, Python3, asyncio, async, await, coroutine, event loop, asynchronous, concurrent, networking, TCP, UDP

Asyncio
=======

Python's ``asyncio`` module provides infrastructure for writing single-threaded
concurrent code using coroutines, multiplexing I/O access over sockets and other
resources, running network clients and servers, and other related primitives.
Unlike threading, asyncio uses cooperative multitasking, where tasks voluntarily
yield control to allow other tasks to run. This makes it ideal for I/O-bound
applications like web servers, database clients, and network services where
waiting for external resources is the primary bottleneck.

This section covers asyncio from basic concepts to advanced patterns, including
the event loop, coroutines, tasks, synchronization primitives, and real-world
examples like TCP/UDP servers, HTTP clients, and connection pools.

.. toctree::
   :maxdepth: 1

   python-asyncio-guide
   python-asyncio-basic
   python-asyncio-server
   python-asyncio-advanced
