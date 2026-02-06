.. meta::
    :description lang=en: Python class cheat sheet covering magic methods, property decorators, inheritance, context managers, and OOP design patterns with code examples
    :keywords: Python, Python3, Python class, Python OOP cheat sheet, magic methods, property decorator, context manager, singleton, abstract class, descriptor, inheritance

=====
Class
=====

.. contents:: Table of Contents
    :backlinks: none

Python is an object-oriented programming language. This cheat sheet covers
class definitions, inheritance, magic methods, property decorators, context
managers, and common design patterns. Understanding these concepts is essential
for writing clean, maintainable Python code.

List Attributes with dir()
--------------------------

The ``dir()`` function returns a list of all attributes and methods of an object.
This is useful for introspection and discovering what operations are available.

.. code-block:: python

    >>> dir(list)  # check all attr of list
    ['__add__', '__class__', ...]

Check Type with isinstance()
----------------------------

Use ``isinstance()`` to check if an object is an instance of a class or its
subclasses. This is preferred over ``type()`` comparison because it supports
inheritance.

.. code-block:: python

    >>> ex = 10
    >>> isinstance(ex, int)
    True
    >>> isinstance(ex, (int, float))  # check multiple types
    True

Check Inheritance with issubclass()
-----------------------------------

Use ``issubclass()`` to check if a class is a subclass of another class.

.. code-block:: python

    >>> class Animal: pass
    >>> class Dog(Animal): pass
    >>> issubclass(Dog, Animal)
    True
    >>> issubclass(Dog, object)
    True

Get Class Name
--------------

Access the class name through the ``__class__.__name__`` attribute.

.. code-block:: python

    >>> class ExampleClass:
    ...     pass
    ...
    >>> ex = ExampleClass()
    >>> ex.__class__.__name__
    'ExampleClass'

Has / Get / Set Attributes
--------------------------

Python provides built-in functions to dynamically access and modify object
attributes at runtime.

.. code-block:: python

    >>> class Example:
    ...     def __init__(self):
    ...         self.name = "ex"
    ...
    >>> ex = Example()
    >>> hasattr(ex, "name")
    True
    >>> getattr(ex, 'name')
    'ex'
    >>> setattr(ex, 'name', 'example')
    >>> ex.name
    'example'
    >>> getattr(ex, 'missing', 'default')  # with default
    'default'

Declare Class with type()
-------------------------

Classes can be created dynamically using ``type()``. This is useful for
metaprogramming and creating classes at runtime.

.. code-block:: python

    >>> def greet(self):
    ...     return f"Hello, I'm {self.name}"
    ...
    >>> Person = type('Person', (object,), {
    ...     'name': 'Anonymous',
    ...     'greet': greet
    ... })
    >>> p = Person()
    >>> p.greet()
    "Hello, I'm Anonymous"

This is equivalent to:

.. code-block:: python

    >>> class Person:
    ...     name = 'Anonymous'
    ...     def greet(self):
    ...         return f"Hello, I'm {self.name}"

__new__ vs __init__
-------------------

``__new__`` creates the instance, ``__init__`` initializes it. ``__init__`` is
only called if ``__new__`` returns an instance of the class.

.. code-block:: python

    >>> class Example:
    ...     def __new__(cls, arg):
    ...         print(f'__new__ {arg}')
    ...         return super().__new__(cls)
    ...     def __init__(self, arg):
    ...         print(f'__init__ {arg}')
    ...
    >>> o = Example("Hello")
    __new__ Hello
    __init__ Hello

__str__ and __repr__
--------------------

``__str__`` returns a human-readable string, ``__repr__`` returns an unambiguous
representation for debugging. When ``__str__`` is not defined, ``__repr__`` is used.

.. code-block:: python

    >>> class Vector:
    ...     def __init__(self, x, y):
    ...         self.x, self.y = x, y
    ...     def __repr__(self):
    ...         return f"Vector({self.x}, {self.y})"
    ...     def __str__(self):
    ...         return f"({self.x}, {self.y})"
    ...
    >>> v = Vector(1, 2)
    >>> repr(v)
    'Vector(1, 2)'
    >>> str(v)
    '(1, 2)'
    >>> print(v)
    (1, 2)

Comparison Magic Methods
------------------------

