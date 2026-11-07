/* Step 1: readable E1-derived snapshot; regenerate with tools/step_sources.py. */
#include <stdio.h>
#include <sys/utsname.h>
#include <string.h>
int main(void) {
    /* TODO: use uname, require QNX 8.0, print target identity.
     * Do not report acceptance until the actual target is checked. */
    fputs("BLOCKED: step1 target identity TODO\n",stderr);
    return 2;
}
