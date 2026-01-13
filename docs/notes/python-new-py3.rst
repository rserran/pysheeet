.. meta::
    :description lang=en: Collect useful snippets of new features in Python3
    :keywords: Python, Python3, New in Python3

==============
New in Python3
==============

.. contents:: Table of Contents
    :backlinks: none

The source code can be found on `py3.py <https://github.com/crazyguitar/pysheeet/blob/master/src/new_py3/py3.py>`_.

Type Parameter Syntax
----------------------

**New in Python 3.12**

- PEP 695_ - Type Parameter Syntax

Python 3.12 introduces a cleaner, more intuitive syntax for defining generic classes
and functions. Instead of importing ``TypeVar`` and ``Generic`` from the typing module,
you can now use the ``[]`` bracket notation directly in class and function definitions.
This makes generic code more readable and reduces boilerplate significantly.

.. code-block:: python

    # Old way (before Python 3.12)
    from typing import TypeVar, Generic
    T = TypeVar('T')
    class Box(Generic[T]):
        def __init__(self, item: T) -> None:
            self.item = item

    # New way (Python 3.12+)
    class Box[T]:
        def __init__(self, item: T) -> None:
            self.item = item

    # Generic functions
    def first[T](items: list[T]) -> T:
        return items[0]


f-string Improvements
----------------------

**New in Python 3.12**

- PEP 701_ - Syntactic formalization of f-strings

F-strings have been significantly improved in Python 3.12. They now support nested
quotes of the same type, backslash escapes, and multi-line expressions without any
limitations. This makes f-strings much more flexible and eliminates many edge cases
that previously required workarounds.

.. code-block:: python

    >>> songs = ["Take me back to Eden", "&", "Satellite"]
    >>> f"This is the playlist: {", ".join(songs)}"
    'This is the playlist: Take me back to Eden, &, Satellite'

    # Nested quotes now work
    >>> f"He said {"hello"}"
    'He said hello'


Exception Groups
-----------------

**New in Python 3.11**

- PEP 654_ - Exception Groups and except*

Exception groups allow you to raise and handle multiple unrelated exceptions
simultaneously. This is particularly useful for concurrent operations where
multiple tasks might fail independently. The new ``except*`` syntax lets you
handle specific exception types from a group while letting others propagate.

.. code-block:: python

    >>> def raise_multiple():
    ...     raise ExceptionGroup("multiple errors", [
    ...         ValueError("invalid value"),
    ...         TypeError("wrong type"),
    ...     ])
    ...
    >>> try:
    ...     raise_multiple()
    ... except* ValueError as e:
    ...     print(f"ValueError: {e.exceptions}")
    ... except* TypeError as e:
    ...     print(f"TypeError: {e.exceptions}")
    ...
    ValueError: (ValueError('invalid value'),)
    TypeError: (TypeError('wrong type'),)


Structural Pattern Matching
----------------------------

**New in Python 3.10**

- PEP 634_ - Structural Pattern Matching: Specification
- PEP 635_ - Structural Pattern Matching: Motivation and Rationale

Pattern matching provides a powerful way to destructure and match complex data
structures. It's similar to switch statements in other languages but far more
expressive, supporting sequence patterns, mapping patterns, class patterns,
and guards. The wildcard ``_`` matches anything and serves as a default case.

.. code-block:: python

    >>> def http_status(status):
    ...     match status:
    ...         case 200:
    ...             return "OK"
    ...         case 404:
    ...             return "Not Found"
    ...         case 500:
    ...             return "Internal Server Error"
    ...         case _:
    ...             return "Unknown"
    ...
    >>> http_status(200)
    'OK'
    >>> http_status(404)
    'Not Found'

    # Pattern matching with destructuring
    >>> def describe_point(point):
    ...     match point:
    ...         case (0, 0):
    ...             return "Origin"
    ...         case (x, 0):
    ...             return f"On x-axis at {x}"
    ...         case (0, y):
    ...             return f"On y-axis at {y}"
    ...         case (x, y):
    ...             return f"Point at ({x}, {y})"
    ...
    >>> describe_point((0, 0))
    'Origin'
    >>> describe_point((5, 0))
    'On x-axis at 5'


Dictionary Merge
----------------

**New in Python 3.9**

- PEP 584_  - Add Union Operators To dict

