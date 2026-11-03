# Step 1: solution specification

Acceptance specification ONLY; no implemented target source or fabricated API stubs.

## Goal

Establish reproducible host and evidence boundaries.

## Inputs and work

- Record host architecture, Python, make and QEMU version. ARM64 TCG is approved; KVM is not required.
- Keep SDKs, images and binaries outside the checkout, even ignored folders. Record authorized SDP build, QSTI version and image provenance when available.

## Required acceptance evidence

A clean clone runs host checks without third-party Python packages; full verification remains blocked.

## Gate

Host: make check-step1 remains BLOCKED (script exit 2). Preserve raw target transcript, versions, source revision and errors. Host-model results do not replace this gate.

[Return to codelab](../../../codelab/codelab.md).
