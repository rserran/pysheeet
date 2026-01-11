"""Python Set Examples

Source code for docs/notes/basic/python-set.rst
"""

import pytest


# Create a Set
def create_set_literal():
    """Create set using literal syntax."""
    return {1, 2, 3}


def create_set_from_list(items: list) -> set:
    """Create set from list, removing duplicates."""
    return set(items)


# Set Comprehension
def set_comprehension_basic(items: list) -> set:
    """Basic set comprehension."""
    return {x for x in items}


def set_comprehension_filter(items: list, threshold: int) -> set:
    """Set comprehension with filter."""
    return {x for x in items if x > threshold}


def set_comprehension_squares(n: int) -> set:
    """Set of squares."""
    return {x**2 for x in range(n)}


# Uniquify
def uniquify_list(items: list) -> list:
    """Remove duplicates from list."""
    return list(set(items))


def uniquify_preserve_order(items: list) -> list:
    """Remove duplicates preserving order (Python 3.7+)."""
    return list(dict.fromkeys(items))


# Add Items
def add_single(s: set, item) -> set:
    """Add single item to set."""
    s.add(item)
    return s


def add_multiple(s: set, items) -> set:
    """Add multiple items to set."""
    s.update(items)
    return s


# Set Operations
def union(a: set, b: set) -> set:
    """Union of two sets."""
    return a | b


def intersection(a: set, b: set) -> set:
    """Intersection of two sets."""
    return a & b


def difference(a: set, b: set) -> set:
    """Difference of two sets (a - b)."""
    return a - b


def symmetric_difference(a: set, b: set) -> set:
    """Symmetric difference of two sets."""
    return a ^ b


def is_subset(a: set, b: set) -> bool:
    """Check if a is subset of b."""
    return a <= b


def is_superset(a: set, b: set) -> bool:
    """Check if a is superset of b."""
    return a >= b


def is_disjoint(a: set, b: set) -> bool:
    """Check if sets have no common elements."""
    return a.isdisjoint(b)


# Tests
class TestSetCreation:
    def test_literal(self):
        assert create_set_literal() == {1, 2, 3}

    def test_from_list(self):
        assert create_set_from_list([1, 2, 2, 3]) == {1, 2, 3}


class TestSetComprehension:
    def test_basic(self):
        assert set_comprehension_basic([1, 2, 2, 3]) == {1, 2, 3}

    def test_filter(self):
        assert set_comprehension_filter([1, 2, 3, 4, 5], 3) == {4, 5}

    def test_squares(self):
        assert set_comprehension_squares(5) == {0, 1, 4, 9, 16}


class TestUniquify:
    def test_uniquify(self):
        result = uniquify_list([1, 2, 2, 3, 3, 3])
        assert set(result) == {1, 2, 3}

    def test_preserve_order(self):
        assert uniquify_preserve_order([3, 1, 2, 1, 3]) == [3, 1, 2]


class TestSetOperations:
    def test_union(self):
        assert union({1, 2}, {2, 3}) == {1, 2, 3}

    def test_intersection(self):
        assert intersection({1, 2, 3}, {2, 3, 4}) == {2, 3}

    def test_difference(self):
        assert difference({1, 2, 3}, {2, 3, 4}) == {1}

    def test_symmetric_difference(self):
        assert symmetric_difference({1, 2, 3}, {2, 3, 4}) == {1, 4}

    def test_subset(self):
        assert is_subset({1, 2}, {1, 2, 3})
        assert not is_subset({1, 2, 3}, {1, 2})

    def test_superset(self):
        assert is_superset({1, 2, 3}, {1, 2})
        assert not is_superset({1, 2}, {1, 2, 3})

    def test_disjoint(self):
        assert is_disjoint({1, 2}, {3, 4})
        assert not is_disjoint({1, 2}, {2, 3})
