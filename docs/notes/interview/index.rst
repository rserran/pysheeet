===========================
Python Interview Cheatsheet
===========================

.. meta::
    :description lang=en: Curated Python interview questions, each linking directly to the exact cheatsheet section that answers it. Covers core language fundamentals, data structures, functions and decorators, iterators and generators, OOP and dunder methods, concurrency and the GIL, asyncio, common gotchas, C extensions, databases, networking, and security.
    :keywords: Python interview questions, Python cheat sheet, GIL, asyncio, threading, multiprocessing, generators, decorators, closures, mutable default arguments, MRO, metaclasses, dunder methods, slots, dataclass, context managers, descriptors, SQLAlchemy, ctypes, Python C API, Python security

This page is a curated, question-indexed map into the rest of the cheatsheet.
Each entry is a question you are likely to see in a Python interview, followed
by a link that jumps directly to the section of the notes that answers it.
It is intentionally a navigation layer — the actual explanations, code, and
caveats live in the linked sections.

Use it two ways:

* **Drilling a topic:** pick a group (e.g. *Asyncio*) and walk every question.
* **Quick review before an interview:** read the questions, and for any you
  cannot confidently answer in one or two sentences, click through.

Python Language Fundamentals
============================

* What does ``from __future__ import ...`` do, and which future imports still
  matter? :ref:`→ basic/python-future: Print Function <notes/basic/python-future:Print Function>` ·
  :ref:`Division <notes/basic/python-future:Division>` ·
  :ref:`Annotations <notes/basic/python-future:Annotations>`
* What is ``Ellipsis`` (``...``) used for in modern Python?
  :ref:`→ basic/python-basic: Ellipsis <notes/basic/python-basic:Ellipsis>`
* How do ``for``/``while`` ``... else`` clauses work?
  :ref:`→ basic/python-basic: for ... else ... <notes/basic/python-basic:for ... else ...>` ·
  :ref:`while ... else ... <notes/basic/python-basic:while ... else ...>`
* What does ``try ... except ... else`` do that a plain ``try ... except``
  does not?
  :ref:`→ basic/python-basic: try ... except ... else ... <notes/basic/python-basic:try ... except ... else ...>`
* How does Python handle Unicode vs bytes, and what is a code point?
  :ref:`→ basic/python-unicode: Characters <notes/basic/python-unicode:Characters>` ·
  :ref:`Unicode Code Point <notes/basic/python-unicode:Unicode Code Point>`

Data Structures & Collections
=============================

* What is the difference between a shallow copy and a deep copy of a list?
  :ref:`→ basic/python-list: Copy Lists <notes/basic/python-list:Copy Lists: Shallow vs Deep Copy>`
* Why can ``[[]] * n`` surprise you?
  :ref:`→ basic/python-list: Initialize Lists with Multiplication Operator <notes/basic/python-list:Initialize Lists with Multiplication Operator>`
* What is a list comprehension, and when is a generator expression better?
  :ref:`→ basic/python-list: List Comprehensions <notes/basic/python-list:Create Lists with List Comprehensions>`
* How do you get ``(index, value)`` pairs while iterating?
  :ref:`→ basic/python-list: enumerate() <notes/basic/python-list:Iterate with Index Using enumerate()>`
* How is a dict iterated, and what does ``dict.items()`` / ``dict.keys()``
  return?
  :ref:`→ basic/python-dict: dict.keys() <notes/basic/python-dict:Get All Keys with \`\`dict.keys()\`\`>` ·
  :ref:`dict.items() <notes/basic/python-dict:Get Key-Value Pairs with \`\`dict.items()\`\`>`
* ``dict.setdefault`` vs ``collections.defaultdict`` — which fits which use
  case?
  :ref:`→ basic/python-dict: setdefault and defaultdict <notes/basic/python-dict:Set Default Values with \`\`setdefault()\`\` and \`\`defaultdict\`\`>`
* How do you merge two dicts (pre-3.9 and post-3.9)?
  :ref:`→ basic/python-dict: Merge Two Dictionaries in Python <notes/basic/python-dict:Merge Two Dictionaries in Python>`
* How would you implement an LRU cache from scratch?
  :ref:`→ basic/python-dict: Implement LRU Cache with OrderedDict <notes/basic/python-dict:Implement LRU Cache with OrderedDict>`
* How do you dedupe a list while preserving order?
  :ref:`→ basic/python-set: Remove Duplicates from a List <notes/basic/python-set:Remove Duplicates from a List>`
* When would you use ``heapq`` instead of sorting?
  :ref:`→ basic/python-heap: Basic Heap Operations <notes/basic/python-heap:Basic Heap Operations>` ·
  :ref:`Priority Queue <notes/basic/python-heap:Implement Priority Queue with \`\`heapq\`\`>`
