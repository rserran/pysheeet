.. meta::
    :description lang=en: Python generator cheat sheet covering generator functions, generator expressions, yield, yield from, send, async generators, and coroutines with code examples
    :keywords: Python, Python3, Python generator, Python generator cheat sheet, yield, yield from, generator expression, async generator, iterator, coroutine, contextmanager

=========
Generator
=========

.. contents:: Table of Contents
    :backlinks: none

Generators are a powerful feature in Python for creating iterators. They allow
you to iterate over data without storing the entire sequence in memory, making
them ideal for processing large datasets or infinite sequences. This cheat sheet
covers generator functions, generator expressions, ``yield``, ``yield from``,
sending values to generators, and async generators.

Generator Function vs Generator Expression
------------------------------------------

A generator function is defined like a normal function but uses ``yield`` to
produce a sequence of values. When called, it returns a generator object that
can be iterated over. A generator expression is a compact syntax similar to
list comprehensions but produces values lazily on demand.

.. code-block:: python

    # generator function
    >>> def gen_func():
    ...     yield 5566
    ...
    >>> g = gen_func()
    >>> g
    <generator object gen_func at 0x...>
    >>> next(g)
    5566

    # generator expression
    >>> g = (x for x in range(3))
    >>> next(g)
    0
    >>> next(g)
    1

Yield Values from Generator
---------------------------

The ``yield`` statement produces a value and suspends the generator's execution.
When ``next()`` is called again, execution resumes from where it left off. This
example generates prime numbers by checking divisibility for each candidate.

.. code-block:: python

    >>> def prime(n):
    ...     p = 2
    ...     while n > 0:
    ...         for x in range(2, p):
    ...             if p % x == 0:
    ...                 break
    ...         else:
    ...             yield p
    ...             n -= 1
    ...         p += 1
    ...
    >>> list(prime(5))
    [2, 3, 5, 7, 11]

Unpack Generators
-----------------

Python 3.5+ (PEP 448) allows unpacking generators directly into lists, sets,
function arguments, and variables using the ``*`` operator. This provides a
convenient way to consume generator values without explicit iteration.

.. code-block:: python

    # PEP 448 - unpacking inside a list
    >>> g1 = (x for x in range(3))
    >>> g2 = (x**2 for x in range(2))
    >>> [1, *g1, 2, *g2]
    [1, 0, 1, 2, 2, 0, 1]

    # unpacking inside a set
    >>> g = (x for x in [5, 5, 6, 6])
    >>> {*g}
    {5, 6}

    # unpacking to variables
    >>> g = (x for x in range(3))
    >>> a, b, c = g
    >>> a, b, c
    (0, 1, 2)

    # extended unpacking
    >>> g = (x for x in range(6))
    >>> a, b, *c, d = g
    >>> a, b, d
    (0, 1, 5)
    >>> c
    [2, 3, 4]

    # unpacking inside a function
    >>> print(*(x for x in range(3)))
    0 1 2

Iterable Class via Generator
----------------------------

You can make a class iterable by implementing ``__iter__`` as a generator method.
This approach is cleaner than implementing a separate iterator class. The
``__reversed__`` method can also be implemented as a generator to support the
built-in ``reversed()`` function.

.. code-block:: python

    >>> class Count:
    ...     def __init__(self, n):
    ...         self._n = n
    ...     def __iter__(self):
    ...         n = self._n
    ...         while n > 0:
    ...             yield n
    ...             n -= 1
    ...     def __reversed__(self):
    ...         n = 1
    ...         while n <= self._n:
    ...             yield n
    ...             n += 1
    ...
    >>> list(Count(5))
    [5, 4, 3, 2, 1]
    >>> list(reversed(Count(5)))
    [1, 2, 3, 4, 5]

Send Values to Generator
------------------------

Generators can receive values through the ``send()`` method. The sent value
becomes the result of the ``yield`` expression inside the generator. Before
sending values, you must start the generator by calling ``next()`` or
``send(None)`` to advance it to the first ``yield``.

