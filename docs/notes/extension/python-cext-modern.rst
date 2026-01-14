.. meta::
    :description lang=en: Comprehensive guide to modern Python C/C++ extensions covering pybind11, ctypes, cffi, and Cython with practical examples for building high-performance Python modules, NumPy integration, GIL management, and class bindings
    :keywords: Python, Python3, pybind11, C Extension, C++, ctypes, cffi, Cython, NumPy, Performance, GIL, Native Code, PyTorch, TensorFlow, SciPy, shared library

=========================
Modern C/C++ Extensions
=========================

.. contents:: Table of Contents
    :backlinks: none

Python's flexibility and ease of use come at a performance cost compared to compiled
languages. When you need maximum speed for numerical computing, real-time processing,
system interfaces, or wrapping existing C/C++ libraries, native extensions bridge the
gap between Python's productivity and C/C++'s performance. This guide covers modern
approaches to building Python extensions: **pybind11** (the recommended choice for C++
projects), **ctypes/cffi** (for calling C libraries without compilation), and **Cython**
(for Python-like syntax that compiles to C). We compare each approach using the same
Fibonacci benchmark to help you choose the right tool for your specific use case.

.. note::

    For most C++ projects, **pybind11** is the recommended choice. It's used by
    major machine learning frameworks like PyTorch, TensorFlow, and scientific
    computing libraries like SciPy. pybind11 provides clean C++11 syntax, automatic
    type conversions between Python and C++ types, excellent NumPy integration for
    numerical computing, and seamless exception handling across language boundaries.

Comparison of Approaches
------------------------

::

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                    C/C++ EXTENSION APPROACHES                           │
    ├─────────────────────────────────────────────────────────────────────────┤
    │  APPROACH      │ PROS                      │ CONS                       │
    ├────────────────┼───────────────────────────┼────────────────────────────┤
    │  pybind11      │ Clean C++11 syntax        │ Requires C++ compiler      │
    │  (recommended) │ Automatic type conversion │ Compile step needed        │
    │                │ NumPy support built-in    │ C++ only (not C)           │
    │                │ Used by PyTorch, SciPy    │                            │
    ├────────────────┼───────────────────────────┼────────────────────────────┤
    │  ctypes        │ No compilation needed     │ Manual type declarations   │
    │                │ Standard library          │ Error-prone                │
    │                │ Works with any C library  │ No C++ support             │
    ├────────────────┼───────────────────────────┼────────────────────────────┤
    │  cffi          │ No compilation needed     │ Extra dependency           │
    │                │ Cleaner than ctypes       │ No C++ support             │
    │                │ PyPy compatible           │                            │
    ├────────────────┼───────────────────────────┼────────────────────────────┤
    │  Cython        │ Python-like syntax        │ New language to learn      │
    │                │ Gradual optimization      │ Build complexity           │
    │                │ Good NumPy integration    │ Debugging harder           │
    ├────────────────┼───────────────────────────┼────────────────────────────┤
    │  Python C API  │ Maximum control           │ Very verbose               │
    │  (legacy)      │ No dependencies           │ Manual refcounting         │
    │                │                           │ Error-prone                │
    └────────────────┴───────────────────────────┴────────────────────────────┘

    When to use what:
    - Wrapping existing C++ library → pybind11
    - Wrapping existing C library  → ctypes or cffi
    - Writing new high-perf code   → pybind11 or Cython
    - Need PyPy compatibility      → cffi or Cython
    - Quick prototype              → ctypes

pybind11: Getting Started
-------------------------

:Source: `src/cext/example.cpp <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/example.cpp>`_

pybind11 is a lightweight header-only C++ library that creates Python bindings for
existing C++ code. Unlike the traditional Python C API, pybind11 uses modern C++11
features like variadic templates and lambda expressions to provide a clean, intuitive
syntax. Installation is simple with ``pip install pybind11``, and it requires only a
C++11 compatible compiler (GCC 4.8+, Clang 3.3+, MSVC 2015+). The ``PYBIND11_MODULE``
macro defines the module entry point, and ``m.def()`` binds C++ functions to Python
with automatic type conversion for common types like int, float, string, and STL
containers.

