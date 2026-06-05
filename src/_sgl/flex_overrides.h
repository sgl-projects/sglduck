#include "panic.h"
#define exit(status) sgl_panic("Fatal scanner error (exit code %d)", status)
#undef stdout
#undef stderr
#define stdout NULL
#define stderr NULL
