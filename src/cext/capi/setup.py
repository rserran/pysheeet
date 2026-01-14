from setuptools import setup, Extension

extensions = [
    Extension("simple", ["simple.c"]),
    Extension("args", ["args.c"]),
    Extension("gil", ["gil.c"]),
    Extension("errors", ["errors.c"]),
    Extension("types_demo", ["types_demo.c"]),
]

setup(
    name="capi_examples",
    version="1.0",
    ext_modules=extensions,
)
