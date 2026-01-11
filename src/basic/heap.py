"""Python Heap Examples

Source code for docs/notes/basic/python-heap.rst
"""

import heapq
import pytest


# Basic Heap Operations
def heapify_list(items: list) -> list:
    """Convert list to heap in-place."""
    h = items.copy()
    heapq.heapify(h)
    return h


def heap_push(h: list, item) -> list:
    """Push item onto heap."""
    heapq.heappush(h, item)
    return h


def heap_pop(h: list):
    """Pop smallest item from heap."""
    return heapq.heappop(h)


# Heap Sort
def heap_sort(items: list) -> list:
    """Sort using heap."""
    h = items.copy()
    heapq.heapify(h)
    return [heapq.heappop(h) for _ in range(len(h))]


# Max Heap
def max_heap_sort(items: list) -> list:
    """Sort descending using negated values."""
    h = [-x for x in items]
    heapq.heapify(h)
    return [-heapq.heappop(h) for _ in range(len(h))]


class MaxHeapItem:
    """Wrapper for max heap behavior."""

    def __init__(self, val):
        self.val = val

    def __lt__(self, other):
        return self.val > other.val


# Priority Queue
def priority_queue_example():
    """Priority queue using tuples."""
    pq = []
    heapq.heappush(pq, (2, "medium"))
    heapq.heappush(pq, (1, "high"))
    heapq.heappush(pq, (3, "low"))
    return [heapq.heappop(pq) for _ in range(len(pq))]


# Custom Objects
class Task:
    """Task with priority for heap."""

    def __init__(self, priority: int, name: str):
        self.priority = priority
        self.name = name

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return f"Task({self.priority}, {self.name!r})"


def task_queue():
    """Process tasks by priority."""
    h = []
    heapq.heappush(h, Task(3, "low"))
    heapq.heappush(h, Task(1, "high"))
    heapq.heappush(h, Task(2, "medium"))
    return [heapq.heappop(h) for _ in range(len(h))]


# K Smallest/Largest
def k_smallest(items: list, k: int) -> list:
    """Find k smallest elements."""
    return heapq.nsmallest(k, items)


def k_largest(items: list, k: int) -> list:
    """Find k largest elements."""
    return heapq.nlargest(k, items)


# Merge Sorted
def merge_sorted(*iterables) -> list:
    """Merge sorted iterables."""
    return list(heapq.merge(*iterables))


# Tests
class TestBasicHeap:
    def test_heapify(self):
        h = heapify_list([5, 1, 3, 2, 6])
        assert h[0] == 1  # min at root

    def test_push_pop(self):
        h = []
        heap_push(h, 3)
        heap_push(h, 1)
        heap_push(h, 2)
        assert heap_pop(h) == 1
        assert heap_pop(h) == 2


class TestHeapSort:
    def test_sort(self):
        assert heap_sort([5, 1, 3, 2, 6]) == [1, 2, 3, 5, 6]

    def test_max_sort(self):
        assert max_heap_sort([5, 1, 3, 2, 6]) == [6, 5, 3, 2, 1]


class TestPriorityQueue:
    def test_priority_order(self):
        result = priority_queue_example()
        assert result[0] == (1, "high")
        assert result[1] == (2, "medium")
        assert result[2] == (3, "low")


class TestCustomObjects:
    def test_max_heap_item(self):
        h = []
        for x in [5, 1, 3]:
            heapq.heappush(h, MaxHeapItem(x))
        assert heapq.heappop(h).val == 5

    def test_task_queue(self):
        tasks = task_queue()
        assert tasks[0].name == "high"
        assert tasks[1].name == "medium"
        assert tasks[2].name == "low"


class TestKElements:
    def test_k_smallest(self):
        assert k_smallest([5, 1, 8, 3, 9], 3) == [1, 3, 5]

    def test_k_largest(self):
        assert k_largest([5, 1, 8, 3, 9], 3) == [9, 8, 5]


class TestMerge:
    def test_merge_sorted(self):
        assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
