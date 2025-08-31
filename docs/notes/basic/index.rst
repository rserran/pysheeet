Quick Start
===========

This is another cheat sheet designed to help developers learn Python syntax from
the ground up. In addition to covering the basics, it also highlights common
patterns and practices that experienced Python developers use, which might seem
unusual to beginners. For instance, you may not have encountered constructs like
``for ... else ...`` in other programming languages.

.. toctree::
   :maxdepth: 1

   python-basic

The ``__future__`` module in Python is a special module that allows developers
to bring features from future Python versions into the current one. A well-known
example is print_function: in Python 2, print is a statement rather than a function,
so to use it as a function, you need to import it from the ``__future__`` module.
Interestingly, this module also contains a few hidden easter eggs.

.. toctree::
   :maxdepth: 1

   python-future

This cheat sheet demonstrates several common ways to declare or implement
functions in Python. For example, developers can define functions using the
familiar ``def`` keyword, similar to other programming languages. Alternatively,
functions can be created using the ``lambda`` syntax for inline or anonymous functions.
In some cases, you might need to modify existing functions—such as for performance
profiling or memory tracking. In these situations, the decorator pattern
(using the ``@`` syntax) is a powerful way to patch or extend functionality.

.. toctree::
   :maxdepth: 1

   python-func

Python is an object-oriented programming language, allowing developers to define
classes of objects that can interact with one another. This cheat sheet not only
covers the basics of class declaration but also demonstrates advanced techniques,
such as implementing design patterns like the Singleton pattern.

.. toctree::
   :maxdepth: 1

   python-object

Function annotations were introduced in Python 3.0 (PEP `3107 <https://peps.python.org/pep-3107/>`_)
and later evolved into Python’s optional static typing system. Unlike languages such as C or C++,
Python is dynamically typed, meaning developers can accidentally pass objects of
the wrong type. Additionally, performing type checks at runtime can be inefficient.
To address this, tools like mypy allow for static type checking without runtime
overhead. This cheat sheet provides common syntax examples for defining and
using type hints in Python.

.. toctree::
   :maxdepth: 1

   python-typing