* How do you emulate a dict-like object with dunder methods?
  :ref:`→ basic/python-dict: Emulate a Dictionary with Special Methods <notes/basic/python-dict:Emulate a Dictionary with Special Methods>`

Functions & Decorators
======================

* What do ``*args`` and ``**kwargs`` really do, and how do you forward them?
  :ref:`→ basic/python-func: Variable Arguments <notes/basic/python-func:Variable Arguments \`\`*args\`\` and \`\`**kwargs\`\`>` ·
  :ref:`Unpack Arguments <notes/basic/python-func:Unpack Arguments>`
* What is the difference between keyword-only and positional-only arguments?
  :ref:`→ basic/python-func: Keyword-Only Arguments <notes/basic/python-func:Keyword-Only Arguments>` ·
  :ref:`Positional-Only Arguments <notes/basic/python-func:Positional-Only Arguments>`
* What is a closure, and what does it capture?
  :ref:`→ basic/python-func: Closure <notes/basic/python-func:Closure>`
* How do decorators work, and how do you write one that takes arguments?
  :ref:`→ basic/python-func: Decorator <notes/basic/python-func:Decorator>` ·
  :ref:`Decorator with Arguments <notes/basic/python-func:Decorator with Arguments>`
* ``functools.lru_cache`` vs ``functools.partial`` — what do they do?
  :ref:`→ basic/python-func: lru_cache <notes/basic/python-func:Cache with \`\`lru_cache\`\`>` ·
  :ref:`Partial Functions <notes/basic/python-func:Partial Functions>`
* How does ``functools.singledispatch`` implement function overloading?
  :ref:`→ basic/python-func: singledispatch <notes/basic/python-func:\`\`singledispatch\`\` - Function Overloading>`

Iterators & Generators
======================

* Generator function vs generator expression — when is each idiomatic?
  :ref:`→ basic/python-generator: Generator Function vs Generator Expression <notes/basic/python-generator:Generator Function vs Generator Expression>`
* How do you send a value into a running generator?
  :ref:`→ basic/python-generator: Send Values to Generator <notes/basic/python-generator:Send Values to Generator>`
* What does ``yield from`` do, and how does it compose generators?
  :ref:`→ basic/python-generator: yield from Expression <notes/basic/python-generator:yield from Expression>` ·
  :ref:`yield from with Return <notes/basic/python-generator:yield from with Return>`
* How do you build an iterable class with a generator method?
  :ref:`→ basic/python-generator: Iterable Class via Generator <notes/basic/python-generator:Iterable Class via Generator>`
* How do you implement a context manager as a generator with
  ``@contextmanager``?
  :ref:`→ basic/python-generator: Context Manager via Generator <notes/basic/python-generator:Context Manager via Generator>` ·
  :ref:`What @contextmanager does <notes/basic/python-generator:What \`\`@contextmanager\`\` Does>`
* What is an async generator, and how does it differ from a normal generator?
  :ref:`→ basic/python-generator: Async Generator <notes/basic/python-generator:Async Generator (Python 3.6+)>`

Classes & OOP
=============

* ``__new__`` vs ``__init__`` — when does each run?
  :ref:`→ basic/python-object: __new__ vs __init__ <notes/basic/python-object:__new__ vs __init__>`
* ``__str__`` vs ``__repr__`` — who calls which?
  :ref:`→ basic/python-object: __str__ and __repr__ <notes/basic/python-object:__str__ and __repr__>`
* How does the descriptor protocol work?
  :ref:`→ basic/python-object: Descriptor Protocol <notes/basic/python-object:Descriptor Protocol>`
* What is the context manager protocol (``__enter__`` / ``__exit__``)?
  :ref:`→ basic/python-object: Context Manager Protocol <notes/basic/python-object:Context Manager Protocol>`
* ``@staticmethod`` vs ``@classmethod`` — when to use which?
  :ref:`→ basic/python-object: staticmethod and classmethod <notes/basic/python-object:@staticmethod and @classmethod>`
* What is MRO, and how does C3 linearization resolve the diamond problem?
  :ref:`→ basic/python-object: The Diamond Problem (MRO) <notes/basic/python-object:The Diamond Problem (MRO)>`
* When should you define ``__slots__``?
  :ref:`→ basic/python-object: __slots__ <notes/basic/python-object:Using __slots__>`
* How do you define a class at runtime with ``type(...)``?
  :ref:`→ basic/python-object: Declare Class with type() <notes/basic/python-object:Declare Class with type()>`
* What are abstract base classes, and how does ``abc`` enforce them?
  :ref:`→ basic/python-object: Abstract Base Classes <notes/basic/python-object:Abstract Base Classes with abc>`
* How do you implement a callable object?
  :ref:`→ basic/python-object: Callable with __call__ <notes/basic/python-object:Callable with __call__>`
