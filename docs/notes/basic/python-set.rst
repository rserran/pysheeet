.. meta::
    :description lang=en: Python set cheat sheet covering set comprehensions, set operations (union, intersection, difference, symmetric difference), removing duplicates from lists, checking subsets and supersets, and frozenset with practical code examples
    :keywords: Python, Python Set, set comprehension, set operations, union, intersection, difference, symmetric difference, frozenset, Python unique list, subset, superset

===
Set
===

.. contents:: Table of Contents
    :backlinks: none

Sets are unordered collections of unique elements in Python. They provide O(1)
average time complexity for membership testing and support mathematical set
operations like union, intersection, and difference. This cheat sheet covers
set comprehensions, common set operations, uniquifying lists, and the immutable
frozenset type.

The source code is available on `GitHub <https://github.com/crazyguitar/pysheeet/blob/master/src/basic/set.py>`_.

References
----------

- `Set Types — set, frozenset <https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset>`_
- `Sets <https://docs.python.org/3/tutorial/datastructures.html#sets>`_

Create a Set
------------

Create sets using curly braces ``{}`` or the ``set()`` constructor. Note that
empty curly braces ``{}`` create a dict, not a set.

.. code-block:: python

    >>> s = {1, 2, 3}
    >>> s
    {1, 2, 3}
    >>> s = set([1, 2, 2, 3])
    >>> s
    {1, 2, 3}
    >>> empty = set()  # not {}
    >>> type(empty)
    <class 'set'>

Create Sets with Set Comprehension
----------------------------------

Like list comprehensions, set comprehensions provide a concise way to create sets.
The syntax uses curly braces ``{}`` instead of square brackets.

.. code-block:: python

    >>> a = [1, 2, 5, 6, 6, 6, 7]
    >>> s = {x for x in a}
    >>> s
    {1, 2, 5, 6, 7}
    >>> s = {x for x in a if x > 3}
    >>> s
    {5, 6, 7}
    >>> s = {x ** 2 for x in range(5)}
    >>> s
    {0, 1, 4, 9, 16}

Remove Duplicates from a List
-----------------------------

Converting a list to a set automatically removes duplicate elements. This is one
of the most common use cases for sets.

.. code-block:: python

    >>> a = [1, 2, 2, 2, 3, 4, 5, 5]
    >>> list(set(a))
    [1, 2, 3, 4, 5]

To preserve the original order, use ``dict.fromkeys()`` (Python 3.7+):

.. code-block:: python

    >>> a = [3, 1, 2, 1, 3, 2]
    >>> list(dict.fromkeys(a))
    [3, 1, 2]

Add Items to a Set
------------------

Use ``add()`` to add a single element, or ``update()`` to add multiple elements.

.. code-block:: python

    >>> s = {1, 2, 3}
    >>> s.add(4)
    >>> s
    {1, 2, 3, 4}
    >>> s.update([5, 6, 7])
    >>> s
    {1, 2, 3, 4, 5, 6, 7}
    >>> s |= {8, 9}  # same as update
    >>> s
    {1, 2, 3, 4, 5, 6, 7, 8, 9}

Remove Items from a Set
-----------------------

Use ``remove()`` to remove an element (raises KeyError if not found), or
``discard()`` to remove without error. Use ``pop()`` to remove an arbitrary element.

.. code-block:: python

    >>> s = {1, 2, 3, 4, 5}
    >>> s.remove(3)
    >>> s
    {1, 2, 4, 5}
    >>> s.discard(10)  # no error if not found
    >>> s.pop()  # remove arbitrary element
    1
    >>> s.clear()  # remove all
    >>> s
    set()

Union with ``|`` Operator
-------------------------

The union of two sets contains all elements from both sets. Use the ``|`` operator
or the ``union()`` method.

.. code-block:: python

    >>> a = {1, 2, 3}
    >>> b = {3, 4, 5}
    >>> a | b
    {1, 2, 3, 4, 5}
    >>> a.union(b)
    {1, 2, 3, 4, 5}
    >>> a | b | {6, 7}  # multiple sets
    {1, 2, 3, 4, 5, 6, 7}

Intersection with ``&`` Operator
--------------------------------

The intersection of two sets contains only elements that exist in both sets.
Use the ``&`` operator or the ``intersection()`` method.

