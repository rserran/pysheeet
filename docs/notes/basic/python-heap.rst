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

Basic Heap Operations
---------------------

The ``heapq`` module provides functions to create and manipulate heaps. Use
``heapify`` to convert a list into a heap in-place in O(n) time. Use ``heappush``
and ``heappop`` to add and remove elements while maintaining the heap property.

.. code-block:: python

    >>> import heapq
    >>> # Convert list to heap in-place
    >>> h = [5, 1, 3, 2, 6]
    >>> heapq.heapify(h)
    >>> h[0]  # smallest element at root
    1
    >>> # Push and pop
    >>> heapq.heappush(h, 0)
    >>> heapq.heappop(h)
    0
    >>> # Push and pop in one operation
    >>> heapq.heappushpop(h, 4)  # push 4, then pop smallest
    1
    >>> # Pop and push in one operation
    >>> heapq.heapreplace(h, 0)  # pop smallest, then push 0
    2

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

A more efficient approach uses ``heapify`` to convert the list in-place:

.. code-block:: python

    >>> import heapq
    >>> def heap_sort(items):
    ...     h = items.copy()
    ...     heapq.heapify(h)
    ...     return [heapq.heappop(h) for _ in range(len(h))]
    ...
    >>> heap_sort([5, 1, 3, 2, 6])
    [1, 2, 3, 5, 6]

Implement Max Heap
------------------

Python's ``heapq`` only provides a min-heap. To implement a max-heap, negate
the values when pushing and negate again when popping.

.. code-block:: python

    >>> import heapq
    >>> # Max heap using negation
    >>> h = []
    >>> for x in [5, 1, 3, 2, 6]:
    ...     heapq.heappush(h, -x)
    ...
    >>> [-heapq.heappop(h) for _ in range(len(h))]
    [6, 5, 3, 2, 1]

For custom objects, implement ``__lt__`` with reversed comparison:

.. code-block:: python

    import heapq

    class MaxHeapItem:
        def __init__(self, val):
            self.val = val

        def __lt__(self, other):
            return self.val > other.val  # reversed for max heap

    h = []
    for x in [5, 1, 3]:
        heapq.heappush(h, MaxHeapItem(x))

    print(heapq.heappop(h).val)  # 5 (largest)

Implement Priority Queue with ``heapq``
---------------------------------------

A priority queue processes elements based on their priority rather than insertion
order. Use tuples ``(priority, value)`` where lower numbers indicate higher priority.

.. code-block:: python

    >>> import heapq
    >>> pq = []
    >>> heapq.heappush(pq, (2, "medium"))
    >>> heapq.heappush(pq, (1, "high"))
    >>> heapq.heappush(pq, (3, "low"))
    >>> [heapq.heappop(pq) for _ in range(len(pq))]
    [(1, 'high'), (2, 'medium'), (3, 'low')]

For custom objects, implement the ``__lt__`` method to define comparison behavior:

.. code-block:: python

    import heapq

    class Task:
        def __init__(self, priority, name):
            self.priority = priority
            self.name = name

        def __lt__(self, other):
            return self.priority < other.priority

        def __repr__(self):
            return f"Task({self.priority}, {self.name!r})"

    h = []
    heapq.heappush(h, Task(3, "low"))
    heapq.heappush(h, Task(1, "high"))
    heapq.heappush(h, Task(2, "medium"))

    while h:
        print(heapq.heappop(h))
    # Task(1, 'high')
    # Task(2, 'medium')
    # Task(3, 'low')

Find K Largest or Smallest Elements
-----------------------------------

The ``nlargest`` and ``nsmallest`` functions efficiently find the k largest or
smallest elements. They are more efficient than sorting when k is small relative
to the list size.

.. code-block:: python

    >>> import heapq
    >>> nums = [5, 1, 8, 3, 9, 2, 7]
    >>> heapq.nsmallest(3, nums)
    [1, 2, 3]
    >>> heapq.nlargest(3, nums)
    [9, 8, 7]

Use the ``key`` parameter to extract comparison keys from complex objects:

.. code-block:: python

    >>> import heapq
    >>> data = [
    ...     {'name': 'Alice', 'score': 85},
    ...     {'name': 'Bob', 'score': 92},
    ...     {'name': 'Charlie', 'score': 78},
    ... ]
    >>> heapq.nlargest(2, data, key=lambda x: x['score'])
    [{'name': 'Bob', 'score': 92}, {'name': 'Alice', 'score': 85}]

Merge Sorted Iterables
----------------------

The ``merge`` function merges multiple sorted inputs into a single sorted output.
It returns an iterator, making it memory-efficient for large datasets.

.. code-block:: python

    >>> import heapq
    >>> a = [1, 3, 5, 7]
    >>> b = [2, 4, 6, 8]
    >>> c = [0, 9, 10]
    >>> list(heapq.merge(a, b, c))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

Use ``key`` and ``reverse`` parameters for custom merging:

.. code-block:: python

    >>> import heapq
    >>> # Merge in descending order
    >>> a = [5, 3, 1]
    >>> b = [6, 4, 2]
    >>> list(heapq.merge(a, b, reverse=True))
    [6, 5, 4, 3, 2, 1]

Maintain a Fixed-Size Heap
--------------------------

To maintain a heap of fixed size k (e.g., tracking top k elements), use
``heappushpop`` or check the size after each push.

.. code-block:: python

    >>> import heapq
    >>> def top_k(items, k):
    ...     """Keep track of k largest elements using min-heap."""
    ...     h = []
    ...     for x in items:
    ...         if len(h) < k:
    ...             heapq.heappush(h, x)
    ...         elif x > h[0]:
    ...             heapq.heapreplace(h, x)
    ...     return sorted(h, reverse=True)
    ...
    >>> top_k([5, 1, 8, 3, 9, 2, 7, 4, 6], 3)
    [9, 8, 7]

Heap with Index Tracking
------------------------

When you need to update priorities in a heap, use a dictionary to track element
positions or mark entries as invalid.

.. code-block:: python

    import heapq

    class IndexedHeap:
        def __init__(self):
            self.heap = []
            self.entry_finder = {}
            self.REMOVED = '<removed>'

        def push(self, item, priority):
            if item in self.entry_finder:
                self.remove(item)
            entry = [priority, item]
            self.entry_finder[item] = entry
            heapq.heappush(self.heap, entry)

        def remove(self, item):
            entry = self.entry_finder.pop(item)
            entry[-1] = self.REMOVED

        def pop(self):
            while self.heap:
                priority, item = heapq.heappop(self.heap)
                if item is not self.REMOVED:
                    del self.entry_finder[item]
                    return item
            raise KeyError('pop from empty heap')

    # Usage
    h = IndexedHeap()
    h.push('task1', 3)
    h.push('task2', 1)
    h.push('task1', 0)  # update priority
    print(h.pop())  # task1 (now has priority 0)
