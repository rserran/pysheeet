/* Demonstrate GIL release and acquire in Python C API. */
#include <Python.h>

#ifdef _WIN32
#include <windows.h>
#define sleep(x) Sleep((x) * 1000)
#else
#include <unistd.h>
#endif

/* Sleep WITHOUT releasing GIL - blocks other threads */
static PyObject* sleep_with_gil(PyObject* self, PyObject* args) {
  int seconds;
  if (!PyArg_ParseTuple(args, "i", &seconds)) {
    return NULL;
  }
  sleep(seconds);
  Py_RETURN_NONE;
}

/* Sleep WITH releasing GIL - allows other threads to run */
static PyObject* sleep_no_gil(PyObject* self, PyObject* args) {
  int seconds;
  if (!PyArg_ParseTuple(args, "i", &seconds)) {
    return NULL;
  }

  Py_BEGIN_ALLOW_THREADS sleep(seconds);
  Py_END_ALLOW_THREADS

      Py_RETURN_NONE;
}

/* CPU work without GIL */
static unsigned long fib_impl(unsigned long n) {
  if (n < 2) return n;
  return fib_impl(n - 1) + fib_impl(n - 2);
}

static PyObject* fib_no_gil(PyObject* self, PyObject* args) {
  unsigned long n, result;
  if (!PyArg_ParseTuple(args, "k", &n)) {
    return NULL;
  }

  Py_BEGIN_ALLOW_THREADS result = fib_impl(n);
  Py_END_ALLOW_THREADS

      return PyLong_FromUnsignedLong(result);
}

static PyMethodDef methods[] = {
    {"sleep_with_gil", (PyCFunction)sleep_with_gil, METH_VARARGS, "Sleep holding GIL (blocks threads)"},
    {"sleep_no_gil", (PyCFunction)sleep_no_gil, METH_VARARGS, "Sleep releasing GIL (allows threads)"},
    {"fib_no_gil", (PyCFunction)fib_no_gil, METH_VARARGS, "Fibonacci with GIL released"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {PyModuleDef_HEAD_INIT, "gil", "GIL handling examples", -1, methods};

PyMODINIT_FUNC PyInit_gil(void) { return PyModule_Create(&module); }
