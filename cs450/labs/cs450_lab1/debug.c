#include "debug.h"
#include <stdarg.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void
debug_panic (const char *file, int line, const char *function,
             const char *message, ...)
{
  printf ("Kernel PANIC at %s:%d in %s(): ", file, line, function);
  exit(1);
}
