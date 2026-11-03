# Step 5: starter specification

Task only, not compilable source.

## Goal

Teach standalone interrupt ownership rather than io-sock assumptions.

## Inputs and work

- Review actual InterruptAttachThread and InterruptWait declarations locally; no guessed signatures are supplied. Inspect IO and INTERRUPT abilities and active policy before attach.
- On EPERM capture the failing operation and inspect grants; do not recommend broad privilege. For INTx inspect owned status, acknowledge device sources, then follow documented unmask rules. InterruptAttachEvent is contextual for io-sock, not an interchangeable standalone sample.

## Required acceptance evidence

Test shared/unrelated IRQ, stale status, timeout, missing ability and repeated attach/detach. Delivery alone does not establish completion.

## Gate

Host: make check-step5 remains BLOCKED (script exit 2). Preserve raw target transcript, versions, source revision and errors. Host-model results do not replace this gate.

[Return to codelab](../../../codelab/codelab.md).
