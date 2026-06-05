#ifndef PANIC_H
#define PANIC_H

/*
 * Host-agnostic fatal-error shim.
 *
 * The ported C grammar sources (parser.y, keyword.c) and flex_overrides.h
 * originally called R's Rf_error() to abort on unrecoverable failures
 * (memory-allocation failures, unexpected tokens, a fatal scanner exit).
 * sgl_panic() replaces those call sites so the C layer carries no R
 * dependency. In pysgl, panic.c raises a C++ exception, which pybind11
 * translates into a Python exception.
 */

#ifdef __cplusplus
extern "C" {
#endif

void sgl_panic(const char *fmt, ...);

#ifdef __cplusplus
}
#endif

#endif
