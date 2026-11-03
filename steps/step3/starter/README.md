# Step 3: starter specification

Task only, not compilable source.

## Goal

A mapped address is not proof of a device protocol.

## Inputs and work

- Register offsets and values remain withheld until every row has live pinned-QEMU evidence. Source inspection alone is insufficient.
- Validate width, alignment and bounds; check identity before writing. Test complementary liveness patterns and width-limited inverse readback. Unmap on failure.

## Required acceptance evidence

Wrong identity, failed mapping and out-of-bounds requests are bounded errors, never PASS.

## Gate

Host: make check-step3 remains BLOCKED (script exit 2). Preserve raw target transcript, versions, source revision and errors. Host-model results do not replace this gate.

[Return to codelab](../../../codelab/codelab.md).
