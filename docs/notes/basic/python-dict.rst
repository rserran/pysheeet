.. meta::
    :description lang=en: Python dictionary cheat sheet covering creation, manipulation, merging, comprehensions, defaultdict, OrderedDict, and LRU cache with code examples
    :keywords: Python, Python3, Python dictionary, Python dict cheat sheet, dict, hashmap, key-value pairs, defaultdict, OrderedDict, dictionary comprehension, LRU cache, dict methods

==========
Dictionary
==========

.. contents:: Table of Contents
    :backlinks: none

Dictionaries are one of Python's most powerful and frequently used data structures.
They store key-value pairs and provide O(1) average time complexity for lookups,
insertions, and deletions. Since Python 3.7, dictionaries maintain insertion order
as a language feature. This cheat sheet covers essential dictionary operations,
from basic manipulation to advanced patterns like emulating dictionary behavior
with special methods and implementing an LRU (Least Recently Used) cache.

The source code is available on `GitHub <https://github.com/crazyguitar/pysheeet/blob/master/src/basic/dict.py>`_.

References
----------

- `Mapping Types — dict <https://docs.python.org/3/library/stdtypes.html#mapping-types-dict>`_
- `collections — Container datatypes <https://docs.python.org/3/library/collections.html>`_
- `PEP 584 -- Add Union Operators To dict <https://www.python.org/dev/peps/pep-0584/>`_

Get All Keys with ``dict.keys()``
---------------------------------

The ``keys()`` method returns a view object containing all dictionary keys.
In Python 3, this is a dynamic view that reflects changes to the dictionary.

.. code-block:: python

    >>> a = {"1":1, "2":2, "3":3}
    >>> b = {"2":2, "3":3, "4":4}
    >>> a.keys()
    ['1', '3', '2']

Get Key-Value Pairs with ``dict.items()``
-----------------------------------------

The ``items()`` method returns key-value pairs as tuples, which is useful for
iterating over both keys and values simultaneously.

.. code-block:: python

    >>> a = {"1":1, "2":2, "3":3}
    >>> a.items()

Find Common Keys Between Dictionaries
-------------------------------------

Finding keys that exist in multiple dictionaries is a common operation. Using
set intersection is the most efficient approach.

.. code-block:: python

    >>> a = {"1":1, "2":2, "3":3}
    >>> b = {"2":2, "3":3, "4":4}
    >>> [_ for _ in a.keys() if _ in b.keys()]
    ['3', '2']
    >>> # better way
    >>> c = set(a).intersection(set(b))
    >>> list(c)
    ['3', '2']
    >>> # or
    >>> [_ for _ in a if _ in b]
    ['3', '2']
    [('1', 1), ('3', 3), ('2', 2)]

Set Default Values with ``setdefault()`` and ``defaultdict``
------------------------------------------------------------

When working with dictionaries, you often need to set default values for missing
keys. Python provides ``setdefault()`` and ``collections.defaultdict`` for this.

.. code-block:: python

    >>> # intuitive but not recommend
    >>> d = {}
    >>> key = "foo"
    >>> if key not in d:
    ...     d[key] = []
    ...

    # using d.setdefault(key[, default])
    >>> d = {}
    >>> key = "foo"
    >>> d.setdefault(key, [])
    []
    >>> d[key] = 'bar'
    >>> d
    {'foo': 'bar'}

    # using collections.defaultdict
    >>> from collections import defaultdict
    >>> d = defaultdict(list)
    >>> d["key"]
    []
    >>> d["foo"]
    []
    >>> d["foo"].append("bar")
    >>> d
    defaultdict(<class 'list'>, {'key': [], 'foo': ['bar']})

``dict.setdefault(key[, default])`` returns its default value if *key* is not in
the dictionary. However, if the key exists in the dictionary, the function will
return its value.

.. code-block:: python

    >>> d = {}
    >>> d.setdefault("key", [])
    []
    >>> d["key"] = "bar"
    >>> d.setdefault("key", [])
    'bar'

Update Dictionary with ``dict.update()``
----------------------------------------

The ``update()`` method merges another dictionary into the current one. Keys from
the second dictionary overwrite existing keys in the first.

