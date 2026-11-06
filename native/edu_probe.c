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

int main(void) {
    setvbuf(stdout,NULL,_IONBF,0); puts("EDU PROBE BEGIN");
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
    if (TimerTimeout(CLOCK_MONOTONIC,_NTO_TIMEOUT_INTR,NULL,&timeout,NULL)<0) goto done;
    r[0x60/4]=1;
    if (InterruptWait(0,NULL)<0) { perror("InterruptWait"); goto done; }
    if (!(r[0x24/4]&1)) goto done;
    r[0x64/4]=1;
    if (r[0x24/4]&1) goto done;
    puts("EDU IRQ raise/wait/ack PASS"); rc=0;
done:
    if (iid>=0) InterruptDetach(iid);
    if (r!=MAP_FAILED) { r[0x64/4]=0xffffffff; munmap((void*)r,0x1000); }
    pci_device_detach(h);
    if (rc) fprintf(stderr,"EDU PROBE FAIL pci=%s errno=%d\n",pci_strerror(error),errno);
    return rc;
}