The ``|`` operator provides a cleaner, more intuitive way to merge dictionaries.
The ``|=`` operator updates a dictionary in place. This is more readable than
using ``{**a, **b}`` or ``dict.update()`` and follows the pattern of set operations.

.. code-block:: python

    >>> a = {"foo": "Foo"}
    >>> b = {"bar": "Bar"}

    # old way
    >>> {**a, **b}
    {'foo': 'Foo', 'bar': 'Bar'}
    >>> a.update(b)
    >>> a
    {'foo': 'Foo', 'bar': 'Bar'}

    # new way
    >>> a = {"foo": "Foo"}
    >>> a | b
    {'foo': 'Foo', 'bar': 'Bar'}
    >>> a |= b
    >>> a
    {'foo': 'Foo', 'bar': 'Bar'}


Positional-only parameters
---------------------------

**New in Python 3.8**

- PEP 570_ - Python Positional-Only Parameters

Parameters before the ``/`` marker must be passed positionally and cannot be used
as keyword arguments. This gives library authors more flexibility in API design
and allows parameter names to be changed without breaking backward compatibility.

.. code-block:: python

    >>> def f(a, b, /, c, d):
    ...     print(a, b, c, d)
    ...
    >>> f(1, 2, 3, 4)
    1 2 3 4
    >>> f(1, 2, c=3, d=4)
    1 2 3 4
    >>> f(1, b=2, c=3, d=4)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: f() got some positional-only arguments passed as keyword arguments: 'b'


The walrus operator
--------------------

**New in Python 3.8**

- PEP 572_ - Assignment Expressions

The walrus operator ``:=`` allows you to assign values to variables as part of an
expression. This reduces code duplication when you need to both compute a value
and use it in a condition. After completing PEP 572, Guido van Rossum, commonly
known as BDFL, decided to resign as Python's dictator.