**Simple function binding:**

.. code-block:: cpp

    // example.cpp
    #include <pybind11/pybind11.h>

    int add(int a, int b) {
        return a + b;
    }

    // Fibonacci for performance comparison
    unsigned long fib(unsigned long n) {
        if (n < 2) return n;
        return fib(n - 1) + fib(n - 2);
    }

    PYBIND11_MODULE(example, m) {
        m.doc() = "Example pybind11 module";
        m.def("add", &add, "Add two integers",
              pybind11::arg("a"), pybind11::arg("b"));
        m.def("fib", &fib, "Compute Fibonacci number");
    }

**Build with setup.py:**

.. code-block:: python

    # setup.py
    from pybind11.setup_helpers import Pybind11Extension, build_ext
    from setuptools import setup

    ext_modules = [
        Pybind11Extension(
            "example",
            ["example.cpp"],
        ),
    ]

    setup(
        name="example",
        ext_modules=ext_modules,
        cmdclass={"build_ext": build_ext},
    )

.. code-block:: bash

    $ pip install pybind11
    $ python setup.py build_ext --inplace
    $ python -c "import example; print(example.add(1, 2))"
    3
    $ python -c "import example; print(example.fib(35))"
    9227465

pybind11: Classes
-----------------

:Source: `src/cext/vector.cpp <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/vector.cpp>`_

pybind11 makes binding C++ classes to Python straightforward with the ``py::class_``
template. You can expose constructors with ``def(py::init<...>())``, member variables
with ``def_readwrite()`` or ``def_readonly()``, and methods with ``def()``. Python
special methods like ``__repr__``, ``__add__``, ``__eq__`` are bound by name, enabling
natural Python syntax for your C++ objects. Default argument values are supported via
``py::arg()``, and you can add docstrings to improve the Python help() experience.

.. code-block:: cpp

    // vector.cpp
    #include <pybind11/pybind11.h>
    #include <cmath>

    namespace py = pybind11;

    class Vector2D {
    public:
        double x, y;

        Vector2D(double x = 0, double y = 0) : x(x), y(y) {}

        double length() const {
            return std::sqrt(x * x + y * y);
        }

        Vector2D operator+(const Vector2D& other) const {
            return Vector2D(x + other.x, y + other.y);
        }

        std::string repr() const {
            return "Vector2D(" + std::to_string(x) + ", " + std::to_string(y) + ")";
        }
    };

    PYBIND11_MODULE(vector, m) {
        py::class_<Vector2D>(m, "Vector2D")
            .def(py::init<double, double>(),
                 py::arg("x") = 0, py::arg("y") = 0)
            .def_readwrite("x", &Vector2D::x)
            .def_readwrite("y", &Vector2D::y)
            .def("length", &Vector2D::length)
            .def("__add__", &Vector2D::operator+)
            .def("__repr__", &Vector2D::repr);
    }

.. code-block:: python

    >>> from vector import Vector2D
    >>> v1 = Vector2D(3, 4)
    >>> v1.length()
    5.0
    >>> v2 = Vector2D(1, 2)
    >>> v3 = v1 + v2
    >>> v3
    Vector2D(4.0, 6.0)

pybind11: NumPy Integration
---------------------------

:Source: `src/cext/numpy_example.cpp <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/numpy_example.cpp>`_

pybind11 provides first-class NumPy support through the ``pybind11/numpy.h`` header,
enabling high-performance numerical computing without data copying. The ``py::array_t<T>``
template wraps NumPy arrays with type safety, and ``unchecked<N>()`` provides fast,
bounds-check-free access for performance-critical inner loops. Arrays can be modified
in-place using ``mutable_unchecked<N>()``, or new arrays can be created and returned.
This zero-copy approach is essential for scientific computing where large datasets
would be expensive to duplicate.

