/**
 * gil_example.cpp - GIL release example
 *
 * Demonstrates:
 *   - Releasing GIL for CPU-intensive work
 *   - Allowing Python threads to run in parallel
 *   - Re-acquiring GIL when needed
 *
 * Usage:
 *   >>> from gil_example import slow_operation, fib_nogil
 *   >>> import threading
 *   >>> # These run in parallel because GIL is released
 *   >>> threads = [threading.Thread(target=slow_operation, args=(1,)) for _ in range(3)]
 */
#include <pybind11/pybind11.h>

#include <chrono>
#include <functional>
#include <thread>

namespace py = pybind11;

// Slow operation that releases GIL
void slow_operation(int seconds) {
  // Release GIL while sleeping
  py::gil_scoped_release release;
  std::this_thread::sleep_for(std::chrono::seconds(seconds));
}

// CPU-intensive Fibonacci without GIL
unsigned long fib_nogil(unsigned long n) {
  // Release GIL for CPU work
  py::gil_scoped_release release;

  std::function<unsigned long(unsigned long)> fib_impl;
  fib_impl = [&](unsigned long n) -> unsigned long {
    if (n < 2) return n;
    return fib_impl(n - 1) + fib_impl(n - 2);
  };
  return fib_impl(n);
}

// Example showing GIL re-acquisition
void call_python_callback(py::function callback, const std::string& msg) {
  // Release GIL for some work
  {
    py::gil_scoped_release release;
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
  }
  // GIL automatically re-acquired here
  // Now safe to call Python
  callback(msg);
}

PYBIND11_MODULE(gil_example, m) {
  m.doc() = "GIL release examples for parallel execution";

  m.def("slow_operation", &slow_operation, "Sleep for N seconds (releases GIL)", py::arg("seconds"));

  m.def("fib_nogil", &fib_nogil, "Compute Fibonacci without holding GIL", py::arg("n"));

  m.def("call_python_callback", &call_python_callback, "Call Python function after releasing GIL", py::arg("callback"), py::arg("msg"));
}