.. code-block:: python

    >>> f = (0, 1)
    >>> [(f := (f[1], sum(f)))[0] for i in range(10)]
    [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    # Useful in while loops
    >>> while (line := input("Enter: ")) != "quit":
    ...     print(f"You entered: {line}")

    # Useful in if statements
    >>> if (n := len("hello")) > 3:
    ...     print(f"Length {n} is greater than 3")


Data Classes
-------------

**New in Python 3.7**

- PEP 557_ - Data Classes

Dataclasses automatically generate boilerplate code like ``__init__``, ``__repr__``,
``__eq__``, and optionally ``__hash__`` for classes that primarily store data.
This reduces repetitive code and makes data-holding classes more concise and readable.

Mutable Data Class

.. code-block:: python

    >>> from dataclasses import dataclass
    >>> @dataclass
    ... class DCls(object):
    ...     x: str
    ...     y: str
    ...
    >>> d = DCls("foo", "bar")
    >>> d
    DCls(x='foo', y='bar')
    >>> d = DCls(x="foo", y="baz")
    >>> d
    DCls(x='foo', y='baz')
    >>> d.z = "bar"

Immutable Data Class

.. code-block:: python

    >>> from dataclasses import dataclass
    >>> from dataclasses import FrozenInstanceError
    >>> @dataclass(frozen=True)
    ... class DCls(object):
    ...     x: str
    ...     y: str
    ...
    >>> try:
    ...     d.x = "baz"
    ... except FrozenInstanceError as e:
    ...     print(e)
    ...
    cannot assign to field 'x'
    >>> try:
    ...     d.z = "baz"
    ... except FrozenInstanceError as e:
    ...     print(e)
    ...
    cannot assign to field 'z'


Built-in ``breakpoint()``
--------------------------

**New in Python 3.7**

- PEP 553_ - Built-in breakpoint()

The ``breakpoint()`` function provides a convenient way to drop into the debugger.
It respects the ``PYTHONBREAKPOINT`` environment variable, allowing you to customize
or disable debugging behavior without modifying code.

.. code-block:: python

    >>> for x in range(3):
    ...     print(x)
    ...     breakpoint()
    ...
    0
    > <stdin>(1)<module>()->None
    (Pdb) c
    1
    > <stdin>(1)<module>()->None
    (Pdb) c
    2
    > <stdin>(1)<module>()->None
    (Pdb) c


Core support for typing module and generic types
-------------------------------------------------

**New in Python 3.7**

- PEP 560_ - Core support for typing module and generic types

Python 3.7 added core support for the typing module, making generic types faster
and enabling classes to customize how they're subscripted via ``__class_getitem__``.

Before Python 3.7

.. code-block:: python

    >>> from typing import Generic, TypeVar
    >>> from typing import Iterable
    >>> T = TypeVar('T')
    >>> class C(Generic[T]): ...
    ...
    >>> def func(l: Iterable[C[int]]) -> None:
    ...     for i in l:
    ...         print(i)
    ...
    >>> func([1,2,3])
    1
    2
    3

Python 3.7 or above

.. code-block:: python

    >>> from typing import Iterable
    >>> class C:
    ...     def __class_getitem__(cls, item):
    ...         return f"{cls.__name__}[{item.__name__}]"
    ...
    >>> def func(l: Iterable[C[int]]) -> None:
    ...     for i in l:
    ...         print(i)
    ...
    >>> func([1,2,3])
    1
    2
    3


Variable annotations
--------------------

**New in Python 3.6**

- PEP 526_ - Syntax for Variable Annotations

Variables can now be annotated with types using the ``:`` syntax, even without
immediate assignment. This enables better static analysis and IDE support.

.. code-block:: python

    >>> from typing import List
    >>> x: List[int] = [1, 2, 3]
    >>> x
    [1, 2, 3]

    >>> from typing import List, Dict
    >>> class Cls(object):
    ...     x: List[int] = [1, 2, 3]
    ...     y: Dict[str, str] = {"foo": "bar"}
    ...
    >>> o = Cls()
    >>> o.x
    [1, 2, 3]
    >>> o.y
    {'foo': 'bar'}


f-string
---------

**New in Python 3.6**

- PEP 498_ - Literal String Interpolation

F-strings (formatted string literals) provide a concise and readable way to embed
expressions inside string literals. They are faster than ``%`` formatting and
``str.format()`` because they are evaluated at runtime.

.. code-block:: python

    >>> py = "Python3"
    >>> f'Awesome {py}'
    'Awesome Python3'
    >>> x = [1, 2, 3, 4, 5]
    >>> f'{x}'
    '[1, 2, 3, 4, 5]'
    >>> def foo(x:int) -> int:
    ...     return x + 1
    ...
    >>> f'{foo(0)}'
    '1'
    >>> f'{123.567:1.3}'
    '1.24e+02'


Asynchronous generators
------------------------

**New in Python 3.6**

- PEP 525_ - Asynchronous Generators

Asynchronous generators combine the power of generators with async/await syntax,
allowing you to yield values asynchronously. This is useful for streaming data
from async sources.

.. code-block:: python

    >>> import asyncio
    >>> async def fib(n: int):
    ...     a, b = 0, 1
    ...     for _ in range(n):
    ...         await asyncio.sleep(1)
    ...         yield a
    ...         b, a = a + b , b
    ...
    >>> async def coro(n: int):
    ...     ag = fib(n)
    ...     f = await ag.asend(None)
    ...     print(f)
    ...     f = await ag.asend(None)
    ...     print(f)
    ...
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(coro(5))
    0
    1


Asynchronous comprehensions
----------------------------

**New in Python 3.6**

- PEP 530_ - Asynchronous Comprehensions

Async comprehensions allow using ``async for`` in list, set, dict comprehensions
and generator expressions. You can also use ``await`` expressions within comprehensions.

.. code-block:: python

    >>> import asyncio
    >>> async def fib(n: int):
    ...     a, b = 0, 1
    ...     for _ in range(n):
    ...         await asyncio.sleep(1)
    ...         yield a
    ...         b, a = a + b , b
    ...

    # async for ... else

    >>> async def coro(n: int):
    ...     async for f in fib(n):
    ...         print(f, end=" ")
    ...     else:
    ...         print()
    ...
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(coro(5))
    0 1 1 2 3

    # async for in list

    >>> async def coro(n: int):
    ...     return [f async for f in fib(n)]
    ...
    >>> loop.run_until_complete(coro(5))
    [0, 1, 1, 2, 3]

    # await in list

    >>> async def slowfmt(n: int) -> str:
    ...     await asyncio.sleep(0.5)
    ...     return f'{n}'
    ...
    >>> async def coro(n: int):
    ...     return [await slowfmt(f) async for f in fib(n)]
    ...
    >>> loop.run_until_complete(coro(5))
    ['0', '1', '1', '2', '3']


New dict implementation
------------------------

**New in Python 3.6**

- PEP 468_ - Preserving the order of \*\*kwargs in a function
- PEP 520_ - Preserving Class Attribute Definition Order
- bpo 27350_ - More compact dictionaries with faster iteration

Python 3.6 introduced a new dictionary implementation that uses 20-25% less memory
and preserves insertion order. This was an implementation detail in 3.6 but became
a language guarantee in Python 3.7.

Before Python 3.5

.. code-block:: python

    >>> import sys
    >>> sys.getsizeof({str(i):i for i in range(1000)})
    49248

    >>> d = {'timmy': 'red', 'barry': 'green', 'guido': 'blue'}
    >>> d   # without order-preserving
    {'barry': 'green', 'timmy': 'red', 'guido': 'blue'}

Python 3.6

- Memory usage is smaller than Python 3.5
- Preserve insertion ordered

.. code-block:: python

    >>> import sys
    >>> sys.getsizeof({str(i):i for i in range(1000)})
    36968

    >>> d = {'timmy': 'red', 'barry': 'green', 'guido': 'blue'}
    >>> d   # preserve insertion ordered
    {'timmy': 'red', 'barry': 'green', 'guido': 'blue'}


``async`` and ``await`` syntax
-------------------------------

**New in Python 3.5**

- PEP 492_ - Coroutines with async and await syntax

The ``async`` and ``await`` keywords provide native syntax for writing coroutines,
making asynchronous code much more readable than the previous generator-based approach.
This is the foundation of modern Python async programming.

Before Python 3.5

.. code-block:: python

    >>> import asyncio
    >>> @asyncio.coroutine
    ... def fib(n: int):
    ...     a, b = 0, 1
    ...     for _ in range(n):
    ...         b, a = a + b, b
    ...     return a
    ...
    >>> @asyncio.coroutine
    ... def coro(n: int):
    ...     for x in range(n):
    ...         yield from asyncio.sleep(1)
    ...         f = yield from fib(x)
    ...         print(f)
    ...
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(coro(3))
    0
    1
    1

Python 3.5 or above

.. code-block:: python

    >>> import asyncio
    >>> async def fib(n: int):
    ...     a, b = 0, 1
    ...     for _ in range(n):
    ...         b, a = a + b, b
    ...     return a
    ...
    >>> async def coro(n: int):
    ...     for x in range(n):
    ...         await asyncio.sleep(1)
    ...         f = await fib(x)
    ...         print(f)
    ...
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(coro(3))
    0
    1
    1


General unpacking
------------------

**New in Python 3.5**

- PEP 448_ - Additional Unpacking Generalizations

Python 3.5 extended the ``*`` and ``**`` unpacking operators to work in more contexts,
including function calls with multiple unpacking operations and in list/dict literals.

Python 2

.. code-block:: python

    >>> def func(*a, **k):
    ...     print(a)
    ...     print(k)
    ...
    >>> func(*[1,2,3,4,5], **{"foo": "bar"})
    (1, 2, 3, 4, 5)
    {'foo': 'bar'}

Python 3

.. code-block:: python

    >>> print(*[1, 2, 3], 4, *[5, 6])
    1 2 3 4 5 6
    >>> [*range(4), 4]
    [0, 1, 2, 3, 4]
    >>> {"foo": "Foo", "bar": "Bar", **{"baz": "baz"}}
    {'foo': 'Foo', 'bar': 'Bar', 'baz': 'baz'}
    >>> def func(*a, **k):
    ...     print(a)
    ...     print(k)
    ...
    >>> func(*[1], *[4,5], **{"foo": "FOO"}, **{"bar": "BAR"})
    (1, 4, 5)
    {'foo': 'FOO', 'bar': 'BAR'}


Matrix multiplication
----------------------

**New in Python 3.5**

- PEP 465_ - A dedicated infix operator for matrix multiplication

The ``@`` operator was added for matrix multiplication, primarily benefiting
scientific computing libraries like NumPy. Classes can implement ``__matmul__``
and ``__imatmul__`` to support this operator.

.. code-block:: python

    >>> # "@" represent matrix multiplication
    >>> class Arr:
    ...     def __init__(self, *arg):
    ...         self._arr = arg
    ...     def __matmul__(self, other):
    ...         if not isinstance(other, Arr):
    ...             raise TypeError
    ...         if len(self) != len(other):
    ...             raise ValueError
    ...         return sum([x*y for x, y in zip(self._arr, other._arr)])
    ...     def __imatmul__(self, other):
    ...         if not isinstance(other, Arr):
    ...             raise TypeError
    ...         if len(self) != len(other):
    ...             raise ValueError
    ...         res = sum([x*y for x, y in zip(self._arr, other._arr)])
    ...         self._arr = [res]
    ...         return self
    ...     def __len__(self):
    ...         return len(self._arr)
    ...     def __str__(self):
    ...         return self.__repr__()
    ...     def __repr__(self):
    ...         return "Arr({})".format(repr(self._arr))
    ...
    >>> a = Arr(9, 5, 2, 7)
    >>> b = Arr(5, 5, 6, 6)
    >>> a @ b  # __matmul__
    124
    >>> a @= b  # __imatmul__
    >>> a
    Arr([124])


Format byte string
-------------------

**New in Python 3.5**

- PEP 461_ - Adding ``%`` formatting to bytes and bytearray

The ``%`` formatting operator now works with bytes and bytearray objects,
making it easier to work with binary protocols and formats.

.. code-block:: python

    >>> b'abc %b %b' % (b'foo', b'bar')
    b'abc foo bar'
    >>> b'%d %f' % (1, 3.14)
    b'1 3.140000'
    >>> class Cls(object):
    ...     def __repr__(self):
    ...         return "repr"
    ...     def __str__(self):
    ...         return "str"
    ...
    'repr'
    >>> b'%a' % Cls()
    b'repr'


Suppressing exception
----------------------

**New in Python 3.3**

- PEP 409_ - Suppressing exception context

When re-raising exceptions, Python shows the chain of exceptions by default.
Using ``raise ... from None`` suppresses the context, showing only the new exception.

Without ``raise Exception from None``

.. code-block:: python

    >>> def func():
    ...     try:
    ...         1 / 0
    ...     except ZeroDivisionError:
    ...         raise ArithmeticError
    ...
    >>> func()
    Traceback (most recent call last):
      File "<stdin>", line 3, in func
    ZeroDivisionError: division by zero

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 5, in func
    ArithmeticError

With ``raise Exception from None``

.. code-block:: python

    >>> def func():
    ...     try:
    ...         1 / 0
    ...     except ZeroDivisionError:
    ...         raise ArithmeticError from None
    ...
    >>> func()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 5, in func
    ArithmeticError

    # debug

    >>> try:
    ...     func()
    ... except ArithmeticError as e:
    ...     print(e.__context__)
    ...
    division by zero


Generator delegation
----------------------

**New in Python 3.3**

- PEP 380_ - Syntax for Delegating to a Subgenerator

The ``yield from`` expression allows a generator to delegate part of its operations
to another generator. This simplifies writing generators that consume other generators.

.. code-block:: python

    >>> def fib(n: int):
    ...     a, b = 0, 1
    ...     for _ in range(n):
    ...         yield a
    ...         b, a = a + b, b
    ...
    >>> def delegate(n: int):
    ...     yield from fib(n)
    ...
    >>> list(delegate(10))
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


BDFL retirement
---------------

**New in Python 3.1**

- PEP 401_ - BDFL Retirement

An April Fools' joke PEP that added a humorous easter egg. When you import
``barry_as_FLUFL`` from ``__future__``, the ``!=`` operator is replaced with ``<>``.

.. code-block:: python

    >>> from __future__ import barry_as_FLUFL
    >>> 1 != 2
      File "<stdin>", line 1
        1 != 2
           ^
    SyntaxError: with Barry as BDFL, use '<>' instead of '!='
    >>> 1 <> 2
    True


Function annotations
--------------------

**New in Python 3.0**

- PEP 3107_ - Function Annotations
- PEP 484_ - Type Hints
- PEP 483_ - The Theory of Type Hints

Function annotations allow attaching metadata to function parameters and return
values. While Python doesn't enforce these at runtime, they enable static type
checking tools and better IDE support.

.. code-block:: python

    >>> import types
    >>> generator = types.GeneratorType
    >>> def fib(n: int) -> generator:
    ...     a, b = 0, 1
    ...     for _ in range(n):
    ...         yield a
    ...         b, a = a + b, b
    ...
    >>> [f for f in fib(10)]
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


Extended iterable unpacking
----------------------------

**New in Python 3.0**

- PEP 3132_ - Extended Iterable Unpacking

The ``*`` operator in unpacking captures remaining items into a list. This works
in assignments and for loops, making it easy to split sequences.

.. code-block:: python

    >>> a, *b, c = range(5)
    >>> a, b, c
    (0, [1, 2, 3], 4)
    >>> for a, *b in [(1, 2, 3), (4, 5, 6, 7)]:
    ...     print(a, b)
    ...
    1 [2, 3]
    4 [5, 6, 7]


Keyword-Only Arguments
-----------------------

**New in Python 3.0**

- PEP 3102_ - Keyword-Only Arguments

Parameters defined after ``*`` in a function signature must be passed as keyword
arguments. This improves API clarity and prevents accidental positional usage.

.. code-block:: python

    >>> def f(a, b, *, kw):
    ...     print(a, b, kw)
    ...
    >>> f(1, 2, 3)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: f() takes 2 positional arguments but 3 were given
    >>> f(1, 2)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: f() missing 1 required keyword-only argument: 'kw'
    >>> f(1, 2, kw=3)
    1 2 3


New Super
----------

**New in Python 3.0**

- PEP 3135_ - New Super

Python 3 simplified the ``super()`` call by making it work without arguments in
most cases. The interpreter automatically determines the class and instance.

Python 2

.. code-block:: python

    >>> class ParentCls(object):
    ...     def foo(self):
    ...         print "call parent"
    ...
    >>> class ChildCls(ParentCls):
    ...     def foo(self):
    ...         super(ChildCls, self).foo()
    ...         print "call child"
    ...
    >>> p = ParentCls()
    >>> c = ChildCls()
    >>> p.foo()
    call parent
    >>> c.foo()
    call parent
    call child

Python 3

.. code-block:: python

    >>> class ParentCls(object):
    ...     def foo(self):
    ...         print("call parent")
    ...
    >>> class ChildCls(ParentCls):
    ...     def foo(self):
    ...         super().foo()
    ...         print("call child")
    ...
    >>> p = ParentCls()
    >>> c = ChildCls()
    >>> p.foo()
    call parent
    >>> c.foo()
    call parent
    call child


Add ``nonlocal`` keyword
-------------------------

**New in Python 3.0**

- PEP 3104_ - Access to Names in Outer Scopes

The ``nonlocal`` keyword allows assigning to variables in an enclosing (but non-global)
scope. This is useful for closures that need to modify outer variables.

.. code-block:: python

    >>> def outf():
    ...     o = "out"
    ...     def inf():
    ...         nonlocal o
    ...         o = "change out"
    ...     inf()
    ...     print(o)
    ...
    >>> outf()
    change out


Not allow ``from module import *`` inside function
---------------------------------------------------

**New in Python 3.0**

Star imports are now only allowed at module level. This prevents namespace pollution
and makes code more predictable.

.. code-block:: python

    >>> def f():
    ...     from os import *
    ...
      File "<stdin>", line 1
    SyntaxError: import * only allowed at module level


Remove ``<>``
--------------

**New in Python 3.0**

The ``<>`` operator (alternative to ``!=``) was removed in Python 3 to simplify
the language. Use ``!=`` for inequality comparisons.

Python 2

.. code-block:: python

    >>> a = "Python2"
    >>> a <> "Python3"
    True

    # equal to !=
    >>> a != "Python3"
    True

Python 3

.. code-block:: python

    >>> a = "Python3"
    >>> a != "Python2"
    True


``print`` is a function
-------------------------

**New in Python 3.0**

- PEP 3105_ - Make print a function

In Python 3, ``print`` became a function instead of a statement. This allows
more flexibility with keyword arguments like ``end``, ``sep``, and ``file``.

Python 2

.. code-block:: python

    >>> print "print is a statement"
    print is a statement
    >>> for x in range(3):
    ...     print x,
    ...
    0 1 2

Python 3

.. code-block:: python

    >>> print("print is a function")
    print is a function
    >>> print()
    >>> for x in range(3):
    ...     print(x, end=' ')
    ... else:
    ...     print()
    ...
    0 1 2


String is unicode
-------------------

**New in Python 3.0**

- PEP 3138_ - String representation in Python 3000
- PEP 3120_ - Using UTF-8 as the default source encoding
- PEP 3131_ - Supporting Non-ASCII Identifiers

In Python 3, all strings are Unicode by default. The ``str`` type represents
Unicode text, while ``bytes`` represents binary data. This eliminates many
encoding-related bugs common in Python 2.

Python 2

.. code-block:: python

    >>> s = 'Café'  # byte string
    >>> s
    'Caf\xc3\xa9'
    >>> type(s)
    <type 'str'>
    >>> u = u'Café' # unicode string
    >>> u
    u'Caf\xe9'
    >>> type(u)
    <type 'unicode'>
    >>> len([_c for _c in 'Café'])
    5

Python 3

.. code-block:: python

    >>> s = 'Café'
    >>> s
    'Café'
    >>> type(s)
    <class 'str'>
    >>> s.encode('utf-8')
    b'Caf\xc3\xa9'
    >>> s.encode('utf-8').decode('utf-8')
    'Café'
    >>> len([_c for _c in 'Café'])
    4


Division Operator
------------------

**New in Python 3.0**

- PEP 238_ - Changing the Division Operator

In Python 3, the ``/`` operator always performs true division (returning a float),
while ``//`` performs floor division. This eliminates a common source of bugs.

Python 2

.. code-block:: python

    >>> 1 / 2
    0
    >>> 1 // 2
    0
    >>> 1. / 2
    0.5

    # back port "true division" to python2

    >>> from __future__ import division
    >>> 1 / 2
    0.5
    >>> 1 // 2
    0

Python 3

.. code-block:: python

    >>> 1 / 2
    0.5
    >>> 1 // 2
    0


.. _695: https://www.python.org/dev/peps/pep-0695/
.. _701: https://www.python.org/dev/peps/pep-0701/
.. _654: https://www.python.org/dev/peps/pep-0654/
.. _634: https://www.python.org/dev/peps/pep-0634/
.. _635: https://www.python.org/dev/peps/pep-0635/
.. _584: https://www.python.org/dev/peps/pep-0584/
.. _570: https://www.python.org/dev/peps/pep-0570/
.. _572: https://www.python.org/dev/peps/pep-0572/
.. _557: https://www.python.org/dev/peps/pep-0557/
.. _553: https://www.python.org/dev/peps/pep-0553/
.. _560: https://www.python.org/dev/peps/pep-0560/
.. _526: https://www.python.org/dev/peps/pep-0526/
.. _498: https://www.python.org/dev/peps/pep-0498/
.. _525: https://www.python.org/dev/peps/pep-0525/
.. _530: https://www.python.org/dev/peps/pep-0530/
.. _468: https://www.python.org/dev/peps/pep-0468/
.. _520: https://www.python.org/dev/peps/pep-0520/
.. _27350: https://bugs.python.org/issue27350
.. _492: https://www.python.org/dev/peps/pep-0492/
.. _448: https://www.python.org/dev/peps/pep-0448/
.. _465: https://www.python.org/dev/peps/pep-0465/
.. _461: https://www.python.org/dev/peps/pep-0461/
.. _409: https://www.python.org/dev/peps/pep-0409/
.. _380: https://www.python.org/dev/peps/pep-0380/
.. _401: https://www.python.org/dev/peps/pep-0401/
.. _3107: https://www.python.org/dev/peps/pep-3107/
.. _484: https://www.python.org/dev/peps/pep-0484/
.. _483: https://www.python.org/dev/peps/pep-0483/
.. _3132: https://www.python.org/dev/peps/pep-3132/
.. _3102: https://www.python.org/dev/peps/pep-3102/
.. _3135: https://www.python.org/dev/peps/pep-3135/
.. _3104: https://www.python.org/dev/peps/pep-3104/
.. _3105: https://www.python.org/dev/peps/pep-3105/
.. _3138: https://www.python.org/dev/peps/pep-3138/
.. _3120: https://www.python.org/dev/peps/pep-3120/
.. _3131: https://www.python.org/dev/peps/pep-3131/
.. _238: https://www.python.org/dev/peps/pep-0238/