.. code-block:: cpp

    // numpy_example.cpp
    #include <pybind11/pybind11.h>
    #include <pybind11/numpy.h>

    namespace py = pybind11;

    // Element-wise multiply (modifies in place)
    void multiply_inplace(py::array_t<double> arr, double factor) {
        auto buf = arr.mutable_unchecked<1>();
        for (py::ssize_t i = 0; i < buf.shape(0); i++) {
            buf(i) *= factor;
        }
    }

    // Return new array
    py::array_t<double> add_arrays(py::array_t<double> a, py::array_t<double> b) {
        auto buf_a = a.unchecked<1>();
        auto buf_b = b.unchecked<1>();

        if (buf_a.shape(0) != buf_b.shape(0)) {
            throw std::runtime_error("Arrays must have same length");
        }

        auto result = py::array_t<double>(buf_a.shape(0));
        auto buf_r = result.mutable_unchecked<1>();

        for (py::ssize_t i = 0; i < buf_a.shape(0); i++) {
            buf_r(i) = buf_a(i) + buf_b(i);
        }
        return result;
    }

    PYBIND11_MODULE(numpy_example, m) {
        m.def("multiply_inplace", &multiply_inplace);
        m.def("add_arrays", &add_arrays);
    }

.. code-block:: python

    >>> import numpy as np
    >>> from numpy_example import multiply_inplace, add_arrays
    >>> arr = np.array([1.0, 2.0, 3.0])
    >>> multiply_inplace(arr, 2.0)
    >>> arr
    array([2., 4., 6.])
    >>> a = np.array([1.0, 2.0, 3.0])
    >>> b = np.array([4.0, 5.0, 6.0])
    >>> add_arrays(a, b)
    array([5., 7., 9.])

pybind11: Releasing the GIL
---------------------------

:Source: `src/cext/gil_example.cpp <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/gil_example.cpp>`_

Python's Global Interpreter Lock (GIL) prevents true parallel execution of Python code
across threads. For CPU-intensive C++ operations or blocking I/O that doesn't need
Python objects, releasing the GIL allows other Python threads to run concurrently.
pybind11 provides ``py::gil_scoped_release`` for RAII-style GIL management—the GIL is
released when the object is created and automatically reacquired when it goes out of
scope. This pattern is essential for multi-threaded applications where C++ code performs
heavy computation while Python threads handle other tasks like UI updates or network I/O.

.. code-block:: cpp

    #include <pybind11/pybind11.h>
    #include <thread>
    #include <chrono>

    namespace py = pybind11;

    // Slow operation that releases GIL
    void slow_operation(int seconds) {
        // Release GIL while doing CPU work
        py::gil_scoped_release release;

        // Simulate slow work
        std::this_thread::sleep_for(std::chrono::seconds(seconds));
    }

    // CPU-intensive work
    unsigned long fib_nogil(unsigned long n) {
        py::gil_scoped_release release;

        std::function<unsigned long(unsigned long)> fib_impl;
        fib_impl = [&](unsigned long n) -> unsigned long {
            if (n < 2) return n;
            return fib_impl(n - 1) + fib_impl(n - 2);
        };
        return fib_impl(n);
    }

    PYBIND11_MODULE(gil_example, m) {
        m.def("slow_operation", &slow_operation);
        m.def("fib_nogil", &fib_nogil);
    }

.. code-block:: python

    import threading
    from datetime import datetime
    from gil_example import slow_operation

    def worker(n):
        print(f"{datetime.now()}: Thread {n} starting")
        slow_operation(1)
        print(f"{datetime.now()}: Thread {n} done")

    # Threads run in parallel because GIL is released
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
    for t in threads: t.start()
    for t in threads: t.join()

ctypes: Quick C Library Access
------------------------------

:Source: `src/cext/fib.c <https://github.com/crazyguitar/pysheeet/blob/master/src/cext/fib.c>`_

ctypes is Python's built-in foreign function interface (FFI) that lets you call C
functions from shared libraries (.so, .dylib, .dll) without writing any C wrapper code
or compiling Python extensions. It's ideal for quick prototyping, accessing system
libraries, or wrapping existing C code when you don't want a build step. The key
requirement is declaring function signatures with ``argtypes`` and ``restype``—without
these declarations, ctypes assumes all arguments and return values are C ``int``, which
causes silent bugs or crashes with other types like ``double`` or pointers.

