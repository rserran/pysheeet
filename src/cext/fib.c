/**
 * fib.c - Pure C library for ctypes/cffi examples
 *
 * Compile:
 *   gcc -shared -fPIC -o libfib.so fib.c      # Linux
 *   clang -shared -fPIC -o libfib.dylib fib.c # macOS
 *
 * Usage with ctypes:
 *   >>> import ctypes
 *   >>> lib = ctypes.CDLL("./libfib.so")
 *   >>> lib.fib.argtypes = [ctypes.c_ulong]
 *   >>> lib.fib.restype = ctypes.c_ulong
 *   >>> lib.fib(10)
 *   55
 *
 * Usage with cffi:
 *   >>> from cffi import FFI
 *   >>> ffi = FFI()
 *   >>> ffi.cdef("unsigned long fib(unsigned long n);")
 *   >>> lib = ffi.dlopen("./libfib.so")
 *   >>> lib.fib(10)
 *   55
 */

unsigned long fib(unsigned long n) {
  if (n < 2) return n;
  return fib(n - 1) + fib(n - 2);
}

unsigned long fib_iter(unsigned long n) {
  if (n < 2) return n;
  unsigned long a = 0, b = 1;
  for (unsigned long i = 1; i < n; ++i) {
    unsigned long tmp = a + b;
    a = b;
    b = tmp;
  }
  return b;
}

int add(int a, int b) { return a + b; }

double multiply(double a, double b) { return a * b; }

/* Structure example */
typedef struct {
  double x;
  double y;
} Point;

double point_distance(Point* p1, Point* p2) {
  double dx = p2->x - p1->x;
  double dy = p2->y - p1->y;
  return dx * dx + dy * dy; /* Returns squared distance */
}

void point_scale(Point* p, double factor) {
  p->x *= factor;
  p->y *= factor;
}
