# Step 2: solution specification

Acceptance specification ONLY; no implemented target source or fabricated API stubs.

## Goal

Separate discovery from exclusive resource ownership.

## Inputs and work

- Review installed QNX 8.0 PCI server declarations. The discontinued legacy PCI API is not the porting target.
- Validate device identity, BAR type and extent, interrupt route and ownership. Unwind partial acquisition in reverse order; never continue with an invalid handle.

## Required acceptance evidence

Missing device, duplicate owner and injected attach failures return nonzero without leaked resources.

## Gate

Host: make check-step2 remains BLOCKED (script exit 2). Preserve raw target transcript, versions, source revision and errors. Host-model results do not replace this gate.

[Return to codelab](../../../codelab/codelab.md).
