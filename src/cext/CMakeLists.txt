cmake_minimum_required(VERSION 3.15)
project(pysheeet_cext)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Find Python and pybind11
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 CONFIG QUIET)

# If pybind11 not found via CMake, try to find it via Python
if(NOT pybind11_FOUND)
    execute_process(
        COMMAND ${Python3_EXECUTABLE} -c "import pybind11; print(pybind11.get_cmake_dir())"
        OUTPUT_VARIABLE pybind11_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
        RESULT_VARIABLE pybind11_RESULT
    )
    if(pybind11_RESULT EQUAL 0)
        find_package(pybind11 CONFIG REQUIRED PATHS ${pybind11_DIR})
    else()
        message(FATAL_ERROR "pybind11 not found. Install with: pip install pybind11")
    endif()
endif()

# Example 1: Basic functions (add, fib)
pybind11_add_module(example example.cpp)

# Example 2: Vector2D class
pybind11_add_module(vector vector.cpp)

# Example 3: NumPy integration
pybind11_add_module(numpy_example numpy_example.cpp)

# Example 4: GIL release example
pybind11_add_module(gil_example gil_example.cpp)

# Pure C library (for ctypes/cffi examples)
add_library(fib SHARED fib.c)
set_target_properties(fib PROPERTIES PREFIX "lib")

# Installation
install(TARGETS example vector numpy_example gil_example fib
        LIBRARY DESTINATION .)