.. code-block:: python

    >>> def spam():
    ...     msg = yield
    ...     print("Message:", msg)
    ...
    >>> g = spam()
    >>> next(g)  # start generator
    >>> try:
    ...     g.send("Hello World!")
    ... except StopIteration:
    ...     pass
    Message: Hello World!

yield from Expression
---------------------

The ``yield from`` expression delegates iteration to another generator or
iterable. It automatically handles forwarding ``send()``, ``throw()``, and
``close()`` calls to the subgenerator, making it ideal for creating generator
pipelines and recursive generators.

.. code-block:: python

    >>> def subgen():
    ...     try:
    ...         yield 9527
    ...     except ValueError:
    ...         print("got ValueError")
    ...
    >>> def delegating_gen():
    ...     yield from subgen()
    ...
    >>> g = delegating_gen()
    >>> next(g)
    9527
    >>> try:
    ...     g.throw(ValueError)
    ... except StopIteration:
    ...     pass
    got ValueError

You can chain multiple ``yield from`` expressions together. The
``inspect.getgeneratorstate()`` function helps track the generator's lifecycle
through its states: GEN_CREATED, GEN_RUNNING, GEN_SUSPENDED, and GEN_CLOSED.

.. code-block:: python

    # yield from + yield from
    >>> import inspect
    >>> def subgen():
    ...     yield from range(3)
    ...
    >>> def delegating_gen():
    ...     yield from subgen()
    ...
    >>> g = delegating_gen()
    >>> inspect.getgeneratorstate(g)
    'GEN_CREATED'
    >>> next(g)
    0
    >>> inspect.getgeneratorstate(g)
    'GEN_SUSPENDED'
    >>> g.close()
    >>> inspect.getgeneratorstate(g)
    'GEN_CLOSED'

yield from with Return
----------------------

Generators can return a value using the ``return`` statement. The returned value
is accessible through the ``value`` attribute of the ``StopIteration`` exception.
When using ``yield from``, the return value of the subgenerator becomes the value
of the ``yield from`` expression.

.. code-block:: python

    >>> def average():
    ...     total = .0
    ...     count = 0
    ...     while True:
    ...         val = yield
    ...         if not val:
    ...             break
    ...         total += val
    ...         count += 1
    ...     return total / count
    ...
    >>> g = average()
    >>> next(g)
    >>> g.send(3)
    >>> g.send(5)
    >>> try:
    ...     g.send(None)
    ... except StopIteration as e:
    ...     print(e.value)
    4.0

.. code-block:: python

    >>> def subgen():
    ...     yield 9527
    ...
    >>> def delegating_gen():
    ...     yield from subgen()
    ...     return 5566
    ...
    >>> g = delegating_gen()
    >>> next(g)
    9527
    >>> try:
    ...     next(g)
    ... except StopIteration as e:
    ...     print(e.value)
    5566

Generate Sequences
------------------

The ``yield from`` expression provides a concise way to yield all values from
an iterable. This is particularly useful for chaining multiple sequences together
or flattening nested structures.

.. code-block:: python

    >>> def chain():
    ...     yield from 'ab'
    ...     yield from range(3)
    ...
    >>> list(chain())
    ['a', 'b', 0, 1, 2]

What ``RES = yield from EXP`` Does
----------------------------------

This snippet shows the simplified equivalent of what ``yield from`` does
internally, as described in PEP 380. It handles iteration, value passing via
``send()``, and captures the return value from the subgenerator.

.. code-block:: python

    # Simplified version (ref: PEP 380)
    >>> def subgen():
    ...     for x in range(3):
    ...         yield x
    ...
    >>> def delegating_gen():
    ...     _i = iter(subgen())
    ...     try:
    ...         _y = next(_i)
    ...     except StopIteration as _e:
    ...         RES = _e.value
    ...     else:
    ...         while True:
    ...             _s = yield _y
    ...             try:
    ...                 _y = _i.send(_s)
    ...             except StopIteration as _e:
    ...                 RES = _e.value
    ...                 break
    ...
    >>> list(delegating_gen())
    [0, 1, 2]

Check Generator Type
--------------------

Use ``types.GeneratorType`` to check if an object is a generator. This is useful
for writing functions that need to handle generators differently from other
iterables.

