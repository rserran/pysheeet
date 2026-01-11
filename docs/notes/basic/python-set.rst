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

Create Sets with Set Comprehension
----------------------------------

Like list comprehensions, set comprehensions provide a concise way to create sets.
The syntax uses curly braces ``{}`` instead of square brackets. You can also add
conditions to filter elements or transform values using conditional expressions.

.. code-block:: python

    >>> a = [1, 2, 5, 6, 6, 6, 7]
    >>> s = {x for x in a}
    >>> s
    set([1, 2, 5, 6, 7])
    >>> s = {x for x in a if x > 3}
    >>> s
    set([5, 6, 7])
    >>> s = {x if x > 3 else -1 for x in a}
    >>> s
    set([6, 5, -1, 7])

Remove Duplicates from a List
-----------------------------

Converting a list to a set automatically removes duplicate elements. This is one
of the most common use cases for sets. Note that the original order may not be
preserved in Python versions before 3.7.

.. code-block:: python

    >>> a = [1, 2, 2, 2, 3, 4, 5, 5]
    >>> a
    [1, 2, 2, 2, 3, 4, 5, 5]
    >>> ua = list(set(a))
    >>> ua
    [1, 2, 3, 4, 5]

Union Two Sets with ``|`` Operator
----------------------------------

The union of two sets contains all elements from both sets. Use the ``|`` operator
or the ``union()`` method. You can also concatenate lists and convert to a set.

.. code-block:: python

    >>> a = set([1, 2, 2, 2, 3])
    >>> b = set([5, 5, 6, 6, 7])
    >>> a | b
    set([1, 2, 3, 5, 6, 7])
    >>> # or
    >>> a = [1, 2, 2, 2, 3]
    >>> b = [5, 5, 6, 6, 7]
    >>> set(a + b)
    set([1, 2, 3, 5, 6, 7])

Add Items to a Set with ``add()`` and ``|=``
--------------------------------------------

Use ``add()`` to add a single element to a set, or use the ``|=`` operator to
add multiple elements from another set. The ``update()`` method also works for
adding multiple elements.

.. code-block:: python

    >>> a = set([1, 2, 3, 3, 3])
    >>> a.add(5)
    >>> a
    set([1, 2, 3, 5])
    >>> # or
    >>> a = set([1, 2, 3, 3, 3])
    >>> a |= set([1, 2, 3, 4, 5, 6])
    >>> a
    set([1, 2, 3, 4, 5, 6])

Intersection of Two Sets with ``&`` Operator
--------------------------------------------

The intersection of two sets contains only elements that exist in both sets.
Use the ``&`` operator or the ``intersection()`` method.

.. code-block:: python

    >>> a = set([1, 2, 2, 2, 3])
    >>> b = set([1, 5, 5, 6, 6, 7])
    >>> a & b
    set([1])

Find Common Elements Between Sets
---------------------------------

Finding common items between two lists is a practical application of set
intersection. Convert both lists to sets and use the ``&`` operator.

.. code-block:: python

    >>> a = [1, 1, 2, 3]
    >>> b = [1, 3, 5, 5, 6, 6]
    >>> com = list(set(a) & set(b))
    >>> com
    [1, 3]

Check Subset and Superset with ``<=`` and ``>=``
------------------------------------------------

Use ``<=`` (subset) and ``>=`` (superset) operators to check if one set contains
all elements of another. The ``issubset()`` and ``issuperset()`` methods provide
the same functionality.

b contains a

.. code-block:: python

    >>> a = set([1, 2])
    >>> b = set([1, 2, 5, 6])
    >>> a <= b
    True

a contains b

.. code-block:: python

    >>> a = set([1, 2, 5, 6])
    >>> b = set([1, 5, 6])
    >>> a >= b
    True

Set Difference with ``-`` Operator
----------------------------------

The difference of two sets contains elements that are in the first set but not
in the second. Use the ``-`` operator or the ``difference()`` method.

.. code-block:: python

    >>> a = set([1, 2, 3])
    >>> b = set([1, 5, 6, 7, 7])
    >>> a - b
    set([2, 3])

Symmetric Difference with ``^`` Operator
----------------------------------------

The symmetric difference contains elements that are in either set, but not in
both. Use the ``^`` operator or the ``symmetric_difference()`` method.

.. code-block:: python

    >>> a = set([1,2,3])
    >>> b = set([1, 5, 6, 7, 7])
    >>> a ^ b
    set([2, 3, 5, 6, 7])
