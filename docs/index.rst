.. python-cheatsheet documentation master file, created by
   sphinx-quickstart on Sun Feb 28 09:26:04 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. meta::
    :description lang=en: Collect useful python snippets for pythoneers or non-pythoneers.
    :keywords: Python, Python Cheat Sheet


Welcome to Python Cheatsheet!
==============================

Welcome to pysheeet. This project aims at collecting useful Python snippets
in order to enhance pythoneers' coding experiences. Please feel free to
contribute if you have any awesome ideas for improvements to code snippets,
explanations, etc.

Any snippets are welcome. If you'd like to contribute, `fork pysheeet on GitHub`_.
If there is any question or suggestion, please create an issue on `GitHub Issues`_.

.. _fork pysheeet on GitHub: https://github.com/crazyguitar/pysheeet
.. _GitHub Issues: https://github.com/crazyguitar/pysheeet/issues

What's New In Python 3
----------------------

The official document, `What's New In Python`_, displays all of the most
important changes. However, if you're too busy to read the whole changes,
this part provides a brief glance of new features in Python 3.

.. _What's New In Python: https://docs.python.org/3/whatsnew/index.html

.. toctree::
   :maxdepth: 1

   notes/python-new-py3


Cheat Sheet
-----------

This part mainly focuses on common snippets in Python code. The cheat sheet not
only includes basic Python features but also data structures and algorithms.

.. toctree::
   :maxdepth: 1
   :caption: Quick Start

   notes/basic/python-basic
   notes/basic/python-future
   notes/basic/python-object
   notes/basic/python-typing
   notes/basic/python-func

.. toctree::
   :maxdepth: 1
   :caption: Container

   notes/container/python-list
   notes/container/python-set
   notes/container/python-dict
   notes/container/python-heap

.. toctree::
   :maxdepth: 1
   :caption: String

   notes/string/python-unicode
   notes/string/python-rexp

.. toctree::
   :maxdepth: 1
   :caption: Iteration

   notes/iteration/python-generator

.. toctree::
   :maxdepth: 1
   :caption: Operating System

   notes/os/python-date
   notes/os/python-os
   notes/os/python-io
   notes/os/python-socket


Advanced Cheat Sheet
--------------------

The goal of this part is to give common snippets including built-in and 3rd party
modules usages.

.. toctree::
   :maxdepth: 1

   notes/multitasking/python-asyncio
   notes/multitasking/python-concurrency
   notes/database/python-sqlalchemy
   notes/security/python-security
   notes/security/python-ssh
   notes/testing/python-tests
   notes/extension/python-c-extensions
   notes/pytorch/slurm

Appendix
--------

The appendix mainly focuses on some critical concepts missing in cheat sheets.

.. toctree::
    :maxdepth: 1

    appendix/python-decorator
    appendix/python-concurrent
    appendix/python-asyncio
    appendix/python-walrus
    appendix/python-gdb