.. code-block:: python

    >>> from types import GeneratorType
    >>> def gen_func():
    ...     yield 5566
    ...
    >>> isinstance(gen_func(), GeneratorType)
    True

Check Generator State
---------------------

The ``inspect.getgeneratorstate()`` function returns the current state of a
generator. This is helpful for debugging and understanding the generator lifecycle.
The four possible states are: GEN_CREATED (not started), GEN_RUNNING (currently
executing), GEN_SUSPENDED (paused at yield), and GEN_CLOSED (completed or closed).

.. code-block:: python

    >>> import inspect
    >>> def gen_func():
    ...     yield 9527
    ...
    >>> g = gen_func()
    >>> inspect.getgeneratorstate(g)
    'GEN_CREATED'
    >>> next(g)
    9527
    >>> inspect.getgeneratorstate(g)
    'GEN_SUSPENDED'
    >>> g.close()
    >>> inspect.getgeneratorstate(g)
    'GEN_CLOSED'

Context Manager via Generator
-----------------------------

The ``@contextlib.contextmanager`` decorator transforms a generator function into
a context manager. Code before ``yield`` runs on entering the ``with`` block,
and code after ``yield`` (typically in ``finally``) runs on exit. The yielded
value is bound to the variable after ``as``.

.. code-block:: python

    >>> import contextlib
    >>> @contextlib.contextmanager
    ... def mylist():
    ...     try:
    ...         l = [1, 2, 3, 4, 5]
    ...         yield l
    ...     finally:
    ...         print("exit scope")
    ...
    >>> with mylist() as l:
    ...     print(l)
    [1, 2, 3, 4, 5]
    exit scope

What ``@contextmanager`` Does
-----------------------------

This snippet shows a simplified implementation of how ``@contextmanager`` works
internally. It wraps a generator in a class that implements the context manager
protocol (``__enter__`` and ``__exit__``), handling both normal exit and
exception propagation.

.. code-block:: python

    class GeneratorCM:
        def __init__(self, gen):
            self._gen = gen

        def __enter__(self):
            return next(self._gen)

        def __exit__(self, *exc_info):
            try:
                if exc_info[0] is None:
                    next(self._gen)
                else:
                    self._gen.throw(*exc_info)
            except StopIteration:
                return True
            raise

    def contextmanager(func):
        def run(*a, **k):
            return GeneratorCM(func(*a, **k))
        return run

Profile Code Block
------------------

A practical example of using generator-based context managers to measure
execution time of code blocks. The ``yield`` statement marks the boundary
between setup (recording start time) and teardown (calculating elapsed time).

.. code-block:: python

    >>> import time
    >>> from contextlib import contextmanager
    >>> @contextmanager
    ... def profile(msg):
    ...     try:
    ...         s = time.time()
    ...         yield
    ...     finally:
    ...         print(f'{msg} cost: {time.time() - s:.2f}s')
    ...
    >>> with profile('block'):
    ...     time.sleep(0.1)
    block cost: 0.10s

``yield from`` and ``__iter__``
-------------------------------

When using ``yield from`` with a class instance, Python calls the object's
``__iter__`` method to get an iterator. This allows custom classes to work
seamlessly with ``yield from`` delegation, enabling elegant composition of
iterables.

.. code-block:: python

    >>> class FakeGen:
    ...     def __iter__(self):
    ...         n = 0
    ...         while n < 3:
    ...             yield n
    ...             n += 1
    ...     def __reversed__(self):
    ...         n = 2
    ...         while n >= 0:
    ...             yield n
    ...             n -= 1
    ...
    >>> def spam():
    ...     yield from FakeGen()
    ...
    >>> list(spam())
    [0, 1, 2]
    >>> list(reversed(FakeGen()))
    [2, 1, 0]

Closure Using Generator
-----------------------

Generators provide an elegant way to implement closures that maintain state
between calls. Each call to ``next()`` resumes execution and can access and
modify the enclosed variables. This is often cleaner than using ``nonlocal``
or class-based approaches.

