.. meta::
    :description lang=en: Comprehensive Python C API tutorial covering native C extension development, module creation, argument parsing, reference counting, GIL management, exception handling, and Python type manipulation including lists, dictionaries, tuples, sets, and strings
    :keywords: Python, C API, C Extension, PyObject, reference counting, GIL, module, CPython, native extension, PyList, PyDict, PyTuple, PySet, PyUnicode, memory management

============
Python C API
============

.. contents:: Table of Contents
    :backlinks: none

The Python C API is the traditional and most powerful way to write native extensions
for CPython. It provides direct access to Python's internals, giving developers
complete control over memory management, object creation, and interpreter interaction.
While more verbose than modern alternatives like pybind11 or cffi, the C API remains
essential for maintaining legacy extensions, understanding how Python works internally,
implementing performance-critical code paths, or accessing low-level features not
exposed by higher-level tools. The C API is also the foundation upon which tools like
Cython and pybind11 are built.

.. warning::

    The C extension interface is specific to CPython and may not work on alternative
    Python implementations like PyPy, Jython, or GraalPython. Additionally, the API
    can change between Python versions (especially between Python 2 and Python 3),
    requiring careful version handling and conditional compilation for compatibility.

Simple setup.py
---------------

Building C extensions requires a ``setup.py`` file that tells Python how to compile
your C code. The ``distutils`` module (or its modern replacement ``setuptools``)
handles cross-platform compilation, linking against the Python library, and generating
the correct shared library format (.so on Linux, .dylib on macOS, .pyd on Windows).
This minimal example compiles a single C file into a Python-importable module.

.. code-block:: python

    from distutils.core import setup, Extension

    ext = Extension('foo', sources=['foo.c'])
    setup(name="Foo", version="1.0", ext_modules=[ext])

Build and install:

.. code-block:: bash

    $ python setup.py build
    $ python setup.py install

Customize CFLAGS
----------------

For production-quality extensions, you'll want to customize compiler flags to enable
warnings, optimizations, or debugging symbols. The ``extra_compile_args`` parameter
passes flags directly to the C compiler (gcc, clang, or MSVC). Common flags include
``-Wall`` and ``-Wextra`` for comprehensive warnings, ``-Werror`` to treat warnings
as errors, ``-O3`` for aggressive optimization, and ``-g`` for debug symbols.

.. code-block:: python

    import sysconfig
    from distutils.core import setup, Extension

    cflags = sysconfig.get_config_var("CFLAGS")
    extra_compile_args = cflags.split()
    extra_compile_args += ["-Wextra", "-Wall", "-Werror"]

    ext = Extension(
        "foo", ["foo.c"],
        extra_compile_args=extra_compile_args
    )

    setup(name="foo", version="1.0", ext_modules=[ext])

Simple C Extension
------------------

:Source: `src/cext/capi/simple.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/simple.c>`_

Every Python C extension follows a standard structure with three essential components:
a module definition (``PyModuleDef``) that describes the module's name and methods,
a method table (``PyMethodDef``) that maps Python function names to C functions, and
an initialization function (``PyInit_<modulename>``) that Python calls when importing
the module. The ``PyDoc_STRVAR`` macro creates docstrings that appear in Python's
``help()`` system. This example demonstrates a minimal working extension.

**foo.c:**

.. code-block:: c

    #include <Python.h>

    PyDoc_STRVAR(doc_mod, "Module document\n");
    PyDoc_STRVAR(doc_foo, "foo() -> None\n\nPrint 'foo' to stdout.");

    static PyObject* foo(PyObject* self)
    {
        PyObject* s = PyUnicode_FromString("foo");
        PyObject_Print(s, stdout, 0);
        Py_DECREF(s);
        Py_RETURN_NONE;
    }

    static PyMethodDef methods[] = {
        {"foo", (PyCFunction)foo, METH_NOARGS, doc_foo},
        {NULL, NULL, 0, NULL}
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT,
        "foo",      /* module name */
        doc_mod,    /* docstring */
        -1,         /* size of per-interpreter state (-1 = global) */
        methods
    };

    PyMODINIT_FUNC PyInit_foo(void)
    {
        return PyModule_Create(&module);
    }

Output:

.. code-block:: bash

    $ python setup.py -q build && python setup.py -q install
    $ python -c "import foo; foo.foo()"
    'foo'