.. code-block:: python

    >>> a = {"1":1, "2":2, "3":3}
    >>> b = {"2":2, "3":3, "4":4}
    >>> a.update(b)
    >>> a
    {'1': 1, '3': 3, '2': 2, '4': 4}

Merge Two Dictionaries in Python
--------------------------------

There are several ways to merge dictionaries depending on your Python version.
Python 3.9+ also supports the ``|`` operator for dictionary merging.

Python 3.4 or lower

.. code-block:: python

    >>> a = {"x": 55, "y": 66}
    >>> b = {"a": "foo", "b": "bar"}
    >>> c = a.copy()
    >>> c.update(b)
    >>> c
    {'y': 66, 'x': 55, 'b': 'bar', 'a': 'foo'}


Python 3.5 or above

.. code-block:: python

    >>> a = {"x": 55, "y": 66}
    >>> b = {"a": "foo", "b": "bar"}
    >>> c = {**a, **b}
    >>> c
    {'x': 55, 'y': 66, 'a': 'foo', 'b': 'bar'}

Emulate a Dictionary with Special Methods
-----------------------------------------

You can create dictionary-like objects by implementing special methods:
``__getitem__``, ``__setitem__``, ``__delitem__``, ``__contains__``, and ``__iter__``.

.. code-block:: python

    >>> class EmuDict(object):
    ...   def __init__(self, dict_):
    ...     self._dict = dict_
    ...   def __repr__(self):
    ...     return "EmuDict: " + repr(self._dict)
    ...   def __getitem__(self, key):
    ...     return self._dict[key]
    ...   def __setitem__(self, key, val):
    ...     self._dict[key] = val
    ...   def __delitem__(self, key):
    ...     del self._dict[key]
    ...   def __contains__(self, key):
    ...     return key in self._dict
    ...   def __iter__(self):
    ...     return iter(self._dict.keys())
    ...
    >>> _ = {"1":1, "2":2, "3":3}
    >>> emud = EmuDict(_)
    >>> emud  # __repr__
    EmuDict: {'1': 1, '2': 2, '3': 3}
    >>> emud['1']  # __getitem__
    1
    >>> emud['5'] = 5  # __setitem__
    >>> emud
    EmuDict: {'1': 1, '2': 2, '3': 3, '5': 5}
    >>> del emud['2']  # __delitem__
    >>> emud
    EmuDict: {'1': 1, '3': 3, '5': 5}
    >>> for _ in emud:
    ...     print(emud[_], end=' ')  # __iter__
    ... else:
    ...     print()
    ...
    1 3 5
    >>> '1' in emud  # __contains__
    True

Implement LRU Cache with OrderedDict
------------------------------------

An LRU (Least Recently Used) cache evicts the least recently accessed items when
full. ``OrderedDict.move_to_end()`` makes implementation straightforward.

.. code-block:: python

	from collections import OrderedDict


	class LRU(object):
		def __init__(self, maxsize=128):
			self._maxsize = maxsize
			self._cache = OrderedDict()

		def get(self, k):
			if k not in self._cache:
				return None

			self._cache.move_to_end(k)
			return self._cache[k]

		def put(self, k, v):
			if k in self._cache:
				self._cache.move_to_end(k)
			self._cache[k] = v
			if len(self._cache) > self._maxsize:
				self._cache.popitem(last=False)

		def __str__(self):
			return str(self._cache)

		def __repr__(self):
			return self.__str__()

Note that dictionaries preserve insertion order from Python 3.7. Moreover,
updating a key does not affect the order. Therefore, a dictionary can also
simulate an LRU cache, which is similar to using an OrderedDict.

.. code-block:: python

	class LRU(object):
		def __init__(self, maxsize=128):
			self._maxsize = maxsize
			self._cache = {}

		def get(self, k):
			if k not in self._cache:
				return None

			self.move_to_end(k)
			return self._cache[k]

		def put(self, k, v):
			if k in self._cache:
				self.move_to_end(k)
			self._cache[k] = v
			if len(self._cache) > self._maxsize:
				self.pop()

		def pop(self):
			it = iter(self._cache.keys())
			del self._cache[next(it)]

		def move_to_end(self, k):
			if k not in self._cache:
				return
			v = self._cache[k]
			del self._cache[k]
			self._cache[k] = v

		def __str__(self):
			return str(self._cache)

		def __repr__(self):
			return self.__str__()
