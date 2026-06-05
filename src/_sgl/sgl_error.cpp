#include "sgl_error.h"

#include <cstdarg>
#include <cstdio>
#include <stdexcept>
#include <string>

/*
 * Compiled as C++ so the throw propagates through pybind11, which translates
 * std::runtime_error into a Python RuntimeError. The declaration in sgl_error.h is
 * wrapped in extern "C" so the ported C sources (parser.tab.c, keyword.c, the
 * generated scanner.c) link against it with C calling convention.
 */
extern "C" void sgl_error(const char *fmt, ...) {
	char buffer[1024];
	va_list args;
	va_start(args, fmt);
	std::vsnprintf(buffer, sizeof(buffer), fmt, args);
	va_end(args);

	throw std::runtime_error(std::string(buffer));
}