Parse Arguments
---------------

:Source: `src/cext/capi/args.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/args.c>`_

C extension functions receive arguments as ``PyObject*`` pointers and must parse them
into C types. The ``PyArg_ParseTuple()`` function handles positional arguments using
format codes: ``i`` for int, ``l`` for long, ``d`` for double, ``s`` for string,
``O`` for any Python object. For keyword arguments, use ``PyArg_ParseTupleAndKeywords()``.
The method flags (``METH_NOARGS``, ``METH_O``, ``METH_VARARGS``, ``METH_KEYWORDS``)
tell Python how to call your function and must match your implementation.

.. code-block:: c

    #include <Python.h>

    // No arguments: METH_NOARGS
    static PyObject *
    foo(PyObject *self)
    {
        Py_RETURN_NONE;
    }

    // Single object argument: METH_O
    static PyObject *
    bar(PyObject *self, PyObject *arg)
    {
        return Py_BuildValue("O", arg);
    }

    // Multiple positional arguments: METH_VARARGS
    static PyObject *
    baz(PyObject *self, PyObject *args)
    {
        PyObject *x = NULL, *y = NULL;
        if (!PyArg_ParseTuple(args, "OO", &x, &y)) {
            return NULL;
        }
        return Py_BuildValue("OO", x, y);
    }

    // Keyword arguments: METH_VARARGS | METH_KEYWORDS
    static PyObject *
    qux(PyObject *self, PyObject *args, PyObject *kwargs)
    {
        static char *keywords[] = {"x", "y", NULL};
        PyObject *x = NULL, *y = NULL;
        if (!PyArg_ParseTupleAndKeywords(args, kwargs,
                                         "O|O", keywords,
                                         &x, &y))
        {
            return NULL;
        }
        if (!y) {
            y = Py_None;
        }
        return Py_BuildValue("OO", x, y);
    }

    static PyMethodDef methods[] = {
        {"foo", (PyCFunction)foo, METH_NOARGS, NULL},
        {"bar", (PyCFunction)bar, METH_O, NULL},
        {"baz", (PyCFunction)baz, METH_VARARGS, NULL},
        {"qux", (PyCFunction)qux, METH_VARARGS | METH_KEYWORDS, NULL},
        {NULL, NULL, 0, NULL}
    };

Output:

.. code-block:: bash

    >>> import foo
    >>> foo.foo()
    >>> foo.bar(3.7)
    3.7
    >>> foo.baz(3, 7)
    (3, 7)
    >>> foo.qux(x=3, y=7)
    (3, 7)

Release the GIL
---------------

:Source: `src/cext/capi/gil.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/gil.c>`_

The Global Interpreter Lock (GIL) is a mutex that protects access to Python objects,
preventing multiple native threads from executing Python bytecode simultaneously.
While the GIL simplifies CPython's implementation, it can become a bottleneck for
CPU-bound multi-threaded code. For long-running C operations that don't access Python
objects (file I/O, network calls, heavy computation), release the GIL using
``Py_BEGIN_ALLOW_THREADS`` and ``Py_END_ALLOW_THREADS`` macros. This allows other
Python threads to run concurrently, dramatically improving multi-threaded performance.

.. code-block:: c

    #include <Python.h>

    static PyObject* foo(PyObject* self)
    {
        Py_BEGIN_ALLOW_THREADS
        sleep(3);  // Blocking operation - other threads can run
        Py_END_ALLOW_THREADS
        Py_RETURN_NONE;
    }

**With GIL released** (threads run concurrently):

.. code-block:: bash

    >>> import threading, foo
    >>> from datetime import datetime
    >>> def f(n):
    ...     print(f'{datetime.now()}: thread {n}')
    ...     foo.foo()
    >>> ts = [threading.Thread(target=f, args=(n,)) for n in range(3)]
    >>> [t.start() for t in ts]; [t.join() for t in ts]
    2018-11-04 20:15:34.860454: thread 0
    2018-11-04 20:15:34.860592: thread 1  # Same time!
    2018-11-04 20:15:34.860705: thread 2

**Without GIL release** (threads run sequentially):

.. code-block:: bash

    2018-11-04 20:16:44.055932: thread 0
    2018-11-04 20:16:47.059718: thread 1  # 3 seconds later
    2018-11-04 20:16:50.063579: thread 2  # 3 seconds later