.. code-block:: python

    # generator version
    >>> def closure_gen():
    ...     x = 5566
    ...     while True:
    ...         x += 1
    ...         yield x
    ...
    >>> g = closure_gen()
    >>> next(g)
    5567
    >>> next(g)
    5568

Simple Scheduler
----------------

This example demonstrates how generators can be used to implement cooperative
multitasking. Each generator represents a task that yields control back to the
scheduler. The scheduler uses a deque to round-robin between tasks, advancing
each one step at a time.

.. code-block:: python

    >>> from collections import deque
    >>> def fib(n):
    ...     if n <= 2: return 1
    ...     return fib(n-1) + fib(n-2)
    ...
    >>> def g_fib(n):
    ...     for x in range(1, n + 1):
    ...         yield fib(x)
    ...
    >>> q = deque([g_fib(3), g_fib(5)])
    >>> def run():
    ...     while q:
    ...         try:
    ...             t = q.popleft()
    ...             print(next(t))
    ...             q.append(t)
    ...         except StopIteration:
    ...             print("Task done")
    ...
    >>> run()
    1
    1
    1
    1
    2
    2
    Task done
    3
    5
    Task done

Simple Round-Robin with Blocking
--------------------------------

A more advanced scheduler that handles I/O blocking using ``select()``. Tasks
yield tuples indicating what operation they're waiting for ('recv' or 'send')
and which socket. The scheduler moves blocked tasks to wait queues and only
runs them when their I/O is ready. This is the foundation of async I/O frameworks.

.. code-block:: python

    from collections import deque
    from select import select
    import socket

    tasks = deque()
    w_read = {}
    w_send = {}

    def run():
        while any([tasks, w_read, w_send]):
            while not tasks:
                can_r, can_s, _ = select(w_read, w_send, [])
                for _r in can_r:
                    tasks.append(w_read.pop(_r))
                for _w in can_s:
                    tasks.append(w_send.pop(_w))
            try:
                task = tasks.popleft()
                why, what = next(task)
                if why == 'recv':
                    w_read[what] = task
                elif why == 'send':
                    w_send[what] = task
            except StopIteration:
                pass

    def server():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', 5566))
        sock.listen(5)
        while True:
            yield 'recv', sock
            conn, addr = sock.accept()
            tasks.append(client_handler(conn))

    def client_handler(conn):
        while True:
            yield 'recv', conn
            msg = conn.recv(1024)
            if not msg: break
            yield 'send', conn
            conn.send(msg)
        conn.close()

    tasks.append(server())
    run()

Async Generator (Python 3.6+)
-----------------------------

Async generators combine ``async def`` with ``yield`` to create asynchronous
iterators. They can use ``await`` to pause for async operations between yields.
Use ``async for`` to iterate over async generators. This is essential for
streaming data from async sources like network connections or databases.

.. code-block:: python

    >>> import asyncio
    >>> async def slow_gen(n, t):
    ...     for x in range(n):
    ...         await asyncio.sleep(t)
    ...         yield x
    ...
    >>> async def task(n):
    ...     async for x in slow_gen(n, 0.1):
    ...         print(x)
    ...
    >>> asyncio.run(task(3))
    0
    1
    2

Async Generator with try..finally
---------------------------------

Async generators support ``try..finally`` blocks for cleanup, just like regular
generators. The ``finally`` block executes when the generator is closed or
garbage collected, ensuring resources are properly released even if an exception
occurs during iteration.

.. code-block:: python

    >>> import asyncio
    >>> async def agen(t):
    ...     try:
    ...         await asyncio.sleep(t)
    ...         yield 1 / 0
    ...     finally:
    ...         print("finally")
    ...
    >>> async def main():
    ...     try:
    ...         g = agen(0.1)
    ...         await g.__anext__()
    ...     except Exception as e:
    ...         print(repr(e))
    ...
    >>> asyncio.run(main())
    finally
    ZeroDivisionError('division by zero')

Send and Throw to Async Generator
---------------------------------

Async generators support ``asend()`` to send values and ``athrow()`` to throw
exceptions, similar to regular generators. These methods are coroutines that
must be awaited. This enables two-way communication with async generators for
building complex async data pipelines.

