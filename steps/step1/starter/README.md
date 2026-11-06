# Step 1: starter specification

Task only, not compilable source.

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

main.c deliberately returns2 until the learner implements the documented contract. Compare the original solution only after attempting the exercise.
