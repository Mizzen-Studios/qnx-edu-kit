# Step 6: IAT-backed resource manager — starter

## Goal and source boundary

Read factorial, parse_command, edu_write, edu_read and main in the resource-manager solution. One dispatch thread owns PCI, IAT and registers. Each synchronous successful write uses InterruptWait, checks pending AND not-busy, acknowledges and unmasks before publishing. No polling fallback. A write is one complete command: 1–2 ASCII digits, optional LF, maximum three bytes, 0..12. Nonblocking requests return EAGAIN; results have per-open snapshots, offsets and EOF. Register /dev/edu mode 0660 only after PCI/BAR/IAT setup; dispatch remains a long-running process.

main.c preserves earlier gates and contains a bounded TODO for this boundary. It refuses completion with a nonzero result; it does not publish a fake target PASS. Step6 retains reference handler scaffolding but deliberately omits resource-manager registration. Complete the TODO in a separate learner workspace.

## Compile contract

From repository root in an authorized initialized SDP environment, use qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -o "$EDU_OUT/step6-starter" steps/step6/starter/main.c -lpci. EDU_OUT must be an existing absolute directory outside the checkout. The starter may report expected unused scaffolding warnings until completed. See [build order](../../../docs/e2-build-order.md) before running anything.

## Required acceptance evidence

Reference expected marker: EDU STEP6 PASS. Require the separate native acceptance client plus shell 10 → 3628800 and IRQ completion evidence. Record target identity, source hashes, image checksum, errors and full transcript. Historical E1 artifacts document reference observations, not a new learner run.

## Gate

Host: make check-step6 checks that all teaching snapshots still derive from native source, then requests a fresh accumulated E1 reference run. Missing external bundle or lease is BLOCKED (exit 2). The manifest binds native source and image; saved fixtures never satisfy this gate. An edited learner source is intentionally refused by the reference checker: rebuild and separately validate your own target image instead of presenting reference acceptance as yours. No helper here creates a learner IFS or installs SDK files.

[Return to codelab](../../../codelab/codelab.md).
