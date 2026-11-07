# Capability ledger

qnx-edu-kit learner-owned fault-to-fix lab

Reference acceptance, compilation and learner execution are separate. No reference receipt or host model can satisfy learner-run acceptance. QSTI provenance and independent human learner validation remain unverified. No DMA-IRQ/secpol expansion in this slice.

Canonical declarations: docs/capabilities.json. Generated view; ledger checks are not runtime acceptance.

**Native observations: observed in this QEMU run · app budget, not a QNX benchmark.**

| Capability | Domain | Level | Status | Bounded claim | Evidence |
|---|---|---|---|---|---|
| host-checks | host | framework | PASS | Host source contracts/models/packaging only; no native proof | [source](../docs/test-results.md) |
| e1-reference | native | reference-run | PASS | Accumulated unchanged E1 all-six-step reference plus IRQ, polled DMA and /dev/edu normal I/O | [source](../docs/acceptance/native-20261107/receipt.json) |
| e2-compile | native | compile | PASS | All6 solutions and6 starters cross-compiled; TODO starter compilation is not runtime completion | [source](../docs/acceptance/e2-qcc-20261107/receipt.json) |
| learner-step3 | native | learner-run | PASS | Local E1 substrate only: actual edited step3 C compiled and freshly booted; wrong challenge FAIL despite app exit0, corrected challenge PASS. Not all-six learner acceptance or clean BSP portability. | [source](../docs/acceptance/learner-20261107/correct-native.json) |
| learner-dev-edu | native | learner-run | UNVERIFIED | Learner-owned /dev/edu finish not yet proved | [source](../steps/step6/starter/main.c) |
| clean-setup | native | setup | UNVERIFIED | Legal licensed SDP/BSP-owned setup must not require distributed SDK/images/private owner bundle; clean-machine reproduction pending | [source](../docs/e2-build-order.md) |
| learner-step3-negative | native | learner-run | FAIL | Intentional wrong-but-compiling edit: stage FAIL although application prints PASS and exits0; expected negative control, not learner completion. | [source](../docs/acceptance/learner-20261107/wrong-native.json) |
