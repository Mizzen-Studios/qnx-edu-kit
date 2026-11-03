# Live verification ledger — NOT tutorial instructions

All rows BLOCKED. No edu register offset, value or bit is proven. The plan's candidate numbers are deliberately not repeated in learner material. Before implementing a row, pin QEMU commit/version and compare its docs/specs/edu.rst with hw/misc/edu.c. Record actual candidate offset/access width/value/semantics here in a reviewed follow-up; do not infer a QNX API from QEMU source.

| Row | Required live experiment | State / transcript |
|---|---|---|
| PCI identity | Enumerate actual vendor/device and BAR sizes/types; ownership/detach | BLOCKED / none |
| ID | Read identity; record offset, width, value and byte order | BLOCKED / none |
| Liveness | Multiple write/read inverse patterns; access width and mask | BLOCKED / none |
| Factorial | Supported input range, result, busy behavior, timeout | BLOCKED / none |
| Status | Busy/completion and IRQ enable bits, read/write semantics | BLOCKED / none |
| IRQ status | Pending bits and clearing behavior with INTx | BLOCKED / none |
| IRQ raise | Controlled raise with observed interrupt | BLOCKED / none |
| IRQ ack | Correct ack, no stuck line, subsequent interrupts work | BLOCKED / none |
| DMA source | Width, address and direction semantics | BLOCKED / none |
| DMA destination | Width, device/host address semantics | BLOCKED / none |
| DMA count | Bounds, zero/oversize behavior | BLOCKED / none |
| DMA command | Start/direction/IRQ bits, completion status | BLOCKED / none |
| DMA buffer | Device address, size and out-of-range behavior | BLOCKED / none |
| DMA mask | Actual default and dma_mask property existence; boundary/clamping | BLOCKED / none |
| Interrupt model | INTx default; MSI only if actually tested | BLOCKED / none |

## Required evidence per row

- Date, operator, clean-clone commit, host/guest architecture and OS.
- SDP build, toolchain selection, QSTI version/image hash (no image redistribution), QEMU version and pinned source hash.
- Exact reviewed local build/run commands, access widths, input/output and expected-vs-observed result; failure/timeout paths.
- Relevant source/doc reference lines and distinction between source reading, host model and live target result.
- Sanitized transcript file + hash, reviewer and limitations. No credentials, proprietary source, image or SDK files.

## Whole-project acceptance (all pending)

1. Approved local licensed SDK setup, verified target boot and deployment user/path.
2. Current PCI server API review, BAR lifecycle, restart-safe re-probe, bounds.
3. Every register row above live verified before implementing or teaching it.
4. Abilities and secpol deny/allow experiments; least privilege after attach; exact policy syntax verified. No guessed policy distributed.
5. Real IAT/InterruptWait lifecycle, concurrent operations, error and cleanup tests.
6. Real resource-manager finish line, malformed/overflow/partial I/O and concurrency tests.
7. DMA/cache/physical-address handling and restart/trace extras independently gated.
8. Eight source diagrams and rendered SVGs from verified flows; claat export validated.
9. Two fresh-agent clean-machine runs following only the codelab; actual elapsed times, failures and corrections recorded.
10. Mandatory real QNX capture; publication, Pages, PR and submission require separate permission.

Host model tests, if later added, must carry pinned-source provenance and UNVERIFIED MODEL labels; never upgrade these live statuses based on a host test.
