# Step 2: solution specification

Original C source entry main.c now exists. The solution shares the checked native implementation; fresh target acceptance and QSTI provenance are separate gates.

## Goal

Separate discovery from exclusive resource ownership.

## Inputs and work

- Review installed QNX 8.0 PCI server declarations. The discontinued legacy PCI API is not the porting target.
- Validate device identity, BAR type and extent, interrupt route and ownership. Unwind partial acquisition in reverse order; never continue with an invalid handle.

## Required acceptance evidence

Missing device, duplicate owner and injected attach failures return nonzero without leaked resources.

## Gate

Host: make check-step2 launches a fresh source/image-bound accumulated target run when the external bundle and exclusive lease are supplied. Without them it remains BLOCKED (exit 2). Preserve raw target transcript, versions, source revision and errors. Host-model results do not replace this gate.

[Return to codelab](../../../codelab/codelab.md).

## Source entry

main.c is the original accumulated solution entry; steps1–5 share native/edu_probe.c and step6 shares native/edu_resmgr.c. The separate target client validates the shell and error/read/write cases. No host model substitutes for target execution.