.. warning::

    Never call Python C API functions between ``Py_BEGIN_ALLOW_THREADS`` and
    ``Py_END_ALLOW_THREADS``. The GIL must be held to safely access Python objects.

Acquire the GIL
---------------

:Source: `src/cext/capi/gil.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/gil.c>`_

When threads are created from C code (using pthreads or platform threading APIs),
they don't automatically hold the GIL. Before these threads can safely call any
Python C API function or access Python objects, they must acquire the GIL using
``PyGILState_Ensure()``. After completing Python operations, release the GIL with
``PyGILState_Release()`` to allow other threads to run. Failing to acquire the GIL
before accessing Python objects leads to crashes, data corruption, or undefined behavior.

.. code-block:: c

    void *worker_thread(void *arg)
    {
        PyObject *result = NULL;
        PyObject *callback = (PyObject *)arg;

        // Do C work here (no GIL needed)
        do_heavy_computation();

        // Acquire GIL before calling Python
        PyGILState_STATE state = PyGILState_Ensure();

        result = PyObject_CallFunction(callback, "s", "Done!");
        Py_XDECREF(result);

        // Release GIL
        PyGILState_Release(state);
        return NULL;
    }

Raise Exception
---------------

:Source: `src/cext/capi/errors.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/errors.c>`_

Error handling in C extensions follows a simple pattern: set an exception using
``PyErr_SetString()`` or ``PyErr_Format()``, then return ``NULL`` to signal failure.
Python provides built-in exception types as global variables: ``PyExc_ValueError``,
``PyExc_TypeError``, ``PyExc_RuntimeError``, ``PyExc_KeyError``, ``PyExc_IndexError``,
and many others. Always check return values from C API functions and propagate errors
by returning ``NULL`` when an exception is already set.

.. code-block:: c

    static PyObject*
    foo(PyObject* self)
    {
        PyErr_SetString(PyExc_NotImplementedError, "Not implemented");
        return NULL;
    }

Output:

.. code-block:: bash

    >>> import foo; foo.foo()
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    NotImplementedError: Not implemented

Custom Exception
----------------

:Source: `src/cext/capi/errors.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/errors.c>`_

For domain-specific errors, create custom exception classes using ``PyErr_NewException()``.
The first argument is the fully-qualified name (``"module.ExceptionName"``), the second
is the base class (``NULL`` defaults to ``Exception``), and the third is an optional
dictionary of class attributes. Register the exception as a module attribute so Python
code can catch it with ``except module.ExceptionName``. Remember to ``Py_INCREF()`` the
exception object before adding it to the module to prevent premature garbage collection.

.. code-block:: c

    static PyObject *FooError;

    static PyObject *
    foo(PyObject *self)
    {
        PyErr_SetString(FooError, "Something went wrong");
        return NULL;
    }

    PyMODINIT_FUNC PyInit_foo(void)
    {
        PyObject *m = PyModule_Create(&module);
        if (!m) return NULL;

        FooError = PyErr_NewException("foo.FooError", NULL, NULL);
        Py_INCREF(FooError);
        PyModule_AddObject(m, "FooError", FooError);
        return m;
    }

Output:

.. code-block:: bash

    >>> import foo; foo.foo()
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    foo.FooError: Something went wrong

Reference Counting
------------------

Python uses reference counting as its primary memory management strategy. Every
``PyObject*`` maintains a count of how many references point to it. When the count
reaches zero, the object is deallocated. Use ``Py_INCREF()`` when storing a new
reference to an object and ``Py_DECREF()`` when you're done with it. The variant
``Py_XDECREF()`` safely handles ``NULL`` pointers. Understanding reference counting
is crucial for avoiding memory leaks (forgetting to decref) and use-after-free bugs
(decrefing too early). Functions that return "new references" transfer ownership to
the caller, while "borrowed references" should not be decrefed.

.. code-block:: c

    static PyObject *
    getrefcount(PyObject *self, PyObject *a)
    {
        return PyLong_FromSsize_t(Py_REFCNT(a));
    }

Output:

.. code-block:: bash

    >>> import sys, foo
    >>> l = [1, 2, 3]
    >>> sys.getrefcount(l[0])
    104
    >>> foo.getrefcount(l[0])
    104
    >>> i = l[0]  # New reference
    >>> foo.getrefcount(l[0])
    105

