# Step 5: IAT interrupt and polled DMA — solution

## Goal and source boundary

Read pci_device_read_irq, InterruptAttachThread and InterruptWait in the probe. Clear stale status (ack 0x64), attach with TRK_MSK, arm a two-second TimerTimeout, raise bit 1 at 0x60, verify own pending bit at 0x24 and acknowledge before detach. Default attach initially unmasks: an extra unmask at count zero returns EAGAIN. Then inspect edu_dma_roundtrip: contiguous uncached MAP_PHYS memory, mem_offset physical range inside 32-bit dma_mask, checked bus mastering, two bounded 64-byte transfers and byte comparison. QEMU device buffer starts at 0x40000; never substitute a virtual pointer for the physical bus address. DMA completion is POLLED, not an IRQ claim. On failed quiescence the reference retains the allocation until the bounded external VM owner stops it.

main.c is a readable original C snapshot mechanically derived from verified E1 native source. Steps1–4 stop after their own boundary and unwind; step5 runs the probe plus polled DMA; step6 is the actual IAT resource manager. No SDK declarations are copied. Snapshot compilation itself is not newly verified by this host-only E2 work.

## Compile contract

From repository root in an authorized initialized SDP environment, use qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -Werror -o "$EDU_OUT/step5-solution" steps/step5/solution/main.c -lpci. EDU_OUT must be an existing absolute directory outside the checkout. The starter may report expected unused scaffolding warnings until completed. See [build order](../../../docs/e2-build-order.md) before running anything.

## Required acceptance evidence

Reference expected marker: EDU STEP5 PASS IAT wait acknowledge. Also require the 64-byte byte-exact polled DMA marker. Record target identity, source hashes, image checksum, errors and full transcript. Historical E1 artifacts document reference observations, not a new learner run.

## Gate

Host: make check-step5 checks that all teaching snapshots still derive from native source, then requests a fresh accumulated E1 reference run. Missing external bundle or lease is BLOCKED (exit 2). The manifest binds native source and image; saved fixtures never satisfy this gate. An edited learner source is intentionally refused by the reference checker: rebuild and separately validate your own target image instead of presenting reference acceptance as yours. No helper here creates a learner IFS or installs SDK files.

[Return to codelab](../../../codelab/codelab.md).
