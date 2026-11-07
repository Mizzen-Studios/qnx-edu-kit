# Step 1: solution specification

Original C source entry main.c now exists. The solution shares the checked native implementation; fresh target acceptance and QSTI provenance are separate gates.

## Goal

Establish reproducible host and evidence boundaries.

## Inputs and work

- Record host architecture, Python, make and QEMU version. ARM64 TCG is approved; KVM is not required.
- Keep SDKs, images and binaries outside the checkout, even ignored folders. Record authorized SDP build, QSTI version and image provenance when available.

## Required acceptance evidence

A clean clone runs host checks without third-party Python packages; full verification remains blocked.

## Gate

Host: make check-step1 launches a fresh source/image-bound accumulated target run when the external bundle and exclusive lease are supplied. Without them it remains BLOCKED (exit 2). Preserve raw target transcript, versions, source revision and errors. Host-model results do not replace this gate.

[Return to codelab](../../../codelab/codelab.md).

## Source entry

main.c is the original accumulated solution entry; steps1–5 share native/edu_probe.c and step6 shares native/edu_resmgr.c. The separate target client validates the shell and error/read/write cases. No host model substitutes for target execution.