.. code-block:: python

    >>> import asyncio
    >>> async def agen(n):
    ...     try:
    ...         for x in range(n):
    ...             await asyncio.sleep(0.1)
    ...             val = yield x
    ...             print(f'got: {val}')
    ...     except RuntimeError as e:
    ...         yield repr(e)
    ...
    >>> async def main():
    ...     g = agen(5)
    ...     ret = await g.asend(None) + await g.asend('foo')
    ...     print(ret)
    ...     ret = await g.athrow(RuntimeError('error'))
    ...     print(ret)
    ...
    >>> asyncio.run(main())
    got: foo
    1
    RuntimeError('error')

Async Comprehension (Python 3.6+)
---------------------------------

PEP 530 introduced async comprehensions, allowing ``async for`` in list, set,
and dict comprehensions. This provides a concise way to collect values from
async generators. You can also use ``if`` clauses to filter values and
conditional expressions for transformations.

.. code-block:: python

    >>> import asyncio
    >>> async def agen(n):
    ...     for x in range(n):
    ...         await asyncio.sleep(0.01)
    ...         yield x
    ...
    >>> async def main():
    ...     ret = [x async for x in agen(5)]
    ...     print(ret)
    ...     ret = [x async for x in agen(5) if x < 3]
    ...     print(ret)
    ...     ret = {f'{x}': x async for x in agen(3)}
    ...     print(ret)
    ...
    >>> asyncio.run(main())
    [0, 1, 2, 3, 4]
    [0, 1, 2]
    {'0': 0, '1': 1, '2': 2}

Simple Async Round-Robin
------------------------

This example shows cooperative multitasking with async generators. Multiple
async generators are scheduled in a deque, and the scheduler awaits each one
in turn using ``__anext__()``. This pattern is useful for interleaving multiple
async data streams fairly.

.. code-block:: python

    >>> import asyncio
    >>> from collections import deque
    >>> async def agen(n):
    ...     for x in range(n):
    ...         await asyncio.sleep(0.1)
    ...         yield x
    ...
    >>> async def main():
    ...     q = deque([agen(3), agen(5)])
    ...     while q:
    ...         try:
    ...             g = q.popleft()
    ...             print(await g.__anext__())
    ...             q.append(g)
    ...         except StopAsyncIteration:
    ...             pass
    ...
    >>> asyncio.run(main())
    0
    0
    1
    1
    2
    2
    3
    4

Async Generator vs Async Iterator Performance
----------------------------------------------

Async generators have better performance than manually implemented async iterators
because they are optimized at the C level in CPython. This benchmark shows that
async generators can be significantly faster for iteration-heavy workloads.

.. code-block:: python

    >>> import time
    >>> import asyncio
    >>> class AsyncIter:
    ...     def __init__(self, n):
    ...         self._n = n
    ...     def __aiter__(self):
    ...         return self
    ...     async def __anext__(self):
    ...         ret = self._n
    ...         if self._n == 0:
    ...             raise StopAsyncIteration
    ...         self._n -= 1
    ...         return ret
    ...
    >>> async def agen(n):
    ...     for i in range(n):
    ...         yield i
    ...
    >>> async def task_agen(n):
    ...     s = time.time()
    ...     async for _ in agen(n): pass
    ...     cost = time.time() - s
    ...     print(f"agen cost time: {cost}")
    ...
    >>> async def task_aiter(n):
    ...     s = time.time()
    ...     async for _ in AsyncIter(n): pass
    ...     cost = time.time() - s
    ...     print(f"aiter cost time: {cost}")
    ...
    >>> n = 10 ** 7
    >>> asyncio.run(task_agen(n))
    agen cost time: 1.2698817253112793
    >>> asyncio.run(task_aiter(n))
    aiter cost time: 4.168368101119995

``yield from == await`` Expression
----------------------------------

Before Python 3.5 introduced ``async``/``await`` syntax, coroutines were
implemented using generators with ``@asyncio.coroutine`` decorator and
``yield from``. The ``await`` keyword is essentially equivalent to ``yield from``
for coroutines. This example shows both the old and new syntax for an echo server.

