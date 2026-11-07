# Step 4: Bounded factorial polling — starter

## Goal and source boundary

Read the status register at 0x20 (r[8]) and factorial at 0x08 (r[2]). Disable factorial IRQ for this polling exercise, submit 10, then test busy at most 1000 one-millisecond sleeps. Require completion and 3628800; an iteration budget is not a measured wall-clock guarantee. The client contract in step6 accepts only 0..12 to avoid unsigned 32-bit overflow.

main.c preserves earlier gates and contains a bounded TODO for this boundary. It refuses completion with a nonzero result; it does not publish a fake target PASS. Step6 retains reference handler scaffolding but deliberately omits resource-manager registration. Complete the TODO in a separate learner workspace.

## Compile contract

From repository root in an authorized initialized SDP environment, use qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -o "$EDU_OUT/step4-starter" steps/step4/starter/main.c -lpci. EDU_OUT must be an existing absolute directory outside the checkout. The starter may report expected unused scaffolding warnings until completed. See [build order](../../../docs/e2-build-order.md) before running anything.

## Required acceptance evidence

Reference expected marker: EDU STEP4 PASS factorial polling. Earlier boundaries must complete without using later hardware operations. Record target identity, source hashes, image checksum, errors and full transcript. Historical E1 artifacts document reference observations, not a new learner run.

## Gate

Host: make check-step4 checks that all teaching snapshots still derive from native source, then requests a fresh accumulated E1 reference run. Missing external bundle or lease is BLOCKED (exit 2). The manifest binds native source and image; saved fixtures never satisfy this gate. An edited learner source is intentionally refused by the reference checker: rebuild and separately validate your own target image instead of presenting reference acceptance as yours. No helper here creates a learner IFS or installs SDK files.

[Return to codelab](../../../codelab/codelab.md).