Implement comparison operators by defining magic methods. Use
``functools.total_ordering`` to generate all comparisons from ``__eq__`` and one other.

.. code-block:: python

    >>> from functools import total_ordering
    >>> @total_ordering
    ... class Number:
    ...     def __init__(self, val):
    ...         self.val = val
    ...     def __eq__(self, other):
    ...         return self.val == other.val
    ...     def __lt__(self, other):
    ...         return self.val < other.val
    ...
    >>> Number(1) < Number(2)
    True
    >>> Number(2) >= Number(1)
    True

Arithmetic Magic Methods
------------------------

Implement arithmetic operators to make objects work with ``+``, ``-``, ``*``, etc.

.. code-block:: python

    >>> class Vector:
    ...     def __init__(self, x, y):
    ...         self.x, self.y = x, y
    ...     def __add__(self, other):
    ...         return Vector(self.x + other.x, self.y + other.y)
    ...     def __mul__(self, scalar):
    ...         return Vector(self.x * scalar, self.y * scalar)
    ...     def __repr__(self):
    ...         return f"Vector({self.x}, {self.y})"
    ...
    >>> Vector(1, 2) + Vector(3, 4)
    Vector(4, 6)
    >>> Vector(1, 2) * 3
    Vector(3, 6)

Callable with __call__
----------------------

Implement ``__call__`` to make instances callable like functions. This is useful
for creating function-like objects that maintain state.

.. code-block:: python

    >>> class Multiplier:
    ...     def __init__(self, factor):
    ...         self.factor = factor
    ...     def __call__(self, x):
    ...         return x * self.factor
    ...
    >>> double = Multiplier(2)
    >>> double(5)
    10
    >>> callable(double)
    True

@property Decorator
-------------------

Use ``@property`` to define getters, setters, and deleters for managed attributes.
This allows attribute access syntax while running custom code.

.. code-block:: python

    >>> class Circle:
    ...     def __init__(self, radius):
    ...         self._radius = radius
    ...     @property
    ...     def radius(self):
    ...         return self._radius
    ...     @radius.setter
    ...     def radius(self, value):
    ...         if value < 0:
    ...             raise ValueError("Radius must be positive")
    ...         self._radius = value
    ...     @property
    ...     def area(self):
    ...         return 3.14159 * self._radius ** 2
    ...
    >>> c = Circle(5)
    >>> c.area
    78.53975
    >>> c.radius = 10
    >>> c.radius
    10

Descriptor Protocol
-------------------

Descriptors control attribute access at the class level. They implement
``__get__``, ``__set__``, and/or ``__delete__`` methods.

.. code-block:: python

    >>> class Positive:
    ...     def __init__(self, name):
    ...         self.name = name
    ...     def __get__(self, obj, objtype=None):
    ...         return obj.__dict__[self.name]
    ...     def __set__(self, obj, value):
    ...         if value < 0:
    ...             raise ValueError("Must be positive")
    ...         obj.__dict__[self.name] = value
    ...
    >>> class Example:
    ...     x = Positive('x')
    ...     def __init__(self, x):
    ...         self.x = x
    ...
    >>> ex = Example(10)
    >>> ex.x
    10

Context Manager Protocol
------------------------

Context managers implement ``__enter__`` and ``__exit__`` to manage resources
with the ``with`` statement. This ensures proper cleanup even if exceptions occur.

.. code-block:: python

    class ManagedFile:
        def __init__(self, filename):
            self.filename = filename

        def __enter__(self):
            self.file = open(self.filename, 'r')
            return self.file

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.file.close()
            return False  # don't suppress exceptions

    with ManagedFile('example.txt') as f:
        content = f.read()

Using contextlib
----------------

The ``contextlib`` module provides utilities for creating context managers
without writing a full class.

.. code-block:: python

    from contextlib import contextmanager

    @contextmanager
    def managed_file(filename):
        f = open(filename, 'r')
        try:
            yield f
        finally:
            f.close()

    with managed_file('example.txt') as f:
        content = f.read()

@staticmethod and @classmethod
------------------------------

``@staticmethod`` defines a method that doesn't access instance or class.
``@classmethod`` receives the class as the first argument, useful for
alternative constructors.

