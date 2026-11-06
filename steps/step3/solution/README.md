# Step 3: solution specification

Original C source entry main.c now exists. The solution shares the checked native implementation; fresh target acceptance and QSTI provenance are separate gates.

## Goal

A mapped address is not proof of a device protocol.

## Inputs and work

- Register offsets and values remain withheld until every row has live pinned-QEMU evidence. Source inspection alone is insufficient.
- Validate width, alignment and bounds; check identity before writing. Test complementary liveness patterns and width-limited inverse readback. Unmap on failure.

## Required acceptance evidence

Wrong identity, failed mapping and out-of-bounds requests are bounded errors, never PASS.

## Gate

Host: make check-step3 launches a fresh source/image-bound accumulated target run when the external bundle and exclusive lease are supplied. Without them it remains BLOCKED (exit 2). Preserve raw target transcript, versions, source revision and errors. Host-model results do not replace this gate.

[Return to codelab](../../../codelab/codelab.md).

## Source entry

main.c is the original accumulated solution entry; steps1–5 share native/edu_probe.c and step6 shares native/edu_resmgr.c. The separate target client validates the shell and error/read/write cases. No host model substitutes for target execution.
