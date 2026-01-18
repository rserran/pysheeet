.. meta::
    :description lang=en: Python function cheat sheet covering function definitions, arguments, decorators, lambda, closures, and functools
    :keywords: Python, Python Function, decorator, lambda, closure, *args, **kwargs, functools, lru_cache, partial

========
Function
========

.. contents:: Table of Contents
    :backlinks: none

A function can help programmers to wrap their logic into a task for avoiding
duplicate code. In Python, the definition of a function is so versatile that
we can use many features such as decorator, annotation, docstrings, default
arguments and so on to define a function. In this cheat sheet, it collects
many ways to define a function and demystifies some enigmatic syntax in functions.

Document Functions
------------------

Documentation provides programmers hints about how a function is supposed to
be used. A docstring gives an expedient way to write a readable document of
functions. The docstring should be placed as the first statement in the function
body, enclosed in triple quotes. It can be accessed via the ``__doc__`` attribute
or the built-in ``help()`` function. PEP `257 <https://www.python.org/dev/peps/pep-0257>`_
defines conventions for docstrings, and tools like ``pydocstyle`` can help
enforce these conventions in your codebase.

.. code-block:: python

    >>> def example():
    ...     """This is an example function."""
    ...     print("Example function")
    ...
    >>> example.__doc__
    'This is an example function.'
    >>> help(example)

Default Arguments
-----------------

Defining a function where the arguments are optional and have a default value
is quite simple in Python. We can just assign values in the definition and make
sure the default arguments appear in the end. When calling the function, you can
omit arguments that have defaults, pass them positionally, or use keyword syntax
to specify them explicitly. This flexibility makes functions more versatile and
easier to use in different contexts.

.. code-block:: python

    >>> def add(a, b=0):
    ...     return a + b
    ...
    >>> add(1)
    1
    >>> add(1, 2)
    3
    >>> add(1, b=2)
    3

.. warning::

    Avoid using mutable objects (like lists or dictionaries) as default arguments.
    Default argument values are evaluated only once when the function is defined,
    not each time the function is called. This means mutable defaults are shared
    across all calls, which can lead to unexpected behavior where modifications
    persist between function calls.

    .. code-block:: python

        >>> def bad(items=[]):  # DON'T do this
        ...     items.append(1)
        ...     return items
        ...
        >>> bad()
        [1]
        >>> bad()  # unexpected!
        [1, 1]

        >>> def good(items=None):  # DO this instead
        ...     if items is None:
        ...         items = []
        ...     items.append(1)
        ...     return items

Variable Arguments ``*args`` and ``**kwargs``
---------------------------------------------

Python provides a flexible way to handle functions that need to accept a variable
number of arguments. Use ``*args`` to collect any number of positional arguments
into a tuple, and ``**kwargs`` to collect any number of keyword arguments into a
dictionary. These are commonly used when writing wrapper functions, decorators,
or functions that need to pass arguments through to other functions. The names
``args`` and ``kwargs`` are conventions; you can use any valid identifier after
the ``*`` or ``**``.

.. code-block:: python

    >>> def example(a, b=None, *args, **kwargs):
    ...     print(a, b)
    ...     print(args)
    ...     print(kwargs)
    ...
    >>> example(1, "var", 2, 3, word="hello")
    1 var
    (2, 3)
    {'word': 'hello'}

Unpack Arguments
----------------

When calling a function, you can use ``*`` to unpack a sequence (like a list or
tuple) into separate positional arguments, and ``**`` to unpack a dictionary into
keyword arguments. This is the inverse of ``*args`` and ``**kwargs`` in function
definitions. Unpacking is particularly useful when you have data in a collection
that you want to pass to a function that expects separate arguments.

.. code-block:: python

    >>> def foo(a, b, c='BAZ'):
    ...     print(a, b, c)
    ...
    >>> foo(*("FOO", "BAR"), **{"c": "baz"})
    FOO BAR baz

    >>> args = [1, 2, 3]
    >>> print(*args)
    1 2 3

Keyword-Only Arguments
----------------------

Arguments that appear after ``*`` or ``*args`` in a function definition are
keyword-only, meaning they must be passed by name and cannot be passed positionally.
This feature, introduced in Python 3.0, helps prevent errors when functions have
many parameters, as it forces callers to be explicit about which argument they're
providing. Keyword-only arguments can have default values, making them optional.

**New in Python 3.0**

.. code-block:: python

    >>> def f(a, b, *, kw):
    ...     print(a, b, kw)
    ...
    >>> f(1, 2, kw=3)
    1 2 3
    >>> f(1, 2, 3)
    Traceback (most recent call last):
    TypeError: f() takes 2 positional arguments but 3 were given

    >>> # keyword-only with default
    >>> def g(a, *, kw=10):
    ...     return a + kw
    ...
    >>> g(5)
    15

