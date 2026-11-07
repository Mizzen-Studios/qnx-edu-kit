# Step 2: PCI discovery and ownership — solution

## Goal and source boundary

Read main from ThreadCtl(IO_LEVEL_1) through pci_device_find and pci_device_attach. The tested x86 PCI module needs checked per-thread I/O level 1: no inherited level 2. Match vendor 0x1234/device 0x11e8; attach EXCLUSIVE and detach. Missing device or failed attach must stop, never dereference a bad handle.

main.c is a readable original C snapshot mechanically derived from verified E1 native source. Steps1–4 stop after their own boundary and unwind; step5 runs the probe plus polled DMA; step6 is the actual IAT resource manager. No SDK declarations are copied. Snapshot compilation itself is not newly verified by this host-only E2 work.

## Compile contract

From repository root in an authorized initialized SDP environment, use qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -Werror -o "$EDU_OUT/step2-solution" steps/step2/solution/main.c -lpci. EDU_OUT must be an existing absolute directory outside the checkout. The starter may report expected unused scaffolding warnings until completed. See [build order](../../../docs/e2-build-order.md) before running anything.

## Required acceptance evidence

Reference expected marker: EDU STEP2 PASS PCI server attach. Earlier boundaries must complete without using later hardware operations. Record target identity, source hashes, image checksum, errors and full transcript. Historical E1 artifacts document reference observations, not a new learner run.

## Gate

Host: make check-step2 checks that all teaching snapshots still derive from native source, then requests a fresh accumulated E1 reference run. Missing external bundle or lease is BLOCKED (exit 2). The manifest binds native source and image; saved fixtures never satisfy this gate. An edited learner source is intentionally refused by the reference checker: rebuild and separately validate your own target image instead of presenting reference acceptance as yours. No helper here creates a learner IFS or installs SDK files.

[Return to codelab](../../../codelab/codelab.md).
