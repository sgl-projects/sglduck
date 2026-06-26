/* Windows/MSVC build-compatibility shims.
 *
 * The committed flex/bison sources target a POSIX toolchain — as in rsgl, which
 * builds on Windows with the GCC-based Rtools, where unistd.h and the GNU
 * asprintf are available. Python extensions build with MSVC instead, which has
 * neither. This header is force-included on Windows builds only (setup.py /FI),
 * so the committed parser/scanner sources stay byte-for-byte in step with rsgl.
 */
#ifndef SGL_WIN_COMPAT_H
#define SGL_WIN_COMPAT_H

#if defined(_MSC_VER)

#include <io.h>      /* isatty / fileno: the flex scanner calls them, and the */
                     /* unistd.h that would declare them is skipped on MSVC.  */
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

/* MSVC has no POSIX/GNU asprintf; the parser uses it to allocate and format its
 * error-message strings. Allocate exactly the needed length (via _vscprintf)
 * and format into it, matching asprintf's contract: on success *strp owns a
 * malloc'd string and the byte count is returned; on failure *strp is NULL and
 * -1 is returned. */
static int asprintf(char **strp, const char *fmt, ...)
{
    va_list ap;
    int len;
    char *buf;

    va_start(ap, fmt);
    len = _vscprintf(fmt, ap);
    va_end(ap);
    if (len < 0) {
        *strp = NULL;
        return -1;
    }

    buf = (char *)malloc((size_t)len + 1);
    if (buf == NULL) {
        *strp = NULL;
        return -1;
    }

    va_start(ap, fmt);
    len = vsnprintf(buf, (size_t)len + 1, fmt, ap);
    va_end(ap);
    if (len < 0) {
        free(buf);
        *strp = NULL;
        return -1;
    }

    *strp = buf;
    return len;
}

#endif /* _MSC_VER */

#endif /* SGL_WIN_COMPAT_H */