Positional-Only Arguments
-------------------------

Arguments that appear before ``/`` in a function definition are positional-only,
meaning they cannot be passed by keyword name. This feature, introduced in Python
3.8, is useful when parameter names are not meaningful to callers or when you want
to reserve the flexibility to change parameter names without breaking existing code.
Many built-in functions like ``len()`` and ``pow()`` use positional-only parameters.
You can combine positional-only (``/``) and keyword-only (``*``) in the same function.

**New in Python 3.8**

.. code-block:: python

    >>> def f(a, b, /, c):
    ...     print(a, b, c)
    ...
    >>> f(1, 2, 3)
    1 2 3
    >>> f(1, 2, c=3)
    1 2 3
    >>> f(a=1, b=2, c=3)
    Traceback (most recent call last):
    TypeError: f() got some positional-only arguments passed as keyword arguments

    >>> # combining positional-only and keyword-only
    >>> def g(a, /, b, *, c):
    ...     return a + b + c
    ...
    >>> g(1, 2, c=3)
    6

Annotations
-----------

Function annotations provide a way to attach metadata to function parameters and
return values. While Python doesn't enforce these annotations at runtime, they
serve as documentation and are used by static type checkers like ``mypy`` to catch
type errors before code runs. Annotations are stored in the function's ``__annotations__``
attribute as a dictionary. The ``typing`` module (Python 3.5+) provides additional
types like ``List``, ``Dict``, ``Optional``, and ``Union`` for more expressive type hints.

**New in Python 3.0**

.. code-block:: python

    >>> def fib(n: int) -> int:
    ...     a, b = 0, 1
    ...     for _ in range(n):
    ...         b, a = a + b, b
    ...     return a
    ...
    >>> fib(10)
    55
    >>> fib.__annotations__
    {'n': <class 'int'>, 'return': <class 'int'>}

Lambda
------

Lambda expressions create small anonymous functions inline. They are syntactically
restricted to a single expression, which is implicitly returned. Lambdas are useful
for short, throwaway functions, especially as arguments to higher-order functions
like ``sorted()``, ``map()``, ``filter()``, and ``reduce()``. While lambdas can make
code more concise, complex logic should be written as regular named functions for
better readability and debugging.

.. code-block:: python

    >>> square = lambda x: x ** 2
    >>> square(5)
    25

    >>> # lambda with multiple arguments
    >>> add = lambda a, b: a + b
    >>> add(2, 3)
    5

    >>> # lambda with conditional
    >>> max_val = lambda a, b: a if a > b else b
    >>> max_val(3, 5)
    5

    >>> # common use: sorting key
    >>> pairs = [(1, 'b'), (2, 'a'), (3, 'c')]
    >>> sorted(pairs, key=lambda x: x[1])
    [(2, 'a'), (1, 'b'), (3, 'c')]

Callable
--------

In Python, any object that implements the ``__call__`` method is callable, meaning
it can be invoked like a function using parentheses. This includes functions, methods,
lambdas, classes (calling a class creates an instance), and instances of classes that
define ``__call__``. The built-in ``callable()`` function returns ``True`` if an object
appears callable, which is useful for checking before attempting to call an object
to avoid ``TypeError`` exceptions.

.. code-block:: python

    >>> callable(print)
    True
    >>> callable(42)
    False

    >>> class Adder:
    ...     def __init__(self, n):
    ...         self.n = n
    ...     def __call__(self, x):
    ...         return self.n + x
    ...
    >>> add_five = Adder(5)
    >>> callable(add_five)
    True
    >>> add_five(10)
    15

Get Function Name
-----------------

Functions in Python are first-class objects with various attributes that provide
metadata about them. The ``__name__`` attribute contains the function's name as
defined, ``__doc__`` contains the docstring, ``__module__`` indicates which module
the function was defined in, and ``__annotations__`` holds type hints. These
attributes are useful for debugging, logging, and introspection.

.. code-block:: python

    >>> def example_function():
    ...     """Example docstring."""
    ...     pass
    ...
    >>> example_function.__name__
    'example_function'
    >>> example_function.__doc__
    'Example docstring.'
    >>> example_function.__module__
    '__main__'

Closure
-------

A closure is a function that captures and remembers values from its enclosing
lexical scope even after that scope has finished executing. This happens when
a nested function references variables from its outer function. Closures are
powerful for creating function factories (functions that return customized
functions), implementing decorators, and maintaining state without using global
variables or classes. Use the ``nonlocal`` keyword to modify captured variables
from the enclosing scope.

