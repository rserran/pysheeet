
.. raw:: html

    <h1 align="center">
    <br>
      <a href="https://www.pythonsheets.com"><img src="docs/_static/logo.png" alt="pysheeet" width=200"></a>
    </h1>
    <p align="center">
      <a href="https://github.com/crazyguitar/pysheeet/actions">
        <img src="https://github.com/crazyguitar/pysheeet/actions/workflows/pythonpackage.yml/badge.svg" alt="Build Status">
      </a>
      <a href="https://coveralls.io/github/crazyguitar/pysheeet?branch=master">
        <img src="https://coveralls.io/repos/github/crazyguitar/pysheeet/badge.svg?branch=master" alt="Coverage">
      </a>
      <a href="https://raw.githubusercontent.com/crazyguitar/pysheeet/master/LICENSE">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License MIT">
      </a>
      <a href="https://doi.org/10.5281/zenodo.15529042">
        <img src="https://zenodo.org/badge/52760178.svg" alt="DOI">
      </a>
    </p>

Introduction
=============

This project was started to bring together useful Python code snippets that make
coding faster, easier, and more enjoyable. You can explore all the cheat sheets at
`Pysheeet <https://www.pythonsheets.com/>`_. Contributions are always welcome—feel
free to fork the repo and submit a pull request to help it grow!


What’s New In Python 3
======================

This part only provides a quick glance at some important features in Python 3.
If you're interested in all of the most important features, please read the
official document, `What’s New in Python <https://docs.python.org/3/whatsnew/index.html>`_.

- `New in Python3 <docs/notes/python-new-py3.rst>`_


Cheat Sheet
===========

- `From Scratch <docs/notes/basic/python-basic.rst>`_
- `Future <docs/notes/basic/python-future.rst>`_
- `Typing <docs/notes/basic/python-typing.rst>`_
- `Class <docs/notes/basic/python-object.rst>`_
- `Function <docs/notes/basic/python-func.rst>`_
- `Unicode <docs/notes/basic/python-unicode.rst>`_
- `List <docs/notes/basic/python-list.rst>`_
- `Set <docs/notes/basic/python-set.rst>`_
- `Dictionary <docs/notes/basic/python-dict.rst>`_
- `Heap <docs/notes/basic/python-heap.rst>`_
- `Generator <docs/notes/basic/python-generator.rst>`_
- `Time <docs/notes/os/python-date.rst>`_
- `File <docs/notes/os/python-io.rst>`_


Advanced Cheat Sheet
====================

- `Operating System <docs/notes/os/python-os.rst>`_
- `Regular expression <docs/notes/basic/python-rexp.rst>`_
- `Concurrency <docs/notes/multitasking/python-concurrency.rst>`_
- `PyTorch <docs/notes/pytorch/pytorch.rst>`_
- `Slurm <docs/notes/pytorch/slurm.rst>`_


Asyncio
=======

Asynchronous programming with Python's ``asyncio`` module. Covers coroutines,
event loops, tasks, networking, and advanced patterns.

- `A Hitchhiker's Guide to Asynchronous Programming <docs/notes/asyncio/python-asyncio-guide.rst>`_ - Design philosophy and evolution
- `Asyncio Basics <docs/notes/asyncio/python-asyncio-basic.rst>`_ - Coroutines, tasks, gather, timeouts
- `Asyncio Networking <docs/notes/asyncio/python-asyncio-server.rst>`_ - TCP/UDP servers, HTTP, SSL/TLS
- `Asyncio Advanced <docs/notes/asyncio/python-asyncio-advanced.rst>`_ - Synchronization, queues, subprocesses


C/C++ Extensions
================

Native extensions for performance-critical code. Covers modern pybind11 (used by
PyTorch, TensorFlow), ctypes, cffi, Cython, and the traditional Python C API.

- `ctypes <docs/notes/extension/python-ctypes.rst>`_ - Load shared libraries without compilation
- `Python C API <docs/notes/extension/python-capi.rst>`_ - Traditional C extension reference
- `Modern C/C++ Extensions <docs/notes/extension/python-cext-modern.rst>`_ - pybind11, Cython


Cryptography
============

Modern cryptographic practices using the ``cryptography`` library. Includes
algorithm recommendations, security checklists, and common mistakes to avoid.

- `Modern Cryptography <docs/notes/cryptography/python-crypto.rst>`_ - AES-GCM, RSA-OAEP, Ed25519, Argon2, key derivation
- `TLS/SSL and Certificates <docs/notes/cryptography/python-tls.rst>`_ - HTTPS servers, certificate generation, CSR, CA


Network
=======

- `Socket Basics <docs/notes/network/python-socket.rst>`_
- `Socket Servers <docs/notes/network/python-socket-server.rst>`_
- `Async Socket I/O <docs/notes/network/python-socket-async.rst>`_
- `SSL/TLS Sockets <docs/notes/network/python-socket-ssl.rst>`_
- `Packet Sniffing <docs/notes/network/python-socket-sniffer.rst>`_
- `SSH and Tunnels <docs/notes/network/python-ssh.rst>`_


Database
========

- `SQLAlchemy Basics <docs/notes/database/python-sqlalchemy.rst>`_
- `SQLAlchemy ORM <docs/notes/database/python-sqlalchemy-orm.rst>`_
- `SQLAlchemy Query Recipes <docs/notes/database/python-sqlalchemy-query.rst>`_


Appendix
=========

- `PEP 572 and the walrus operator <docs/notes/appendix/python-walrus.rst>`_
- `Python Interpreter in GNU Debugger <docs/notes/appendix/python-gdb.rst>`_

PDF Version
============

`pdf`_

.. _pdf: https://media.readthedocs.org/pdf/pysheeet/latest/pysheeet.pdf

How to run the server
=======================

.. code-block:: bash

    $ virtualenv venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt
    $ make
    $ python app.py

    # URL: localhost:5000
