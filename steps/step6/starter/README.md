# Step 6: starter specification

Task only, not compilable source.

## Goal

Turn messages into a predictable client contract.

## Inputs and work

- Define bounded decimal input with optional newline, partial-write behavior, per-open result ownership and serialization. Cap message size before parsing.
- Implement partial reads, offsets and EOF, errors without stale output and cancellation using actual installed resmgr declarations. Publish readiness last; process death does not reset hardware.

## Required acceptance evidence

Future target acceptance: write 10 to /dev/edu and read 3628800. Test concurrent clients, malformed input, partial reads, death and re-probe.

## Gate

Host: make check-step6 launches a fresh source/image-bound accumulated target run when the external bundle and exclusive lease are supplied. Without them it remains BLOCKED (exit 2). Preserve raw target transcript, versions, source revision and errors. Host-model results do not replace this gate.

[Return to codelab](../../../codelab/codelab.md).

## Source entry

main.c deliberately returns2 until the learner implements the documented contract. Compare the original solution only after attempting the exercise.
