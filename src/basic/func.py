"""Python Function Examples

Source code for docs/notes/basic/python-func.rst
"""

import pytest
from functools import wraps, lru_cache


# Default Arguments
def greet(name: str, greeting: str = "Hello") -> str:
    """Greet with optional greeting."""
    return f"{greeting}, {name}!"


# Variable Arguments
def sum_all(*args) -> int:
    """Sum all positional arguments."""
    return sum(args)


def format_info(**kwargs) -> str:
    """Format keyword arguments."""
    return ", ".join(f"{k}={v}" for k, v in kwargs.items())


# Keyword-Only Arguments
def keyword_only(a, b, *, kw):
    """Function with keyword-only argument."""
    return a + b + kw


# Positional-Only Arguments (Python 3.8+)
def positional_only(a, b, /, c):
    """Function with positional-only arguments."""
    return a + b + c


# Lambda
square = lambda x: x**2
add = lambda a, b: a + b


# Generator
def fibonacci(n: int):
    """Generate fibonacci sequence."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def countdown(n: int):
    """Countdown generator."""
    while n > 0:
        yield n
        n -= 1


# Decorator
def log_calls(func):
    """Decorator that logs function calls."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        return func(*args, **kwargs)

    wrapper.call_count = 0
    return wrapper


# Decorator with Arguments
def repeat(times: int):
    """Decorator that repeats function calls."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


# Closure
def make_multiplier(n: int):
    """Create a multiplier function."""

    def multiplier(x: int) -> int:
        return x * n

    return multiplier


# Cache
@lru_cache(maxsize=None)
def fib_cached(n: int) -> int:
    """Fibonacci with caching."""
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


# Callable Class
class Adder:
    """Callable class that adds a fixed value."""

    def __init__(self, n: int):
        self.n = n

    def __call__(self, x: int) -> int:
        return self.n + x


# Tests
class TestDefaultArguments:
    def test_default(self):
        assert greet("Alice") == "Hello, Alice!"

    def test_custom(self):
        assert greet("Bob", "Hi") == "Hi, Bob!"


class TestVariableArguments:
    def test_args(self):
        assert sum_all(1, 2, 3, 4, 5) == 15

    def test_kwargs(self):
        result = format_info(name="Alice", age=30)
        assert "name=Alice" in result
        assert "age=30" in result


class TestKeywordOnly:
    def test_keyword_only(self):
        assert keyword_only(1, 2, kw=3) == 6


class TestPositionalOnly:
    def test_positional_only(self):
        assert positional_only(1, 2, 3) == 6
        assert positional_only(1, 2, c=3) == 6


class TestLambda:
    def test_square(self):
        assert square(5) == 25

    def test_add(self):
        assert add(2, 3) == 5


class TestGenerator:
    def test_fibonacci(self):
        assert list(fibonacci(10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_countdown(self):
        assert list(countdown(5)) == [5, 4, 3, 2, 1]


class TestDecorator:
    def test_log_calls(self):
        @log_calls
        def example():
            return "result"

        example()
        example()
        assert example.call_count == 2

    def test_repeat(self):
        counter = {"count": 0}

        @repeat(3)
        def increment():
            counter["count"] += 1

        increment()
        assert counter["count"] == 3


class TestClosure:
    def test_multiplier(self):
        double = make_multiplier(2)
        triple = make_multiplier(3)
        assert double(5) == 10
        assert triple(5) == 15


class TestCache:
    def test_fib_cached(self):
        assert fib_cached(10) == 55
        assert fib_cached(20) == 6765


class TestCallable:
    def test_adder(self):
        add_five = Adder(5)
        assert add_five(10) == 15
        assert callable(add_five)
