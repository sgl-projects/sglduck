#include "sgl_error.h"
#define exit(status) sgl_error("Fatal scanner error (exit code %d)", status)
#undef stdout
#undef stderr
#define stdout NULL
#define stderr NULL
