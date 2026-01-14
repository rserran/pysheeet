.. meta::
    :description lang=en: Python C/C++ extension tutorial covering pybind11, ctypes, cffi, Cython, and the Python C API for high-performance native code
    :keywords: Python, Python3, pybind11, ctypes, cffi, Cython, C extension, C API, native code, performance, NumPy, shared library

Extension
=========

Python's flexibility comes at a performance cost. When you need speed for
numerical computing, system interfaces, or wrapping existing C/C++ libraries,
native extensions bridge the gap. This section covers multiple approaches:

- **ctypes** - Standard library FFI for calling C functions without compilation
- **Python C API** - Traditional approach with maximum control (legacy)
- **pybind11** (recommended for C++) - Clean C++11 syntax with automatic type
  conversions, used by PyTorch, TensorFlow, and SciPy
- **cffi** - Cleaner alternative to ctypes with PyPy compatibility
- **Cython** - Python-like syntax that compiles to C for gradual optimization

For most new projects wrapping C++ code, pybind11 is the recommended choice.
For calling existing C libraries without a build step, use ctypes or cffi.

.. toctree::
   :maxdepth: 1

   python-ctypes
   python-capi
   python-cext-modern