.. code-block:: python

    import asyncio
    import socket

    loop = asyncio.get_event_loop()
    host = 'localhost'
    port = 5566
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(False)
    sock.bind((host, port))
    sock.listen(10)

    # old syntax (Python 3.4)
    @asyncio.coroutine
    def echo_server():
        while True:
            conn, addr = yield from loop.sock_accept(sock)
            loop.create_task(handler(conn))

    @asyncio.coroutine
    def handler(conn):
        while True:
            msg = yield from loop.sock_recv(conn, 1024)
            if not msg:
                break
            yield from loop.sock_sendall(conn, msg)
        conn.close()

    # new syntax (Python 3.5+)
    async def echo_server():
        while True:
            conn, addr = await loop.sock_accept(sock)
            loop.create_task(handler(conn))

    async def handler(conn):
        while True:
            msg = await loop.sock_recv(conn, 1024)
            if not msg:
                break
            await loop.sock_sendall(conn, msg)
        conn.close()

    loop.create_task(echo_server())
    loop.run_forever()

Simple Compiler Using Generators
--------------------------------

This advanced example from David Beazley demonstrates using generators to
implement a simple expression compiler. It includes a tokenizer, parser, and
evaluator using the visitor pattern with generators for stack-based evaluation.

.. code-block:: python

    import re
    import types
    from collections import namedtuple

    tokens = [
        r'(?P<NUMBER>\d+)',
        r'(?P<PLUS>\+)',
        r'(?P<MINUS>-)',
        r'(?P<TIMES>\*)',
        r'(?P<DIVIDE>/)',
        r'(?P<WS>\s+)']

    Token = namedtuple('Token', ['type', 'value'])
    lex = re.compile('|'.join(tokens))

    def tokenize(text):
        scan = lex.scanner(text)
        gen = (Token(m.lastgroup, m.group())
                for m in iter(scan.match, None) if m.lastgroup != 'WS')
        return gen

    class Node:
        _fields = []
        def __init__(self, *args):
            for attr, value in zip(self._fields, args):
                setattr(self, attr, value)

    class Number(Node):
        _fields = ['value']

    class BinOp(Node):
        _fields = ['op', 'left', 'right']

    def parse(toks):
        lookahead, current = next(toks, None), None

        def accept(*toktypes):
            nonlocal lookahead, current
            if lookahead and lookahead.type in toktypes:
                current, lookahead = lookahead, next(toks, None)
                return True

        def expr():
            left = term()
            while accept('PLUS', 'MINUS'):
                left = BinOp(current.value, left)
                left.right = term()
            return left

        def term():
            left = factor()
            while accept('TIMES', 'DIVIDE'):
                left = BinOp(current.value, left)
                left.right = factor()
            return left

        def factor():
            if accept('NUMBER'):
                return Number(int(current.value))
            else:
                raise SyntaxError()
        return expr()

    class NodeVisitor:
        def visit(self, node):
            stack = [self.genvisit(node)]
            ret = None
            while stack:
                try:
                    node = stack[-1].send(ret)
                    stack.append(self.genvisit(node))
                    ret = None
                except StopIteration as e:
                    stack.pop()
                    ret = e.value
            return ret

        def genvisit(self, node):
            ret = getattr(self, 'visit_' + type(node).__name__)(node)
            if isinstance(ret, types.GeneratorType):
                ret = yield from ret
            return ret

    class Evaluator(NodeVisitor):
        def visit_Number(self, node):
            return node.value

        def visit_BinOp(self, node):
            leftval = yield node.left
            rightval = yield node.right
            if node.op == '+':
                return leftval + rightval
            elif node.op == '-':
                return leftval - rightval
            elif node.op == '*':
                return leftval * rightval
            elif node.op == '/':
                return leftval / rightval

    def evaluate(exp):
        toks = tokenize(exp)
        tree = parse(toks)
        return Evaluator().visit(tree)

    print(evaluate('2 * 3 + 5 / 2'))  # 8.5
    print(evaluate('+'.join([str(x) for x in range(10000)])))  # 49995000