.. code-block:: python

    >>> def make_multiplier(n):
    ...     def multiplier(x):
    ...         return x * n
    ...     return multiplier
    ...
    >>> double = make_multiplier(2)
    >>> triple = make_multiplier(3)
    >>> double(5)
    10
    >>> triple(5)
    15

    >>> # closure with mutable state
    >>> def make_counter():
    ...     count = 0
    ...     def counter():
    ...         nonlocal count
    ...         count += 1
    ...         return count
    ...     return counter
    ...
    >>> counter = make_counter()
    >>> counter()
    1
    >>> counter()
    2

Generator
---------

Generator functions use the ``yield`` statement to produce a sequence of values
lazily, one at a time, instead of computing all values upfront and storing them
in memory. When called, a generator function returns a generator iterator that
can be iterated over with ``for`` loops or ``next()``. Generators are memory-efficient
for large sequences and can represent infinite sequences. Generator expressions
provide a concise syntax similar to list comprehensions but with lazy evaluation.

.. code-block:: python

    >>> def fib(n):
    ...     a, b = 0, 1
    ...     for _ in range(n):
    ...         yield a
    ...         b, a = a + b, b
    ...
    >>> list(fib(10))
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    >>> # generator expression
    >>> squares = (x**2 for x in range(5))
    >>> list(squares)
    [0, 1, 4, 9, 16]

Decorator
---------

Decorators are a powerful pattern for modifying or extending the behavior of
functions without changing their source code. A decorator is a function that
takes a function as input and returns a new function (usually a wrapper) that
adds some functionality before or after calling the original. The ``@decorator``
syntax is syntactic sugar for ``func = decorator(func)``. Always use ``@wraps``
from ``functools`` in your wrapper function to preserve the original function's
metadata like ``__name__``, ``__doc__``, and ``__annotations__``.

**New in Python 2.4** - PEP `318 <https://www.python.org/dev/peps/pep-0318/>`_

.. code-block:: python

    >>> from functools import wraps
    >>> def log_calls(func):
    ...     @wraps(func)
    ...     def wrapper(*args, **kwargs):
    ...         print(f"Calling {func.__name__}")
    ...         return func(*args, **kwargs)
    ...     return wrapper
    ...
    >>> @log_calls
    ... def greet(name):
    ...     return f"Hello, {name}!"
    ...
    >>> greet("Alice")
    Calling greet
    'Hello, Alice!'

    >>> # equivalent to:
    >>> # greet = log_calls(greet)

.. note::

    Always use ``@wraps(func)`` in decorators to preserve the original function's
    ``__name__``, ``__doc__``, and other attributes. Without it, the decorated
    function will have the wrapper's attributes, which makes debugging harder.

Decorator with Arguments
------------------------

To create a decorator that accepts arguments, you need an extra layer of nesting.
The outermost function takes the decorator's arguments and returns the actual
decorator. The middle function takes the function being decorated and returns
the wrapper. The innermost function is the wrapper that executes when the decorated
function is called. This pattern is commonly used for decorators like ``@repeat(3)``
or ``@route('/path')``.

.. code-block:: python

    >>> from functools import wraps
    >>> def repeat(times):
    ...     def decorator(func):
    ...         @wraps(func)
    ...         def wrapper(*args, **kwargs):
    ...             for _ in range(times):
    ...                 result = func(*args, **kwargs)
    ...             return result
    ...         return wrapper
    ...     return decorator
    ...
    >>> @repeat(3)
    ... def say_hello():
    ...     print("Hello!")
    ...
    >>> say_hello()
    Hello!
    Hello!
    Hello!

    >>> # equivalent to:
    >>> # say_hello = repeat(3)(say_hello)

Class Decorator
---------------

Decorators can also be implemented as classes instead of functions. A class-based
decorator implements ``__init__`` to receive the decorated function and ``__call__``
to act as the wrapper. This approach is useful when the decorator needs to maintain
state across multiple calls to the decorated function, such as counting calls,
caching results, or tracking timing information.

.. code-block:: python

    >>> class CountCalls:
    ...     def __init__(self, func):
    ...         self.func = func
    ...         self.count = 0
    ...     def __call__(self, *args, **kwargs):
    ...         self.count += 1
    ...         return self.func(*args, **kwargs)
    ...
    >>> @CountCalls
    ... def example():
    ...     return "result"
    ...
    >>> example()
    'result'
    >>> example()
    'result'
    >>> example.count
    2

Cache with ``lru_cache``
------------------------

The ``lru_cache`` decorator from ``functools`` automatically caches function results
based on the arguments passed. When the function is called with the same arguments
again, the cached result is returned instead of recomputing it. This is especially
useful for expensive computations or recursive functions like Fibonacci. The ``maxsize``
parameter limits cache size (use ``None`` for unlimited). Use ``cache_info()`` to
see hit/miss statistics and ``cache_clear()`` to reset the cache.

