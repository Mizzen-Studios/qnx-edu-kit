/* Step 1: readable E1-derived snapshot; regenerate with tools/step_sources.py. */
/* Original application code; no SDK implementation or headers vendored. */
#include <pci/pci.h>
#include <sys/utsname.h>
#include <sys/mman.h>
#include <sys/neutrino.h>
#include <sys/siginfo.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <errno.h>
#include <signal.h>
#include <dlfcn.h>
#include <string.h>

int main(void) {
    struct utsname target;
    if (uname(&target)<0 || strcmp(target.sysname,"QNX")!=0) return 1;
    printf("EDU TARGET %s %s %s\n",target.sysname,target.release,target.machine);
    setvbuf(stdout,NULL,_IONBF,0); puts("EDU PROBE BEGIN"); puts("EDU STEP1 PASS QNX target process");
    return 0;
}
