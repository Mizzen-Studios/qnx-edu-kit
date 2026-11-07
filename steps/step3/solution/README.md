# Step 3: BAR mapping and liveness — solution

## Goal and source boundary

Read pci_device_read_ba and the BAR0 loop. Require a memory BAR, sufficient extent, and a valid mmap_device_memory result before MMIO. The verified reference maps 0x1000 bytes; the probe checks a smaller minimum extent whereas the resource manager requires the full mapping extent. Do not generalize that probe precondition to arbitrary hardware. At byte offsets 0x00 and 0x04, require ID 0x010000ed and the 32-bit complement of 0x12345678. Unmap and detach on every acquired-resource failure.

main.c is a readable original C snapshot mechanically derived from verified E1 native source. Steps1–4 stop after their own boundary and unwind; step5 runs the probe plus polled DMA; step6 is the actual IAT resource manager. No SDK declarations are copied. Snapshot compilation itself is not newly verified by this host-only E2 work.

## Compile contract

From repository root in an authorized initialized SDP environment, use qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -Werror -o "$EDU_OUT/step3-solution" steps/step3/solution/main.c -lpci. EDU_OUT must be an existing absolute directory outside the checkout. The starter may report expected unused scaffolding warnings until completed. See [build order](../../../docs/e2-build-order.md) before running anything.

## Required acceptance evidence

Reference expected marker: EDU STEP3 PASS BAR ID and complement. Earlier boundaries must complete without using later hardware operations. Record target identity, source hashes, image checksum, errors and full transcript. Historical E1 artifacts document reference observations, not a new learner run.

## Gate

Host: make check-step3 checks that all teaching snapshots still derive from native source, then requests a fresh accumulated E1 reference run. Missing external bundle or lease is BLOCKED (exit 2). The manifest binds native source and image; saved fixtures never satisfy this gate. An edited learner source is intentionally refused by the reference checker: rebuild and separately validate your own target image instead of presenting reference acceptance as yours. No helper here creates a learner IFS or installs SDK files.

[Return to codelab](../../../codelab/codelab.md).