**New in Python 3.2**

.. code-block:: python

    >>> from functools import lru_cache
    >>> @lru_cache(maxsize=None)
    ... def fib(n):
    ...     if n < 2:
    ...         return n
    ...     return fib(n - 1) + fib(n - 2)
    ...
    >>> fib(100)
    354224848179261915075
    >>> fib.cache_info()
    CacheInfo(hits=98, misses=101, maxsize=None, currsize=101)
    >>> fib.cache_clear()  # clear the cache

**New in Python 3.9** - ``@cache`` is a simpler alias for ``@lru_cache(maxsize=None)``

.. code-block:: python

    >>> from functools import cache
    >>> @cache
    ... def factorial(n):
    ...     return n * factorial(n-1) if n else 1

Partial Functions
-----------------

The ``functools.partial`` function creates a new callable with some arguments of
the original function pre-filled. This is useful for adapting functions to interfaces
that expect fewer arguments, creating specialized versions of general functions,
or preparing callback functions. The resulting partial object can be called with
the remaining arguments. You can pre-fill both positional and keyword arguments.

.. code-block:: python

    >>> from functools import partial
    >>> def power(base, exponent):
    ...     return base ** exponent
    ...
    >>> square = partial(power, exponent=2)
    >>> cube = partial(power, exponent=3)
    >>> square(5)
    25
    >>> cube(5)
    125

    >>> # useful for callbacks
    >>> from functools import partial
    >>> def greet(greeting, name):
    ...     return f"{greeting}, {name}!"
    ...
    >>> say_hello = partial(greet, "Hello")
    >>> say_hello("Alice")
    'Hello, Alice!'

``singledispatch`` - Function Overloading
-----------------------------------------

The ``singledispatch`` decorator from ``functools`` enables function overloading
based on the type of the first argument. You define a base function and then
register specialized implementations for different types using the ``@func.register``
decorator. When the function is called, Python automatically dispatches to the
appropriate implementation based on the argument's type. This is useful for writing
generic functions that behave differently for different types.

**New in Python 3.4**

.. code-block:: python

    >>> from functools import singledispatch
    >>> @singledispatch
    ... def process(arg):
    ...     return f"Default: {arg}"
    ...
    >>> @process.register(int)
    ... def _(arg):
    ...     return f"Integer: {arg * 2}"
    ...
    >>> @process.register(list)
    ... def _(arg):
    ...     return f"List with {len(arg)} items"
    ...
    >>> process("hello")
    'Default: hello'
    >>> process(5)
    'Integer: 10'
    >>> process([1, 2, 3])
    'List with 3 items'

``reduce`` - Cumulative Operations
----------------------------------

The ``reduce`` function from ``functools`` applies a two-argument function
cumulatively to the items of a sequence, from left to right, reducing the sequence
to a single value. For example, ``reduce(f, [a, b, c, d])`` computes ``f(f(f(a, b), c), d)``.
An optional third argument provides an initial value. While ``reduce`` can be powerful,
list comprehensions or explicit loops are often more readable for simple cases.

.. code-block:: python

    >>> from functools import reduce
    >>> # sum of list
    >>> reduce(lambda x, y: x + y, [1, 2, 3, 4, 5])
    15

    >>> # product of list
    >>> reduce(lambda x, y: x * y, [1, 2, 3, 4, 5])
    120

    >>> # with initial value
    >>> reduce(lambda x, y: x + y, [1, 2, 3], 10)
    16

Higher-Order Functions
----------------------

Higher-order functions are functions that take other functions as arguments or
return functions as results. Python provides several built-in higher-order functions
that are commonly used for functional programming patterns. ``map()`` applies a
function to every item in an iterable, ``filter()`` keeps items where the function
returns ``True``, and ``sorted()``/``min()``/``max()`` accept a ``key`` function
to customize comparison. These functions return iterators (except ``sorted``),
so wrap them in ``list()`` if you need a list.

.. code-block:: python

    >>> # map - apply function to each item
    >>> list(map(lambda x: x**2, [1, 2, 3, 4]))
    [1, 4, 9, 16]

    >>> # filter - keep items where function returns True
    >>> list(filter(lambda x: x > 2, [1, 2, 3, 4]))
    [3, 4]

    >>> # sorted with key function
    >>> sorted(['banana', 'apple', 'cherry'], key=len)
    ['apple', 'banana', 'cherry']

    >>> # min/max with key function
    >>> max(['apple', 'banana', 'cherry'], key=len)
    'banana'
