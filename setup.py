"""Build configuration for the compiled SGL parser/bridge extension.

The package metadata lives in ``pyproject.toml``; this file exists only to
declare the ``sglduck._sgl`` C/C++ extension. We compile a fixed set of committed
C sources (the bison/flex output is checked into version control), so there is
no cmake and no code generation at build or install time.
"""

import sys

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup


class BuildExt(build_ext):
    """build_ext that keeps C++-only flags off the C sources.

    Pybind11Extension applies the C++ standard flag (``-std=c++17``) to every
    source in the extension, but clang rejects ``-std=c++17`` when compiling a
    ``.c`` file as C. We compile a mix of committed C sources and two C++ files
    (the bridge + the error shim) in one extension, so strip any ``-std=`` flag
    when the source being compiled is C.
    """

    def build_extensions(self):
        original_compile = self.compiler._compile

        def patched_compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
            if src.endswith(".c"):
                extra_postargs = [a for a in extra_postargs if not a.startswith("-std=")]
            return original_compile(obj, src, ext, cc_args, extra_postargs, pp_opts)

        self.compiler._compile = patched_compile
        try:
            super().build_extensions()
        finally:
            self.compiler._compile = original_compile

_SGL_SOURCES = [
    "src/_sgl/sgl_to_pgs.cpp",   # pybind11 bridge
    "src/_sgl/sgl_error.cpp",    # sgl_error() fatal-error shim (C++: throws)
    "src/_sgl/parser.tab.c",     # committed bison output
    "src/_sgl/scanner.c",        # committed flex output
    "src/_sgl/aes.c",
    "src/_sgl/geom.c",
    "src/_sgl/cta.c",
    "src/_sgl/qual.c",
    "src/_sgl/scale.c",
    "src/_sgl/keyword.c",
    "src/_sgl/title.c",
    "src/_sgl/case.c",
    "src/_sgl/cgs_order.c",
]

# sgl_error() throws a C++ exception that must unwind through the C parser
# frames (sgl_to_cgs / yyparse) to reach the bridge. -fexceptions makes that
# unwinding well-defined for the C sources on GCC/Clang. (MSVC enables C++
# exception unwinding through extern "C" by default.)
_extra_compile_args = [] if sys.platform == "win32" else ["-fexceptions"]

ext_modules = [
    Pybind11Extension(
        "sglduck._sgl",
        sources=_SGL_SOURCES,
        include_dirs=["src/_sgl"],
        extra_compile_args=_extra_compile_args,
    )
]

setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": BuildExt},
)