Iterate a List
--------------

:Source: `src/cext/capi/types_demo.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/types_demo.c>`_

The Python C API provides two approaches for iterating over sequences. The generic
iterator protocol using ``PyObject_GetIter()`` and ``PyIter_Next()`` works with any
iterable object (lists, tuples, generators, custom iterables). For lists specifically,
you can use ``PyList_Size()`` and ``PyList_GetItem()`` for direct indexed access,
which is slightly faster but less flexible. Note that ``PyList_GetItem()`` returns
a borrowed reference, while ``PyIter_Next()`` returns a new reference that must be
decrefed after use.

.. code-block:: c

    static PyObject *iter_list(PyObject *self, PyObject *args) {
        PyObject *list, *iter, *item;
        if (!PyArg_ParseTuple(args, "O", &list)) {
            return NULL;
        }
        iter = PyObject_GetIter(list);
        if (!iter) return NULL;

        PyObject *result = PyList_New(0);
        while ((item = PyIter_Next(iter)) != NULL) {
            PyObject *doubled = PyLong_FromLong(PyLong_AsLong(item) * 2);
            PyList_Append(result, doubled);
            Py_DECREF(doubled);
            Py_DECREF(item);
        }
        Py_DECREF(iter);
        return result;
    }

Output:

.. code-block:: bash

    >>> import types_demo
    >>> types_demo.iter_list([1, 2, 3])
    [2, 4, 6]

Iterate a Dictionary
--------------------

:Source: `src/cext/capi/types_demo.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/types_demo.c>`_

Dictionary iteration in C uses ``PyDict_Next()`` with a position variable that tracks
the iteration state. Initialize ``pos`` to 0 before the loop, and the function updates
it automatically. The key and value pointers receive borrowed references to the current
item on each iteration—do not decref them unless you incref first. This function is
safe to use even if the dictionary is modified during iteration (though modifications
may cause items to be skipped or visited twice). For read-only iteration, this is the
most efficient approach.

.. code-block:: c

    static PyObject *iter_dict(PyObject *self, PyObject *args) {
        PyObject *dict;
        if (!PyArg_ParseTuple(args, "O!", &PyDict_Type, &dict)) {
            return NULL;
        }
        PyObject *result = PyList_New(0);
        PyObject *key, *value;
        Py_ssize_t pos = 0;
        while (PyDict_Next(dict, &pos, &key, &value)) {
            PyObject *pair = PyTuple_Pack(2, key, value);
            PyList_Append(result, pair);
            Py_DECREF(pair);
        }
        return result;
    }

Output:

.. code-block:: bash

    >>> import types_demo
    >>> types_demo.iter_dict({"a": 1, "b": 2})
    [('a', 1), ('b', 2)]

Create a List
-------------

:Source: `src/cext/capi/types_demo.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/types_demo.c>`_

Creating Python lists from C involves ``PyList_New()`` to allocate the list and
``PyList_Append()`` or ``PyList_SetItem()`` to populate it. When using ``PyList_New(n)``
with a non-zero size, you must initialize all slots with ``PyList_SetItem()`` before
the list is used. ``PyList_SetItem()`` steals a reference to the item, while
``PyList_Append()`` increments the reference count. For building lists dynamically,
start with ``PyList_New(0)`` and use ``PyList_Append()``.

.. code-block:: c

    static PyObject *list_demo(PyObject *self) {
        PyObject *list = PyList_New(0);
        PyList_Append(list, PyLong_FromLong(1));
        PyList_Append(list, PyLong_FromLong(2));
        PyList_Append(list, PyLong_FromLong(3));
        return list;
    }

Output:

.. code-block:: bash

    >>> import types_demo
    >>> types_demo.list_demo()
    [1, 2, 3]

Create a Dictionary
-------------------

:Source: `src/cext/capi/types_demo.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/types_demo.c>`_

