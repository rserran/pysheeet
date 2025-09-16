
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
- `Operating System <docs/notes/os/python-os.rst>`_


Advanced Cheat Sheet
====================

- `Regular expression <docs/notes/basic/python-rexp.rst>`_
- `Socket <docs/notes/os/python-socket.rst>`_
- `Asyncio <docs/notes/multitasking/python-asyncio.rst>`_
- `Concurrency <docs/notes/multitasking/python-concurrency.rst>`_
- `Sqlalchemy <docs/notes/database/python-sqlalchemy.rst>`_
- `Security <docs/notes/security/python-security.rst>`_
- `SSH <docs/notes/security/python-ssh.rst>`_
- `Tests <docs/notes/testing/python-tests.rst>`_
- `C Extensions <docs/notes/extension/python-c-extensions.rst>`_
- `PyTorch <docs/notes/pytorch/pytorch.rst>`_
- `Slurm <docs/notes/pytorch/slurm.rst>`_


Appendix
=========

- `A Hitchhikers Guide to Asynchronous Programming <docs/notes/appendix/python-concurrent.rst>`_
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
