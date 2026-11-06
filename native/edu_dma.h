/* Original QNX/QEMU-only diagnostic; no SDK implementation is included.
 * This assumes the tested x86 PC guest with no IOMMU and dma_mask=0xffffffff.
 * It is NOT a portable hardware DMA allocator or a production driver. */
#ifndef EDU_DMA_H
#define EDU_DMA_H
static int edu_dma_roundtrip(pci_devhdl_t h, pci_bdf_t bdf, volatile uint32_t *r) {
    const size_t allocation=4096, count=64;
    unsigned char *memory=MAP_FAILED;
    off_t physical=0;
    size_t contiguous=0;
    pci_cmd_t original=0, current=0;
    int restore_command=0, result=1;
    volatile uint64_t *src=(volatile uint64_t *)((volatile char *)r+0x80);
    volatile uint64_t *dst=(volatile uint64_t *)((volatile char *)r+0x88);
    volatile uint64_t *len=(volatile uint64_t *)((volatile char *)r+0x90);
    volatile uint64_t *cmd=(volatile uint64_t *)((volatile char *)r+0x98);
    if (pci_device_read_cmd(bdf,&original)!=PCI_ERR_OK) return 1;
    memory=mmap(NULL,allocation,PROT_READ|PROT_WRITE|PROT_NOCACHE,
                MAP_PRIVATE|MAP_ANON|MAP_PHYS,NOFD,0);
    if (memory==MAP_FAILED) { perror("DMA mmap contiguous"); return 1; }
    if (mem_offset(memory,NOFD,allocation,&physical,&contiguous)<0) {
        perror("DMA mem_offset"); goto done;
    }
    if (physical<0 || contiguous<allocation || (uint64_t)physical>UINT32_MAX-(allocation-1)) {
        fputs("DMA physical range/contiguity rejected\n",stderr); goto done;
    }
    printf("EDU DMA physical=%llx contiguous=%zu count=%zu\n",
           (unsigned long long)physical,contiguous,count);
    for (size_t i=0;i<count;i++) memory[i]=(unsigned char)(i*7+3);
    memset(memory+128,0,count);
    restore_command=1;
    if (pci_device_write_cmd(h,original|4,&current)!=PCI_ERR_OK || !(current&4)) {
        fputs("DMA bus master enable failed\n",stderr); goto done;
    }
    for (int phase=0;phase<2;phase++) {
        if (*cmd&1) { fputs("DMA unexpectedly busy\n",stderr); goto done; }
        *src=phase?0x40000:(uint64_t)physical;
        *dst=phase?(uint64_t)physical+128:0x40000;
        *len=count;
        __sync_synchronize();
        *cmd=phase?3:1;
        for (int wait=0;(*cmd&1) && wait<2000;wait++) usleep(1000);
        if (*cmd&1) { fputs("DMA completion timeout\n",stderr); goto done; }
        __sync_synchronize();
        printf("EDU DMA phase=%d completed\n",phase);
    }
    if (memcmp(memory,memory+128,count)) { fputs("DMA byte mismatch\n",stderr); goto done; }
    puts("EDU DMA 64-byte RAM->EDU->RAM byte-exact PASS (polled, no DMA IRQ claim)");
    result=0;
done:
    /* In the tested QEMU PCI model, disabling bus mastering blocks future
     * DMA address-space transactions. Verify it before releasing the buffer.
     * Physical hardware needs a stronger device-specific quiescence contract. */
    if (restore_command) {
        if (pci_device_write_cmd(h,original&~4,&current)!=PCI_ERR_OK || (current&4)) {
            fputs("DMA CANNOT QUIESCE: retain buffer until this isolated VM is stopped\n",stderr);
            /* Fail closed without freeing a potentially live DMA allocation.
             * The external capped, bounded VM harness is the recovery owner. */
            for (;;) pause();
        }
    }
    munmap(memory,allocation);
    if (restore_command && pci_device_write_cmd(h,original,NULL)!=PCI_ERR_OK) result=1;
    return result;
}
#endif