.. code-block:: c

    // fib.c - Compile: gcc -shared -fPIC -o libfib.so fib.c
    unsigned long fib(unsigned long n) {
        if (n < 2) return n;
        return fib(n - 1) + fib(n - 2);
    }

    double add_doubles(double a, double b) {
        return a + b;
    }

.. code-block:: python

    import ctypes
    from ctypes import c_ulong, c_double

    # Load shared library
    # Linux: libfib.so, macOS: libfib.dylib, Windows: fib.dll
    lib = ctypes.CDLL("./libfib.so")

    # Declare function signatures (important for non-int types!)
    lib.fib.argtypes = [c_ulong]
    lib.fib.restype = c_ulong

    lib.add_doubles.argtypes = [c_double, c_double]
    lib.add_doubles.restype = c_double

    # Call functions
    print(lib.fib(35))        # 9227465
    print(lib.add_doubles(1.5, 2.5))  # 4.0

ctypes: Structures and Pointers
-------------------------------

Working with C structures and pointers in ctypes requires careful type declarations
that mirror the C memory layout exactly. Define structures by subclassing ``Structure``
and specifying ``_fields_`` as a list of (name, type) tuples in the same order as the
C struct. Use ``POINTER(Type)`` to create pointer types and ``byref(obj)`` to pass
objects by reference (equivalent to ``&obj`` in C). This approach is more error-prone
than pybind11 but works without any compilation step.

.. code-block:: c

    // point.c
    typedef struct {
        double x;
        double y;
    } Point;

    double distance(Point* p1, Point* p2) {
        double dx = p2->x - p1->x;
        double dy = p2->y - p1->y;
        return sqrt(dx*dx + dy*dy);
    }

    void scale_point(Point* p, double factor) {
        p->x *= factor;
        p->y *= factor;
    }

.. code-block:: python

    import ctypes
    from ctypes import Structure, c_double, POINTER, byref
    import math

    class Point(Structure):
        _fields_ = [("x", c_double), ("y", c_double)]

    lib = ctypes.CDLL("./libpoint.so")

    lib.distance.argtypes = [POINTER(Point), POINTER(Point)]
    lib.distance.restype = c_double

    lib.scale_point.argtypes = [POINTER(Point), c_double]
    lib.scale_point.restype = None

    # Create points
    p1 = Point(0, 0)
    p2 = Point(3, 4)

    # Pass by reference
    dist = lib.distance(byref(p1), byref(p2))
    print(f"Distance: {dist}")  # 5.0

    # Modify in place
    lib.scale_point(byref(p2), 2.0)
    print(f"Scaled: ({p2.x}, {p2.y})")  # (6.0, 8.0)

cffi: Cleaner Foreign Function Interface
----------------------------------------

cffi (C Foreign Function Interface) provides a cleaner, more Pythonic API than ctypes
for calling C code. Instead of Python type objects, you declare C function signatures
using actual C syntax in ``ffi.cdef()``, which can often be copied directly from header
files. cffi handles type conversions automatically and provides better error messages.
It's also the recommended FFI for PyPy, where it runs significantly faster than ctypes.
Install with ``pip install cffi``.

.. code-block:: python

    from cffi import FFI

    ffi = FFI()

    # Declare C functions (copy from header file)
    ffi.cdef("""
        unsigned long fib(unsigned long n);
        double add_doubles(double a, double b);
    """)

    # Load library
    lib = ffi.dlopen("./libfib.so")

    # Call functions - types are automatic!
    print(lib.fib(35))              # 9227465
    print(lib.add_doubles(1.5, 2.5))  # 4.0

**cffi with inline C code (ABI mode):**

.. code-block:: python

    from cffi import FFI

    ffi = FFI()
    ffi.cdef("unsigned long fib(unsigned long n);")

    # Compile C code inline
    ffi.set_source("_fib_cffi", """
        unsigned long fib(unsigned long n) {
            if (n < 2) return n;
            return fib(n - 1) + fib(n - 2);
        }
    """)

    ffi.compile()

    # Now import and use
    from _fib_cffi import lib
    print(lib.fib(35))

Cython: Python-like Syntax
--------------------------