.. code-block:: python

    >>> a = {1, 2, 3, 4}
    >>> b = {3, 4, 5, 6}
    >>> a & b
    {3, 4}
    >>> a.intersection(b)
    {3, 4}

Find Common Elements Between Lists
----------------------------------

Finding common items between two lists is a practical application of set
intersection.

.. code-block:: python

    >>> a = [1, 1, 2, 3]
    >>> b = [3, 5, 5, 6]
    >>> list(set(a) & set(b))
    [3]

Difference with ``-`` Operator
------------------------------

The difference of two sets contains elements that are in the first set but not
in the second. Use the ``-`` operator or the ``difference()`` method.

.. code-block:: python

    >>> a = {1, 2, 3, 4}
    >>> b = {3, 4, 5, 6}
    >>> a - b
    {1, 2}
    >>> b - a
    {5, 6}

Symmetric Difference with ``^`` Operator
----------------------------------------

The symmetric difference contains elements that are in either set, but not in
both. Use the ``^`` operator or the ``symmetric_difference()`` method.

.. code-block:: python

    >>> a = {1, 2, 3}
    >>> b = {3, 4, 5}
    >>> a ^ b
    {1, 2, 4, 5}

Check Subset with ``<=`` Operator
---------------------------------

Use ``<=`` or ``issubset()`` to check if all elements of one set are in another.
Use ``<`` for proper subset (subset but not equal).

.. code-block:: python

    >>> a = {1, 2}
    >>> b = {1, 2, 3, 4}
    >>> a <= b  # a is subset of b
    True
    >>> a < b   # a is proper subset
    True
    >>> a <= a  # equal sets
    True
    >>> a < a   # not proper subset
    False

Check Superset with ``>=`` Operator
-----------------------------------

Use ``>=`` or ``issuperset()`` to check if a set contains all elements of another.

.. code-block:: python

    >>> a = {1, 2, 3, 4}
    >>> b = {1, 2}
    >>> a >= b  # a is superset of b
    True
    >>> a > b   # a is proper superset
    True

Check Disjoint Sets
-------------------

Two sets are disjoint if they have no elements in common. Use ``isdisjoint()``
to check.

.. code-block:: python

    >>> a = {1, 2, 3}
    >>> b = {4, 5, 6}
    >>> a.isdisjoint(b)
    True
    >>> c = {3, 4, 5}
    >>> a.isdisjoint(c)
    False

Membership Testing
------------------

Sets provide O(1) average time complexity for membership testing, making them
much faster than lists for this operation.

.. code-block:: python

    >>> s = {1, 2, 3, 4, 5}
    >>> 3 in s
    True
    >>> 10 in s
    False
    >>> 10 not in s
    True

Frozenset - Immutable Set
-------------------------

``frozenset`` is an immutable version of set. It can be used as a dictionary key
or as an element of another set.

.. code-block:: python

    >>> fs = frozenset([1, 2, 3])
    >>> fs
    frozenset({1, 2, 3})
    >>> fs.add(4)  # raises AttributeError
    AttributeError: 'frozenset' object has no attribute 'add'

Use frozenset as dictionary key:

.. code-block:: python

    >>> d = {frozenset([1, 2]): "a", frozenset([3, 4]): "b"}
    >>> d[frozenset([1, 2])]
    'a'

Use frozenset in a set:

.. code-block:: python

    >>> s = {frozenset([1, 2]), frozenset([3, 4])}
    >>> frozenset([1, 2]) in s
    True

Set Operations Summary
----------------------

.. code-block:: python

    # Creation
    s = {1, 2, 3}           # literal
    s = set([1, 2, 3])      # from iterable
    s = {x for x in range(5)}  # comprehension

    # Add/Remove
    s.add(x)                # add single element
    s.update([x, y])        # add multiple elements
    s.remove(x)             # remove (KeyError if missing)
    s.discard(x)            # remove (no error if missing)
    s.pop()                 # remove arbitrary element
    s.clear()               # remove all

    # Set Operations
    a | b                   # union
    a & b                   # intersection
    a - b                   # difference
    a ^ b                   # symmetric difference

    # Comparisons
    a <= b                  # subset
    a < b                   # proper subset
    a >= b                  # superset
    a > b                   # proper superset
    a.isdisjoint(b)         # no common elements

    # Membership
    x in s                  # O(1) lookup
    x not in s