Python dictionaries are created with ``PyDict_New()`` and populated using
``PyDict_SetItem()`` for PyObject keys or ``PyDict_SetItemString()`` for C string keys.
Both functions increment the reference count of the value, so you may need to decref
temporary objects after insertion. For retrieving values, ``PyDict_GetItem()`` and
``PyDict_GetItemString()`` return borrowed references (or NULL if the key doesn't exist),
while ``PyDict_GetItemWithError()`` distinguishes between missing keys and errors.

.. code-block:: c

    static PyObject *dict_demo(PyObject *self) {
        PyObject *dict = PyDict_New();
        PyDict_SetItemString(dict, "name", PyUnicode_FromString("Python"));
        PyDict_SetItemString(dict, "version", PyLong_FromLong(3));
        return dict;
    }

Output:

.. code-block:: bash

    >>> import types_demo
    >>> types_demo.dict_demo()
    {'name': 'Python', 'version': 3}

Create a Tuple
--------------

:Source: `src/cext/capi/types_demo.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/types_demo.c>`_

Tuples are immutable sequences, and the C API reflects this: once created and populated,
tuple contents cannot be changed. Use ``PyTuple_New(n)`` to create a tuple of size n,
then ``PyTuple_SetItem()`` to fill each slot (this steals a reference). Alternatively,
``Py_BuildValue()`` with parentheses format creates tuples directly from C values:
``"(isd)"`` creates a tuple of (int, string, double). ``PyTuple_Pack(n, ...)`` is
another convenient way to create tuples from existing PyObject pointers.

.. code-block:: c

    static PyObject *tuple_demo(PyObject *self) {
        return Py_BuildValue("(isd)", 1, "hello", 3.14);
    }

Output:

.. code-block:: bash

    >>> import types_demo
    >>> types_demo.tuple_demo()
    (1, 'hello', 3.14)

Create a Set
------------

:Source: `src/cext/capi/types_demo.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/types_demo.c>`_

Sets are unordered collections of unique hashable objects. Create an empty set with
``PySet_New(NULL)`` or initialize from an iterable with ``PySet_New(iterable)``.
Add elements with ``PySet_Add()``, which returns 0 on success or -1 on error (e.g.,
if the object is unhashable). Check membership with ``PySet_Contains()``, remove
elements with ``PySet_Discard()`` (no error if missing) or ``PySet_Pop()`` to remove
and return an arbitrary element. Duplicate additions are silently ignored.

.. code-block:: c

    static PyObject *set_demo(PyObject *self) {
        PyObject *set = PySet_New(NULL);
        PySet_Add(set, PyLong_FromLong(1));
        PySet_Add(set, PyLong_FromLong(2));
        PySet_Add(set, PyLong_FromLong(2));  /* duplicate ignored */
        PySet_Add(set, PyLong_FromLong(3));
        return set;
    }

Output:

.. code-block:: bash

    >>> import types_demo
    >>> types_demo.set_demo()
    {1, 2, 3}

String Operations
-----------------

:Source: `src/cext/capi/types_demo.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/types_demo.c>`_

Python 3 strings are Unicode objects, created with ``PyUnicode_FromString()`` for
UTF-8 encoded C strings or ``PyUnicode_FromFormat()`` for printf-style formatting.
Concatenate strings with ``PyUnicode_Concat()``, which returns a new string object.
For extracting C strings, use ``PyUnicode_AsUTF8()`` (returns a borrowed pointer valid
only while the object exists) or ``PyUnicode_AsUTF8AndSize()`` to also get the length.
The format function supports ``%s`` for C strings, ``%S`` for Python objects (calls str()),
``%R`` for repr(), and ``%d``, ``%u``, ``%ld`` for integers.

.. code-block:: c

    static PyObject *str_demo(PyObject *self) {
        PyObject *s1 = PyUnicode_FromString("Hello");
        PyObject *s2 = PyUnicode_FromString(" World");
        PyObject *result = PyUnicode_Concat(s1, s2);
        Py_DECREF(s1);
        Py_DECREF(s2);
        return result;
    }

    static PyObject *str_format(PyObject *self, PyObject *args) {
        const char *name;
        int age;
        if (!PyArg_ParseTuple(args, "si", &name, &age)) {
            return NULL;
        }
        return PyUnicode_FromFormat("%s is %d years old", name, age);
    }

Output:

.. code-block:: bash

    >>> import types_demo
    >>> types_demo.str_demo()
    'Hello World'
    >>> types_demo.str_format("Alice", 30)
    'Alice is 30 years old'

Bytes Operations
----------------

:Source: `src/cext/capi/types_demo.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/types_demo.c>`_

Bytes objects represent immutable sequences of bytes, essential for binary data, file I/O,
and network protocols. Create bytes from C strings with ``PyBytes_FromString()`` (copies
until null terminator) or ``PyBytes_FromStringAndSize()`` for binary data with embedded
nulls. Access the internal buffer with ``PyBytes_AsString()`` (borrowed pointer) and get
the length with ``PyBytes_Size()``. For mutable byte sequences, use ``PyByteArray_*``
functions instead. When parsing arguments, use format code ``s#`` for bytes with length
or ``S`` to accept only bytes objects.

.. code-block:: c

    static PyObject *bytes_demo(PyObject *self) {
        return PyBytes_FromString("hello bytes");
    }

    static PyObject *bytes_len(PyObject *self, PyObject *args) {
        PyObject *bytes;
        if (!PyArg_ParseTuple(args, "S", &bytes)) {
            return NULL;
        }
        return PyLong_FromSsize_t(PyBytes_Size(bytes));
    }

Output:

.. code-block:: bash

    >>> import types_demo
    >>> types_demo.bytes_demo()
    b'hello bytes'
    >>> types_demo.bytes_len(b"hello")
    5

Simple Class
------------

Defining custom Python types in C requires creating a ``PyTypeObject`` structure that
describes the type's behavior, memory layout, and methods. The minimal type needs
``tp_name`` (fully qualified name like ``"module.ClassName"``), ``tp_basicsize`` (size
of the instance struct), and ``tp_new`` (allocation function, often ``PyType_GenericNew``).
Call ``PyType_Ready()`` to finalize the type before use, then add it to your module with
``PyModule_AddObject()``. The ``Py_TPFLAGS_DEFAULT`` flag enables standard type features.

.. code-block:: c

    typedef struct {
        PyObject_HEAD
    } FooObject;

    static PyTypeObject FooType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "foo.Foo",
        .tp_doc = "Foo objects",
        .tp_basicsize = sizeof(FooObject),
        .tp_itemsize = 0,
        .tp_flags = Py_TPFLAGS_DEFAULT,
        .tp_new = PyType_GenericNew
    };

    PyMODINIT_FUNC PyInit_foo(void)
    {
        PyObject *m = NULL;
        if (PyType_Ready(&FooType) < 0)
            return NULL;
        if ((m = PyModule_Create(&module)) == NULL)
            return NULL;
        Py_INCREF(&FooType);
        PyModule_AddObject(m, "Foo", (PyObject *)&FooType);
        return m;
    }