Cython is a programming language that combines Python syntax with C data types,
compiling to efficient C code. It's excellent for gradual optimization: start with
pure Python code, then add type declarations to critical sections for dramatic speedups.
Cython supports three levels of optimization: pure Python (``def``), typed Python
(``def`` with type hints), and pure C functions (``cdef``). The ``cdef`` functions
run at C speed but can only be called from other Cython code, so you typically wrap
them with a ``def`` function for Python access. Install with ``pip install cython``.

.. code-block:: cython

    # fib.pyx
    def fib_py(n):
        """Pure Python - slow"""
        if n < 2:
            return n
        return fib_py(n - 1) + fib_py(n - 2)

    def fib_typed(long n):
        """With type hints - faster"""
        if n < 2:
            return n
        return fib_typed(n - 1) + fib_typed(n - 2)

    cdef unsigned long _fib_c(unsigned long n):
        """C function - fastest"""
        if n < 2:
            return n
        return _fib_c(n - 1) + _fib_c(n - 2)

    def fib_c(unsigned long n):
        """Python wrapper for C function"""
        return _fib_c(n)

.. code-block:: python

    # setup.py
    from setuptools import setup
    from Cython.Build import cythonize

    setup(
        ext_modules=cythonize("fib.pyx"),
    )

.. code-block:: bash

    $ python setup.py build_ext --inplace
    $ python -c "from fib import fib_c; print(fib_c(35))"
    9227465

Performance Comparison
----------------------

Understanding the performance characteristics of each approach helps you choose the
right tool. This benchmark compares all approaches using recursive Fibonacci (n=35),
a CPU-bound task that highlights the overhead of Python's interpreter. Native code
achieves 50-100x speedups by eliminating Python object creation, method dispatch, and
bytecode interpretation. The actual speedup varies by workload—numerical code with
NumPy integration can see even larger gains, while I/O-bound code benefits less.

.. code-block:: python

    from time import time

    def benchmark(func, n=35, runs=3):
        times = []
        for _ in range(runs):
            start = time()
            result = func(n)
            times.append(time() - start)
        return min(times), result

    # Pure Python
    def fib_python(n):
        if n < 2: return n
        return fib_python(n - 1) + fib_python(n - 2)

    # Results (approximate, varies by system):
    #
    # | Approach          | Time (s) | Speedup |
    # |-------------------|----------|---------|
    # | Pure Python       | 2.50     | 1x      |
    # | Cython (typed)    | 0.08     | 31x     |
    # | Cython (cdef)     | 0.05     | 50x     |
    # | ctypes            | 0.05     | 50x     |
    # | cffi              | 0.05     | 50x     |
    # | pybind11          | 0.04     | 62x     |
    # | pybind11 (no GIL) | 0.04     | 62x     |

Best Practices
--------------

Following these guidelines will help you write efficient, maintainable, and safe
native extensions. The most common mistakes are holding the GIL during long operations
(blocking other threads), copying large arrays unnecessarily (killing performance),
and ignoring error handling (causing crashes instead of Python exceptions).

**Do:**

- Use pybind11 for new C++ bindings
- Release the GIL for CPU-intensive operations
- Use NumPy arrays for numerical data (zero-copy with pybind11)
- Declare types in ctypes/cffi (avoid silent bugs)
- Profile before optimizing—find the real bottleneck

**Don't:**

- Write Python C API code for new projects (use pybind11)
- Hold the GIL during blocking I/O or long computations
- Copy large arrays between Python and C (use views)
- Ignore error handling in C code
- Optimize prematurely—Python is often fast enough

**Error handling:**

.. code-block:: cpp

    // pybind11 - exceptions automatically convert to Python
    double divide(double a, double b) {
        if (b == 0) {
            throw std::runtime_error("Division by zero");
        }
        return a / b;
    }

    // In Python: raises RuntimeError

**Memory management:**

.. code-block:: cpp

    // pybind11 handles Python object refcounting automatically
    // For raw pointers, use return value policies:

    py::class_<Parent>(m, "Parent")
        .def("get_child", &Parent::get_child,
             py::return_value_policy::reference_internal);  // Child tied to Parent lifetime
