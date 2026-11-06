# Native DMA diagnostic — experimental QNX/QEMU only

Original implementation: native/edu_dma.h, called by native/edu_probe.c only after the native BAR, factorial and one-shot IRQ checks succeed. Build with the same real SDP 8.0 qcc command documented in the tutorial; the header is original application code, not an SDK file.

## Fixed laboratory contract

- x86 PC QNX guest with no IOMMU, QEMU edu device explicitly configured dma_mask=0xffffffff, 512MiB guest RAM. Do not use the default 28-bit mask with this probe, or assume these mappings are portable to hardware.
- Allocate one 4096-byte uncached anonymous physical mapping using the installed QNX mmap API; verify physical offset, contiguous extent and complete 32-bit address range before enabling bus mastering. No virtual pointer is used as a DMA address.
- Preserve original PCI command, enable/check bus-master bit, and transfer exactly 64 known bytes RAM->EDU offset0x40000, then EDU->a separate offset128 in the same owned page.
- Each phase polls the start/busy bit for at most 2000 one-millisecond waits. Compiler/full barriers surround ownership transitions. Compare all 64 returned bytes; partial/mismatched results fail.
- This test uses polled DMA completion, NOT a DMA completion interrupt. Native manual interrupt raise/wait/ack is verified separately. DMA IRQ delivery remains an explicit pending gate.

## Cleanup boundary

Before releasing the physical allocation, disable PCI bus mastering and check the returned command. This blocks future DMA transactions in the tested QEMU PCI address-space model. After releasing the mapping, restore the original command. This is NOT proof of device-specific quiescence on physical hardware.

If bus mastering cannot be disabled/read back, the diagnostic deliberately retains the mapping and waits for the external VM supervisor rather than freeing a potentially live DMA buffer. The private native harness bounds its wait loop to180seconds, with additional bounded handshake/termination cleanup, and terminates the owned VM; it also caps CPU100%, host memory1GiB, nice15. Never run this diagnostic without an equivalent bounded VM supervisor. A quiescence failure is not success and is not a production-driver shutdown design.

Denied allocation/offset/ability, out-of-range memory, timeout, bus-master failure and mismatch are non-success paths. Error-path fault injection, DMA interrupt completion, restart/reprobe and least-privilege deny/allow remain unaccepted. No SDK, binaries or images are committed.
