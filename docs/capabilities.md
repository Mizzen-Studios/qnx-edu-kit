# Capability ledger

qnx-edu-kit learner-owned fault-to-fix lab

Reference acceptance, compilation and learner execution are separate. No reference receipt or host model can satisfy learner-run acceptance. QSTI provenance and independent human learner validation remain unverified. No DMA-IRQ/secpol expansion in this slice.

Canonical declarations: docs/capabilities.json. Generated view; ledger checks are not runtime acceptance.

**Native observations: observed in this QEMU run · app budget, not a QNX benchmark.**

| Capability | Domain | Level | Status | Bounded claim | Evidence |
|---|---|---|---|---|---|
| host-checks | host | framework | PASS | Source-bound host suite83total:81passed/2skipped; models/contracts/packaging only, not native proof | [source](../docs/acceptance/learner-finish-clean-20261107/final-host-receipt.json) |
| e1-reference | native | reference-run | PASS | Accumulated unchanged E1 all-six-step reference plus IRQ, polled DMA and /dev/edu normal I/O | [source](../docs/acceptance/native-20261107/receipt.json) |
| e2-compile | native | compile | PASS | All6 solutions and6 starters cross-compiled; TODO starter compilation is not runtime completion | [source](../docs/acceptance/e2-qcc-20261107/receipt.json) |
| learner-step3 | native | learner-run | PASS | Fresh clean stock generic platform: actual edited step3 C wrong intendedFAIL/correctedPASS, repeated on final fixed PCI topology; no E1/stripped kernel, broad portability or human-review claim. | [source](../docs/acceptance/clean-step3-20261107/native-clean/final-topology/correct-native.json) |
| learner-dev-edu | native | learner-run | PASS | One edited step6 starter: fresh clean-image normal write10/read3628800 with IRQ completion and ack, source-bound; no reference checker, human/all-stage or platform-health claim. | [source](../docs/acceptance/learner-finish-clean-20261107/unmasked/native.json) |
| clean-setup | native | setup | PASS | One pinned clean generic setup: stock kernel built using512MiB RAM+1GiB guest swap; native wrong intendedFAIL/correctedPASS. Startup Memoryfault preserved; no broad portability, SSH-health or independent-review claim. | [source](../docs/acceptance/clean-step3-20261107/native-clean/receipt.json) |
| learner-step3-negative | native | learner-run | FAIL | Intentional wrong-but-compiling edit: stage FAIL although application prints PASS and exits0; expected negative control, not learner completion. | [source](../docs/acceptance/clean-step3-20261107/native-clean/final-topology/wrong-native.json) |
| clean-stock-image-build | host | build | PASS | Fresh unmodified stock generic IFS/disk completed with512MiB guest+1GiB guest disk swap, unchanged hostcaps; isolated service exit0 and queue zero restarts. Previous guestOOM preserved. | [source](../docs/acceptance/clean-step3-20261107/swap-attempt/outcome.json) |
