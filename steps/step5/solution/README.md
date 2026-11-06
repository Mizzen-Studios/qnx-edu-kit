# Step 5: solution specification

Original C source entry main.c now exists. The solution shares the checked native implementation; fresh target acceptance and QSTI provenance are separate gates.

## Goal

Teach standalone interrupt ownership rather than io-sock assumptions.

## Inputs and work

- Review actual InterruptAttachThread and InterruptWait declarations locally; no guessed signatures are supplied. Inspect IO and INTERRUPT abilities and active policy before attach.
- On EPERM capture the failing operation and inspect grants; do not recommend broad privilege. For INTx inspect owned status, acknowledge device sources, then follow documented unmask rules. InterruptAttachEvent is contextual for io-sock, not an interchangeable standalone sample.

## Required acceptance evidence

Test shared/unrelated IRQ, stale status, timeout, missing ability and repeated attach/detach. Delivery alone does not establish completion.

## Gate

Host: make check-step5 launches a fresh source/image-bound accumulated target run when the external bundle and exclusive lease are supplied. Without them it remains BLOCKED (exit 2). Preserve raw target transcript, versions, source revision and errors. Host-model results do not replace this gate.

[Return to codelab](../../../codelab/codelab.md).

## Source entry

main.c is the original accumulated solution entry; steps1–5 share native/edu_probe.c and step6 shares native/edu_resmgr.c. The separate target client validates the shell and error/read/write cases. No host model substitutes for target execution.
