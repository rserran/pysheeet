# pybind11 C++ Extension Examples

This directory contains C++ source files demonstrating pybind11 bindings.

## Prerequisites

```bash
pip install pybind11 numpy
```

## Building with CMake

```bash
mkdir build && cd build
cmake ..
make
```

The compiled modules will be in the `build/` directory.

## Building with setup.py (Alternative)

```bash
pip install .
```

## Examples

### example.cpp
Basic function bindings (add, fibonacci).

```python
>>> import example
>>> example.add(1, 2)
3
>>> example.fib(10)
55
```

### vector.cpp
Class binding with operators and properties.

```python
>>> from vector import Vector2D
>>> v = Vector2D(3, 4)
>>> v.length()
5.0
>>> v2 = v + Vector2D(1, 1)
>>> v2
Vector2D(4.0, 5.0)
```

### numpy_example.cpp
NumPy array operations (zero-copy).

```python
>>> import numpy as np
>>> from numpy_example import multiply_inplace
>>> arr = np.array([1.0, 2.0, 3.0])
>>> multiply_inplace(arr, 2.0)
>>> arr
array([2., 4., 6.])
```

### gil_example.cpp
GIL release for parallel execution.

```python
>>> from gil_example import fib_nogil
>>> import threading
>>> # Runs in parallel because GIL is released
>>> threads = [threading.Thread(target=fib_nogil, args=(30,)) for _ in range(4)]
```

### fib.c
Pure C library for ctypes/cffi examples.

```bash
# Compile
gcc -shared -fPIC -o libfib.so fib.c      # Linux
clang -shared -fPIC -o libfib.dylib fib.c # macOS
```

```python
>>> import ctypes
>>> lib = ctypes.CDLL("./libfib.so")
>>> lib.fib(10)
55
```