* What does ``@property`` buy you over plain getters/setters?
  :ref:`→ basic/python-object: @property Decorator <notes/basic/python-object:@property Decorator>`

Concurrency
===========

* What is the GIL, and how does it affect CPU-bound vs I/O-bound code?
  :ref:`→ concurrency/python-threading: Understanding the GIL <notes/concurrency/python-threading:Understanding the GIL>`
* Threading vs multiprocessing — when would you reach for each?
  :ref:`→ concurrency/python-threading: Creating Threads <notes/concurrency/python-threading:Creating Threads>` ·
  :ref:`multiprocessing: Creating Processes <notes/concurrency/python-multiprocessing:Creating Processes>`
* ``Lock`` vs ``RLock`` — what is the difference?
  :ref:`→ concurrency/python-threading: Lock <notes/concurrency/python-threading:Lock - Mutual Exclusion>` ·
  :ref:`RLock <notes/concurrency/python-threading:RLock - Reentrant Lock>`
* How do you synchronize with ``Event``, ``Condition``, or ``Barrier``?
  :ref:`→ concurrency/python-threading: Event <notes/concurrency/python-threading:Event - Thread Signaling>` ·
  :ref:`Condition <notes/concurrency/python-threading:Condition - Complex Synchronization>` ·
  :ref:`Barrier <notes/concurrency/python-threading:Barrier - Synchronization Point>`
* How would you build a producer-consumer pipeline with ``queue.Queue``?
  :ref:`→ concurrency/python-threading: Producer-Consumer with Queue <notes/concurrency/python-threading:Producer-Consumer with Queue>`
* What is a deadlock, and how do you prevent one?
  :ref:`→ concurrency/python-threading: Deadlock Example and Prevention <notes/concurrency/python-threading:Deadlock Example and Prevention>`
* How do you share state across processes (Queue, Pipe, Value, Manager)?
  :ref:`→ concurrency/python-multiprocessing: Sharing Data with Queue <notes/concurrency/python-multiprocessing:Sharing Data with Queue>` ·
  :ref:`Shared Memory <notes/concurrency/python-multiprocessing:Shared Memory with Value and Array>` ·
  :ref:`Manager <notes/concurrency/python-multiprocessing:Manager for Complex Shared Objects>`
* ``ThreadPoolExecutor`` vs ``ProcessPoolExecutor`` — how do you pick?
  :ref:`→ concurrency/python-futures: ThreadPoolExecutor <notes/concurrency/python-futures:ThreadPoolExecutor Basics>` ·
  :ref:`ProcessPoolExecutor <notes/concurrency/python-futures:ProcessPoolExecutor Basics>`
* How do you process results from many futures as they complete?
  :ref:`→ concurrency/python-futures: as_completed <notes/concurrency/python-futures:Processing Results as They Complete>`

Asyncio
=======

* What actually happens when you call ``asyncio.run(coro())``?
  :ref:`→ asyncio/python-asyncio-basic: asyncio.run <notes/asyncio/python-asyncio-basic:Running Coroutines with asyncio.run>`
* ``asyncio.create_task`` vs awaiting a coroutine directly — what is the
  difference?
  :ref:`→ asyncio/python-asyncio-basic: Tasks <notes/asyncio/python-asyncio-basic:Creating and Managing Tasks>`
* How do ``asyncio.gather`` and ``asyncio.wait`` differ?
  :ref:`→ asyncio/python-asyncio-basic: gather <notes/asyncio/python-asyncio-basic:Gathering Multiple Coroutines>` ·
  :ref:`wait for first completed <notes/asyncio/python-asyncio-basic:Waiting for First Completed>`
* How do you time-bound an awaitable?
  :ref:`→ asyncio/python-asyncio-basic: Waiting with Timeout <notes/asyncio/python-asyncio-basic:Waiting with Timeout>`
* What is an async context manager, and how do you write one?
  :ref:`→ asyncio/python-asyncio-basic: Async Context Managers <notes/asyncio/python-asyncio-basic:Asynchronous Context Managers>` ·
  :ref:`@asynccontextmanager <notes/asyncio/python-asyncio-basic:Using @asynccontextmanager>`
* How do you call blocking code from an async function without blocking the
  loop?
  :ref:`→ asyncio/python-asyncio-basic: Running Blocking Code in Executor <notes/asyncio/python-asyncio-basic:Running Blocking Code in Executor>`
* How do you handle exceptions raised inside tasks?
  :ref:`→ asyncio/python-asyncio-basic: Exception Handling in Tasks <notes/asyncio/python-asyncio-basic:Exception Handling in Tasks>`
* How do you rate-limit concurrency in asyncio?
  :ref:`→ asyncio/python-asyncio-advanced: Semaphores <notes/asyncio/python-asyncio-advanced:Semaphores for Rate Limiting>`
