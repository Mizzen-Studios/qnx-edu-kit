/* Original application code; no SDK implementation or headers vendored. */
#include <pci/pci.h>
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

/* Diagnostic-only: no stdio, allocator or symbol lookup in the signal handler. */
static char *hex_value(char *out, uintptr_t value) {
    static const char digits[]="0123456789abcdef";
    *out++='0'; *out++='x';
    for (int shift=(int)(sizeof(value)*8)-4;shift>=0;shift-=4)
        *out++=digits[(value>>shift)&15];
    return out;
}
static void fault_report(int signo, siginfo_t *info, void *context) {
    (void)context;
    char buf[160], *p=buf;
    const char prefix[]="EDU FAULT signo/code/fltno/ip/addr ";
    for (size_t i=0;i<sizeof(prefix)-1;i++) *p++=prefix[i];
    p=hex_value(p,(uintptr_t)signo); *p++=' ';
    p=hex_value(p,(uintptr_t)info->si_code); *p++=' ';
    p=hex_value(p,(uintptr_t)info->si_fltno); *p++=' ';
    p=hex_value(p,(uintptr_t)info->si_fltip); *p++=' ';
    p=hex_value(p,(uintptr_t)info->si_addr); *p++='\n';
    (void)write(STDERR_FILENO,buf,(size_t)(p-buf));
    _exit(128+signo);
}
int main(void) {
    setvbuf(stdout,NULL,_IONBF,0); puts("EDU PROBE BEGIN");
    struct sigaction action={0};
    action.sa_sigaction=fault_report; action.sa_flags=SA_SIGINFO;
    sigemptyset(&action.sa_mask);
    if (sigaction(SIGSEGV,&action,NULL)<0 || sigaction(SIGBUS,&action,NULL)<0 ||
        sigaction(SIGILL,&action,NULL)<0) { perror("sigaction"); return 1; }
    Dl_info library;
    if (dladdr((void *)pci_device_read_ba,&library))
        printf("EDU LIBPCI base=%p file=%s read_ba=%p\n",library.dli_fbase,library.dli_fname,(void *)pci_device_read_ba);
    if (dladdr((void *)memcpy,&library))
        printf("EDU LIBC base=%p file=%s memcpy=%p\n",library.dli_fbase,library.dli_fname,(void *)memcpy);
    /* x86 PCI configuration access may execute port I/O in the HW module.
     * Request only this thread's level 1; do not enable inheritance or level 2. */
    if (ThreadCtl(_NTO_TCTL_IO_LEVEL,(void *)(uintptr_t)_NTO_IO_LEVEL_1)<0) {
        perror("ThreadCtl(IO_LEVEL_1)"); return 1;
    }
    puts("EDU IO_LEVEL_1 acquired");
    pci_err_t error=PCI_ERR_OK;
    pci_bdf_t bdf=pci_device_find(0,0x1234,0x11e8,PCI_CCODE_ANY);
    if (bdf==PCI_BDF_NONE) { fputs("EDU absent\n",stderr); return 1; }
    pci_devhdl_t h=pci_device_attach(bdf,pci_attachFlags_e_EXCLUSIVE,&error);
    if (h==NULL) { fprintf(stderr,"attach: %s\n",pci_strerror(error)); return 1; }
    puts("EDU PCI attached");
    pci_ba_t bars[6] = {0}; int_t n=6; int rc=1, iid=-1; pci_irq_t irq=-1;
    volatile uint32_t *r=MAP_FAILED;
    puts("EDU read_ba BEGIN");
    if ((error=pci_device_read_ba(h,&n,bars,pci_reqType_e_UNSPECIFIED))!=PCI_ERR_OK) goto done;
    puts("EDU read_ba END");
    if (n<0 || n>6) goto done;
    for (int i=0;i<n;i++) if (bars[i].bar_num==0 && bars[i].type==pci_asType_e_MEM && bars[i].size>=0x100) {
        r=mmap_device_memory(NULL,0x1000,PROT_READ|PROT_WRITE|PROT_NOCACHE,0,bars[i].addr);
        printf("EDU BAR0=%llx size=%llu\n",(unsigned long long)bars[i].addr,(unsigned long long)bars[i].size);
        break;
    }
    if (r==MAP_FAILED) { perror("mmap_device_memory"); goto done; }
    printf("EDU MAP=%p\n",(void*)r);
    printf("EDU ID=%08x\n",r[0]);
    if (r[0]!=0x010000ed) goto done;
    r[1]=0x12345678; if (r[1]!=0xedcba987) goto done;
    r[8]=0; r[2]=10;
    for (int i=0;(r[8]&1) && i<1000;i++) usleep(1000);
    if ((r[8]&1) || r[2]!=3628800) goto done;
    puts("EDU FACTORIAL 10=3628800 PASS");
    n=1; error=pci_device_read_irq(h,&n,&irq);
    if (error!=PCI_ERR_OK || n!=1 || irq<0) goto done;
    printf("EDU IRQ=%d\n",irq);
    struct sigevent event; SIGEV_INTR_INIT(&event);
    iid=InterruptAttachEvent(irq,&event,_NTO_INTR_FLAGS_TRK_MSK);
    if (iid<0) { perror("InterruptAttachEvent"); goto done; }
    if (InterruptUnmask(irq,iid)<0) { perror("InterruptUnmask"); goto done; }
    r[0x64/4]=0xffffffff;
    uint64_t timeout=2000000000ULL;
    if (TimerTimeout(CLOCK_MONOTONIC,_NTO_TIMEOUT_INTR,NULL,&timeout,NULL)<0) {
        perror("TimerTimeout(INTR)"); goto done;
    }
    r[0x60/4]=1;
    printf("EDU IRQ raised pending=%08x\n",r[0x24/4]);
    if (InterruptWait(0,NULL)<0) { perror("InterruptWait"); goto done; }
    printf("EDU IRQ woke pending=%08x\n",r[0x24/4]);
    if (!(r[0x24/4]&1)) { fputs("EDU IRQ wake without own pending bit\n",stderr); goto done; }
    r[0x64/4]=1;
    if (r[0x24/4]&1) { fputs("EDU IRQ ack failed\n",stderr); goto done; }
    puts("EDU IRQ raise/wait/ack PASS"); rc=0;
done:
    if (iid>=0) InterruptDetach(iid);
    if (r!=MAP_FAILED) { r[0x64/4]=0xffffffff; munmap((void*)r,0x1000); }
    pci_device_detach(h);
    if (ThreadCtl(_NTO_TCTL_IO_LEVEL,(void *)(uintptr_t)_NTO_IO_LEVEL_NONE)<0) {
        perror("ThreadCtl(IO_LEVEL_NONE)"); rc=1;
    }
    if (rc) fprintf(stderr,"EDU PROBE FAIL pci=%s errno=%d\n",pci_strerror(error),errno);
    return rc;
}
