# Step 4: starter specification

Task only, not compilable source.

## Goal

Use request ownership and a monotonic deadline.

## Inputs and work

- Accept decimal integers 0 through 12 for this unsigned 32-bit teaching contract; larger factorials overflow.
- Serialize requests; busy hardware cannot silently replace pending work. Read only after completion, and distinguish timeout from valid input zero.

## Required acceptance evidence

Future QNX expectations: 0 and 1 return 1; 10 returns 3628800. These are mathematical expectations, not observed target results.

## Gate

Host: make check-step4 launches a fresh source/image-bound accumulated target run when the external bundle and exclusive lease are supplied. Without them it remains BLOCKED (exit 2). Preserve raw target transcript, versions, source revision and errors. Host-model results do not replace this gate.

[Return to codelab](../../../codelab/codelab.md).

## Source entry

main.c deliberately returns2 until the learner implements the documented contract. Compare the original solution only after attempting the exercise.