.. code-block:: python

    >>> class Date:
    ...     def __init__(self, year, month, day):
    ...         self.year, self.month, self.day = year, month, day
    ...     @classmethod
    ...     def from_string(cls, date_string):
    ...         year, month, day = map(int, date_string.split('-'))
    ...         return cls(year, month, day)
    ...     @staticmethod
    ...     def is_valid(date_string):
    ...         try:
    ...             y, m, d = map(int, date_string.split('-'))
    ...             return 1 <= m <= 12 and 1 <= d <= 31
    ...         except:
    ...             return False
    ...
    >>> d = Date.from_string('2024-01-15')
    >>> d.year
    2024
    >>> Date.is_valid('2024-13-01')
    False

Abstract Base Classes with abc
------------------------------

Use ``abc`` module to define abstract base classes that cannot be instantiated
and require subclasses to implement certain methods.

.. code-block:: python

    >>> from abc import ABC, abstractmethod
    >>> class Shape(ABC):
    ...     @abstractmethod
    ...     def area(self):
    ...         pass
    ...
    >>> class Rectangle(Shape):
    ...     def __init__(self, width, height):
    ...         self.width, self.height = width, height
    ...     def area(self):
    ...         return self.width * self.height
    ...
    >>> r = Rectangle(3, 4)
    >>> r.area()
    12
    >>> Shape()  # raises TypeError

The Diamond Problem (MRO)
-------------------------

Python uses Method Resolution Order (MRO) to resolve the diamond problem in
multiple inheritance. Use ``ClassName.mro()`` to see the resolution order.

.. code-block:: python

    >>> class A:
    ...     def method(self):
    ...         return "A"
    ...
    >>> class B(A):
    ...     def method(self):
    ...         return "B"
    ...
    >>> class C(A):
    ...     def method(self):
    ...         return "C"
    ...
    >>> class D(B, C):
    ...     pass
    ...
    >>> D().method()
    'B'
    >>> D.mro()
    [<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>]

Singleton Pattern
-----------------

Singleton ensures only one instance of a class exists. Implement using
``__new__`` or a decorator.

.. code-block:: python

    class Singleton:
        _instance = None

        def __new__(cls):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    a = Singleton()
    b = Singleton()
    print(a is b)  # True

Using __slots__
---------------

``__slots__`` restricts instance attributes and reduces memory usage by avoiding
``__dict__`` per instance.

.. code-block:: python

    >>> class Point:
    ...     __slots__ = ['x', 'y']
    ...     def __init__(self, x, y):
    ...         self.x, self.y = x, y
    ...
    >>> p = Point(1, 2)
    >>> p.x
    1
    >>> p.z = 3  # raises AttributeError

Common Magic Methods Reference
------------------------------

.. code-block:: python

    # Object Creation and Representation
    __new__(cls, ...)        # create instance
    __init__(self, ...)      # initialize instance
    __del__(self)            # destructor
    __repr__(self)           # repr(obj)
    __str__(self)            # str(obj)

    # Comparison
    __eq__(self, other)      # ==
    __ne__(self, other)      # !=
    __lt__(self, other)      # <
    __le__(self, other)      # <=
    __gt__(self, other)      # >
    __ge__(self, other)      # >=

    # Arithmetic
    __add__(self, other)     # +
    __sub__(self, other)     # -
    __mul__(self, other)     # *
    __truediv__(self, other) # /
    __floordiv__(self, other)# //
    __mod__(self, other)     # %
    __pow__(self, other)     # **

    # Container
    __len__(self)            # len(obj)
    __getitem__(self, key)   # obj[key]
    __setitem__(self, k, v)  # obj[key] = value
    __delitem__(self, key)   # del obj[key]
    __contains__(self, item) # item in obj
    __iter__(self)           # iter(obj)

    # Attribute Access
    __getattr__(self, name)  # obj.name (when not found)
    __setattr__(self, n, v)  # obj.name = value
    __delattr__(self, name)  # del obj.name

    # Callable
    __call__(self, ...)      # obj()

    # Context Manager
    __enter__(self)          # with obj
    __exit__(self, ...)      # exit with block

    # Descriptor
    __get__(self, obj, type) # descriptor access
    __set__(self, obj, val)  # descriptor assignment
    __delete__(self, obj)    # descriptor deletion