Class with Members and Methods
------------------------------

Full-featured Python classes in C require implementing several type slots. Use
``PyMemberDef`` to expose C struct fields as Python attributes (with automatic type
conversion), and ``PyMethodDef`` for instance methods. Implement ``tp_new`` for memory
allocation (called before ``__init__``), ``tp_init`` for initialization (the ``__init__``
method), and ``tp_dealloc`` for cleanup (must decref all owned PyObject members and call
``tp_free``). The ``Py_TPFLAGS_BASETYPE`` flag allows the type to be subclassed in Python.

.. code-block:: c

    #include <Python.h>
    #include <structmember.h>

    typedef struct {
        PyObject_HEAD
        PyObject *foo;
        PyObject *bar;
    } FooObject;

    static void
    Foo_dealloc(FooObject *self)
    {
        Py_XDECREF(self->foo);
        Py_XDECREF(self->bar);
        Py_TYPE(self)->tp_free((PyObject *)self);
    }

    static PyObject *
    Foo_new(PyTypeObject *type, PyObject *args, PyObject *kw)
    {
        FooObject *self = (FooObject *)type->tp_alloc(type, 0);
        if (self) {
            self->foo = PyUnicode_FromString("");
            self->bar = PyUnicode_FromString("");
        }
        return (PyObject *)self;
    }

    static int
    Foo_init(FooObject *self, PyObject *args, PyObject *kw)
    {
        static char *keywords[] = {"foo", "bar", NULL};
        PyObject *foo = NULL, *bar = NULL;

        if (!PyArg_ParseTupleAndKeywords(args, kw, "|OO", keywords, &foo, &bar))
            return -1;

        if (foo) { Py_INCREF(foo); Py_XDECREF(self->foo); self->foo = foo; }
        if (bar) { Py_INCREF(bar); Py_XDECREF(self->bar); self->bar = bar; }
        return 0;
    }

    static PyMemberDef Foo_members[] = {
        {"foo", T_OBJECT_EX, offsetof(FooObject, foo), 0, "foo attribute"},
        {"bar", T_OBJECT_EX, offsetof(FooObject, bar), 0, "bar attribute"},
        {NULL}
    };

