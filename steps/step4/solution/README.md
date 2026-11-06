# Step 4: solution specification

Original C source entry main.c now exists. The solution shares the checked native implementation; fresh target acceptance and QSTI provenance are separate gates.

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

main.c is the original accumulated solution entry; steps1–5 share native/edu_probe.c and step6 shares native/edu_resmgr.c. The separate target client validates the shell and error/read/write cases. No host model substitutes for target execution.
