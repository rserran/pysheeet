.. meta::
    :description lang=en: Python concurrency tutorial covering threading, multiprocessing, locks, semaphores, queues, process pools, and concurrent.futures
    :keywords: Python, Python3, threading, multiprocessing, concurrency, parallel, lock, semaphore, queue, ThreadPoolExecutor, ProcessPoolExecutor, GIL

Concurrency
===========

Python provides multiple approaches for concurrent execution to handle CPU-bound
and I/O-bound tasks efficiently. The ``threading`` module enables lightweight
concurrent execution within a single process, while ``multiprocessing`` bypasses
the Global Interpreter Lock (GIL) by using separate processes for true parallelism.
The ``concurrent.futures`` module offers a high-level interface that abstracts
the differences between threads and processes behind a unified API.

Understanding when to use each approach is crucial: threads excel at I/O-bound
tasks (network requests, file operations) where the GIL is released during
waiting, while processes are better for CPU-bound tasks (computation, data
processing) where true parallel execution is needed.

.. toctree::
   :maxdepth: 1

   python-threading
   python-multiprocessing
   python-futures