* What is a graceful shutdown in asyncio?
  :ref:`→ asyncio/python-asyncio-advanced: Graceful Shutdown <notes/asyncio/python-asyncio-advanced:Graceful Shutdown>`
* Conceptually, what is a coroutine and how does the event loop drive it?
  :ref:`→ asyncio/python-asyncio-guide: What is a Coroutine? <notes/asyncio/python-asyncio-guide:What is a Coroutine?>` ·
  :ref:`Event Loop <notes/asyncio/python-asyncio-guide:Event Loop>`

Common Gotchas
==============

* Why is using a mutable default argument (``def f(x=[])``) dangerous?
  :ref:`→ basic/python-func: Default Arguments <notes/basic/python-func:Default Arguments>`

C Extensions & Interop
======================

* How do you write a C extension module with the CPython C API?
  :ref:`→ extension/python-capi: Simple C Extension <notes/extension/python-capi:Simple C Extension>` ·
  :ref:`Parse Arguments <notes/extension/python-capi:Parse Arguments>`
* How and why do you release the GIL in a C extension?
  :ref:`→ extension/python-capi: Release the GIL <notes/extension/python-capi:Release the GIL>`
* How do you call into a shared library with ``ctypes``?
  :ref:`→ extension/python-ctypes: Loading Shared Libraries <notes/extension/python-ctypes:Loading Shared Libraries>` ·
  :ref:`Basic Type Mapping <notes/extension/python-ctypes:Basic Type Mapping>`

Networking
==========

* How do you resolve a hostname to an IP in Python?
  :ref:`→ network/python-socket: Address Info (DNS Resolution) <notes/network/python-socket:Get Address Info (DNS Resolution)>`
* Network byte order — when and why do you need ``htons`` / ``ntohs``?
  :ref:`→ network/python-socket: Network Byte Order Conversion <notes/network/python-socket:Network Byte Order Conversion>`
* How do you build a minimal TLS echo server and client?
  :ref:`→ network/python-socket-ssl: Simple TLS Echo Server <notes/network/python-socket-ssl:Simple TLS Echo Server>` ·
  :ref:`TLS Client <notes/network/python-socket-ssl:TLS Client>`
* What is mutual TLS (mTLS), and why would a service require it?
  :ref:`→ network/python-socket-ssl: Mutual TLS (mTLS) <notes/network/python-socket-ssl:Mutual TLS (mTLS)>`

Databases
=========

* What does a SQLAlchemy engine actually hold, and how do connections work?
  :ref:`→ database/python-sqlalchemy: Create an Engine <notes/database/python-sqlalchemy:Create an Engine>` ·
  :ref:`Database URL Format <notes/database/python-sqlalchemy:Database URL Format>`
* How do you run raw SQL safely with parameters?
  :ref:`→ database/python-sqlalchemy: Connect and Execute Raw SQL <notes/database/python-sqlalchemy:Connect and Execute Raw SQL>`
* Transactions in SQLAlchemy — who commits, and when?
  :ref:`→ database/python-sqlalchemy: Transaction Management <notes/database/python-sqlalchemy:Transaction Management>`
* Core vs ORM — what does the ORM add on top?
  :ref:`→ database/python-sqlalchemy-orm: Declarative Base <notes/database/python-sqlalchemy-orm:Define Models with Declarative Base>` ·
  :ref:`Session Basics <notes/database/python-sqlalchemy-orm:Session Basics>`

Security & Crypto
=================

* What are the common cryptographic mistakes to avoid?
  :ref:`→ security/python-crypto: Common Mistakes <notes/security/python-crypto:Common Mistakes (Don't Do This)>` ·
  :ref:`Security Checklist <notes/security/python-crypto:Security Checklist>`
* Why should you prefer ``secrets`` over ``random`` for tokens?
  :ref:`→ security/python-crypto: Secure Random Generation <notes/security/python-crypto:Secure Random Generation>` ·
  :ref:`Weak Random <notes/security/python-vulnerability:Weak Random Number Generation>`
* What is a timing attack, and how do you defend against one?
  :ref:`→ security/python-vulnerability: Timing Attacks <notes/security/python-vulnerability:Timing Attacks on String Comparison>`
* How does SQL injection happen in Python, and how is it prevented?
  :ref:`→ security/python-vulnerability: SQL Injection <notes/security/python-vulnerability:SQL Injection>`

See Also
========

If a question above is not covered, the top-level indices are the best next
stop:

* :doc:`../basic/index` — Python core language and data structures
* :doc:`../concurrency/index` — Threading, multiprocessing, futures
* :doc:`../asyncio/index` — Asyncio and async patterns
* :doc:`../network/index` — Sockets and SSL/TLS
* :doc:`../database/index` — SQLAlchemy core and ORM
* :doc:`../security/index` — Cryptography and common vulnerabilities
* :doc:`../extension/index` — C extensions and FFI