Output:

.. code-block:: bash

    >>> import foo
    >>> o = foo.Foo('hello', 'world')
    >>> o.foo
    'hello'
    >>> o.bar
    'world'

Properties (Getter/Setter)
--------------------------

For computed attributes or attributes requiring validation, use ``PyGetSetDef`` to define
properties with custom getter and setter functions. The getter receives the instance and
an optional closure pointer, returning a new reference to the attribute value. The setter
receives the instance, new value (or NULL for deletion), and closure, returning 0 on
success or -1 on error. This provides the same functionality as Python's ``@property``
decorator but with C-level control over attribute access.

.. code-block:: c

    static PyObject *
    Foo_getfoo(FooObject *self, void *closure)
    {
        Py_INCREF(self->foo);
        return self->foo;
    }

    static int
    Foo_setfoo(FooObject *self, PyObject *value, void *closure)
    {
        if (!value || !PyUnicode_Check(value)) {
            PyErr_SetString(PyExc_TypeError, "value must be a string");
            return -1;
        }
        Py_INCREF(value);
        Py_XDECREF(self->foo);
        self->foo = value;
        return 0;
    }

    static PyGetSetDef Foo_getsetters[] = {
        {"foo", (getter)Foo_getfoo, (setter)Foo_setfoo, "foo property", NULL},
        {NULL}
    };

Calling Python from C
---------------------

C extensions often need to call back into Python code—invoking callbacks, calling methods
on objects, or using Python library functions. Use ``PyObject_CallFunction()`` for calling
with C-style format arguments, ``PyObject_CallObject()`` with a tuple of arguments, or
``PyObject_CallMethod()`` to call a method by name. Always check if the callable is valid
with ``PyCallable_Check()`` before calling, and check the return value for NULL (indicating
an exception was raised). The GIL must be held when calling Python functions.

.. code-block:: c

    static PyObject *
    call_callback(PyObject *self, PyObject *args)
    {
        PyObject *callback = NULL;
        PyObject *result = NULL;

        if (!PyArg_ParseTuple(args, "O:callback", &callback))
            return NULL;

        if (!PyCallable_Check(callback)) {
            PyErr_SetString(PyExc_TypeError, "argument must be callable");
            return NULL;
        }

        // Call: callback("Hello from C!")
        result = PyObject_CallFunction(callback, "s", "Hello from C!");
        return result;
    }

Output:

.. code-block:: bash

    >>> import foo
    >>> foo.call_callback(print)
    Hello from C!

Performance Comparison
----------------------

:Source: `src/cext/capi/simple.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/capi/simple.c>`_

C extensions provide dramatic speedups for CPU-bound operations by eliminating Python's
interpreter overhead. This recursive Fibonacci benchmark demonstrates typical performance
gains of 50-100x compared to pure Python. The speedup comes from avoiding Python object
creation, method dispatch, and bytecode interpretation on each function call. For
numerical code, the gains can be even larger when combined with SIMD instructions or
multi-threading (with GIL released). However, the overhead of crossing the Python/C
boundary means C extensions are most beneficial for compute-intensive inner loops rather
than simple operations.

.. code-block:: c

    static unsigned long fib(unsigned long n)
    {
        if (n < 2) return n;
        return fib(n - 1) + fib(n - 2);
    }

    static PyObject *
    py_fib(PyObject *self, PyObject *args)
    {
        unsigned long n = 0;
        if (!PyArg_ParseTuple(args, "k", &n)) return NULL;
        return PyLong_FromUnsignedLong(fib(n));
    }

.. code-block:: python

    >>> from time import time
    >>> def py_fib(n):
    ...     if n < 2: return n
    ...     return py_fib(n-1) + py_fib(n-2)
    ...
    >>> s = time(); _ = py_fib(35); e = time(); e - s
    4.953313112258911
    >>> import foo
    >>> s = time(); _ = foo.fib(35); e = time(); e - s
    0.04628586769104004
