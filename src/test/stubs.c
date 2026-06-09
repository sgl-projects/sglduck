#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>

#include "sgl_error.h"

/*
 * Test-only sgl_error(): print and abort. The real shim (sgl_error.cpp)
 * throws a C++ exception for pybind11 to translate, which cannot link into
 * this plain C test binary.
 */
void sgl_error(const char *fmt, ...) {
	va_list args;
	va_start(args, fmt);
	vfprintf(stderr, fmt, args);
	va_end(args);
	fprintf(stderr, "\n");
	abort();
}
