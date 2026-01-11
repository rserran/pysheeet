"""Python OOP Examples

Source code for docs/notes/basic/python-object.rst
"""

import pytest
from abc import ABC, abstractmethod


# Basic Class
class Person:
    """Basic class with __init__."""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Hello, I'm {self.name}"


# Class and Instance Attributes
class Counter:
    """Class with class and instance attributes."""

    count = 0

    def __init__(self):
        Counter.count += 1
        self.id = Counter.count


# Inheritance
class Animal:
    """Base class for inheritance."""

    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError


class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} says Meow!"


# Magic Methods
class Vector:
    """Class with magic methods."""

    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# Callable
class Multiplier:
    """Callable class."""

    def __init__(self, factor: int):
        self.factor = factor

    def __call__(self, x: int) -> int:
        return x * self.factor


# Property
class Circle:
    """Class with property."""

    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float):
        if value < 0:
            raise ValueError("Radius must be positive")
        self._radius = value

    @property
    def area(self) -> float:
        return 3.14159 * self._radius**2


# Context Manager
class ManagedResource:
    """Context manager class."""

    def __init__(self):
        self.entered = False
        self.exited = False

    def __enter__(self):
        self.entered = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exited = True
        return False


# Singleton
class Singleton:
    """Singleton pattern."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# Class Methods and Static Methods
class Date:
    """Class with classmethod and staticmethod."""

    def __init__(self, year: int, month: int, day: int):
        self.year, self.month, self.day = year, month, day

    @classmethod
    def from_string(cls, date_string: str):
        year, month, day = map(int, date_string.split("-"))
        return cls(year, month, day)

    @staticmethod
    def is_valid(date_string: str) -> bool:
        try:
            year, month, day = map(int, date_string.split("-"))
            return 1 <= month <= 12 and 1 <= day <= 31
        except:
            return False


# Abstract Base Class
class Shape(ABC):
    """Abstract base class."""

    @abstractmethod
    def area(self) -> float:
        pass


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width, self.height = width, height

    def area(self) -> float:
        return self.width * self.height


# Tests
class TestBasicClass:
    def test_person(self):
        p = Person("Alice", 30)
        assert p.name == "Alice"
        assert p.greet() == "Hello, I'm Alice"


class TestClassAttributes:
    def test_counter(self):
        Counter.count = 0  # reset
        a, b = Counter(), Counter()
        assert a.id == 1
        assert b.id == 2
        assert Counter.count == 2


class TestInheritance:
    def test_dog(self):
        assert Dog("Buddy").speak() == "Buddy says Woof!"

    def test_cat(self):
        assert Cat("Whiskers").speak() == "Whiskers says Meow!"


class TestMagicMethods:
    def test_vector_add(self):
        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        assert v1 + v2 == Vector(4, 6)

    def test_vector_repr(self):
        assert repr(Vector(1, 2)) == "Vector(1, 2)"


class TestCallable:
    def test_multiplier(self):
        double = Multiplier(2)
        assert double(5) == 10
        assert callable(double)


class TestProperty:
    def test_circle_area(self):
        c = Circle(5)
        assert abs(c.area - 78.53975) < 0.001

    def test_circle_setter(self):
        c = Circle(5)
        c.radius = 10
        assert c.radius == 10

    def test_circle_invalid(self):
        c = Circle(5)
        with pytest.raises(ValueError):
            c.radius = -1


class TestContextManager:
    def test_managed_resource(self):
        with ManagedResource() as r:
            assert r.entered
        assert r.exited


class TestSingleton:
    def test_singleton(self):
        a = Singleton()
        b = Singleton()
        assert a is b


class TestClassMethods:
    def test_from_string(self):
        d = Date.from_string("2024-01-15")
        assert d.year == 2024
        assert d.month == 1

    def test_is_valid(self):
        assert Date.is_valid("2024-01-15")
        assert not Date.is_valid("2024-13-01")


class TestABC:
    def test_rectangle(self):
        r = Rectangle(3, 4)
        assert r.area() == 12

    def test_abstract_instantiation(self):
        with pytest.raises(TypeError):
            Shape()
