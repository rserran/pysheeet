"""Python Generator Examples

Source code for docs/notes/basic/python-generator.rst
"""

import pytest
from contextlib import contextmanager


# Generator Function
def simple_gen():
    """Simple generator yielding values."""
    yield 1
    yield 2
    yield 3


def fibonacci(n: int):
    """Generate fibonacci sequence."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def infinite_counter(start: int = 0):
    """Infinite counter generator."""
    n = start
    while True:
        yield n
        n += 1


# Generator Expression
def gen_expr_sum(n: int) -> int:
    """Sum using generator expression."""
    return sum(x**2 for x in range(n))


# Send Values
def accumulator():
    """Accumulator that receives values via send."""
    total = 0
    while True:
        value = yield total
        if value is not None:
            total += value


# yield from
def chain(*iterables):
    """Chain multiple iterables."""
    for it in iterables:
        yield from it


def flatten(nested):
    """Flatten nested lists."""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


# Iterable Class
class Range:
    """Custom range class using generator."""

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __iter__(self):
        n = self.start
        while n < self.end:
            yield n
            n += 1

    def __reversed__(self):
        n = self.end - 1
        while n >= self.start:
            yield n
            n -= 1


# Pipeline
def filter_positive(nums):
    """Filter positive numbers."""
    for n in nums:
        if n > 0:
            yield n


def double(nums):
    """Double each number."""
    for n in nums:
        yield n * 2


# Context Manager
@contextmanager
def capture_output():
    """Context manager using generator."""
    output = []
    yield output


# Tests
class TestGeneratorBasics:
    def test_simple_gen(self):
        assert list(simple_gen()) == [1, 2, 3]

    def test_fibonacci(self):
        assert list(fibonacci(10)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_infinite_counter(self):
        from itertools import islice

        assert list(islice(infinite_counter(), 5)) == [0, 1, 2, 3, 4]
        assert list(islice(infinite_counter(10), 3)) == [10, 11, 12]


class TestGeneratorExpression:
    def test_gen_expr_sum(self):
        assert gen_expr_sum(5) == 0 + 1 + 4 + 9 + 16

    def test_unpack(self):
        g = (x for x in range(3))
        assert [*g] == [0, 1, 2]


class TestSend:
    def test_accumulator(self):
        acc = accumulator()
        assert next(acc) == 0
        assert acc.send(10) == 10
        assert acc.send(20) == 30
        assert acc.send(5) == 35


class TestYieldFrom:
    def test_chain(self):
        assert list(chain([1, 2], [3, 4])) == [1, 2, 3, 4]

    def test_flatten(self):
        assert list(flatten([1, [2, [3, 4], 5], 6])) == [1, 2, 3, 4, 5, 6]


class TestIterableClass:
    def test_range(self):
        assert list(Range(1, 5)) == [1, 2, 3, 4]

    def test_reversed_range(self):
        assert list(reversed(Range(1, 5))) == [4, 3, 2, 1]


class TestPipeline:
    def test_pipeline(self):
        nums = [-1, 2, -3, 4, 5]
        result = list(double(filter_positive(nums)))
        assert result == [4, 8, 10]


class TestContextManager:
    def test_capture(self):
        with capture_output() as out:
            out.append("test")
        assert out == ["test"]
