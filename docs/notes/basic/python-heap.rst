.. meta::
    :description lang=en: Python heap and priority queue cheat sheet covering heapq module operations, heap sort algorithm, priority queue implementation with custom comparators, and practical examples
    :keywords: Python, Python Cheat Sheet, heap, heapq, priority queue, heap sort, min heap, max heap, Python heapq, nlargest, nsmallest

====
Heap
====

.. contents:: Table of Contents
    :backlinks: none

The heapq module provides an implementation of the heap queue algorithm, also
known as the priority queue algorithm. Heaps are binary trees where every parent
node has a value less than or equal to any of its children (min-heap). This
cheat sheet covers heap operations including heap sort, priority queues, merging
sorted iterables, and finding the n largest or smallest elements efficiently.

The source code is available on `GitHub <https://github.com/crazyguitar/pysheeet/blob/master/src/basic/heap.py>`_.

References
----------

- `heapq — Heap queue algorithm <https://docs.python.org/3/library/heapq.html>`_
- `queue.PriorityQueue <https://docs.python.org/3/library/queue.html#queue.PriorityQueue>`_

Implement Heap Sort with ``heapq``
----------------------------------

Heap sort works by pushing all elements onto a heap and then popping them off
one by one. Since the heap maintains the min-heap property, elements come out
in sorted order. The time complexity is O(n log n).

.. code-block:: python

    >>> import heapq
    >>> a = [5, 1, 3, 2, 6]
    >>> h = []
    >>> for x in a:
    ...     heapq.heappush(h, x)
    ...
    >>> x = [heapq.heappop(h) for _ in range(len(a))]
    >>> x
    [1, 2, 3, 5, 6]

Implement Priority Queue with ``heapq``
---------------------------------------

A priority queue processes elements based on their priority rather than insertion
order. Use tuples ``(priority, value)`` where lower numbers indicate higher priority.
For custom objects, implement the ``__lt__`` method to define comparison behavior.

.. code-block:: python

   import heapq

    h = []
    heapq.heappush(h, (1, "1")) # (priority, value)
    heapq.heappush(h, (5, "5"))
    heapq.heappush(h, (3, "3"))
    heapq.heappush(h, (2, "2"))
    x = [heapq.heappop(h) for _ in range(len(h))]
    print(x)

.. code-block:: python

    import heapq

    class Num(object):
        def __init__(self, n):
            self._n = n

        def __lt__(self, other):
            return self._n < other._n

        def __repr__(self):
            return self.__str__()

        def __str__(self):
            return f"Num({self._n})"

    h = []
    heapq.heappush(h, Num(5))
    heapq.heappush(h, Num(2))
    heapq.heappush(h, Num(1))
    x = [heapq.heappop(h) for _ in range(len(h))]
    print(x)
    # output: [Num(1), Num(2), Num(5)]
