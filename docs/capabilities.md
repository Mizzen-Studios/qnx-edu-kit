# Capability ledger

qnx-edu-kit learner-owned fault-to-fix lab

Nov8 approved bounded executable upgrades; historical rows retain their original receipts. HOST interface checks and native observations are distinct; new independent council gate pending. Existing licensed SDK only, current split-host readiness blocked, no new-install/second-SDK/human claim; path policy BLOCKED, ability control explicitly separate. C6/native safety STOPPED; SocketCAN UNVERIFIED; no safety/timing/availability/platform-health claims.

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
| own-session-cockpit | host | workflow | PASS | Operable local notebook and CLI own-source orchestration; browser notes/export controls are host behavior, not human learning. | [source](../docs/learner-cockpit.md) |
| own-wrapper-step3 | native | learner-run | PASS | Actual notebook wrapper wrong stage FAIL despite app0, corrected PASS; all attempts preserved and own source/build/native bindings retained. | [source](../docs/acceptance/wrapper-20261108/correct-native.json) |
| own-wrapper-dev-edu | native | learner-run | PASS | Actual own wrapper /dev/edu write10/read3628800 with IRQ completion1 and ack0; no reference import or all-platform acceptance. | [source](../docs/acceptance/wrapper-20261108/finish-native.json) |
| ability-stage | native | learner-run | PASS | Same ELF separate processes: denied IO yields EPERM, narrowed IO subrange0..0 permits IO_LEVEL_1. Ability control only, not /dev pathname policy or platform minimum. | [source](../docs/acceptance/ability-20261108/receipt.json) |
| pathname-policy | native | runtime | UNVERIFIED | BLOCKED: SDK tools available; loaded policy identity and attach/connect pathname enforcement not established. | [source](../docs/acceptance/prereq-20261108/receipt.json) |
| single-host-readiness | host | setup | UNVERIFIED | Parameterized user-supplied legal paths and exact next-command planner implemented; current split SDK/QEMU environment correctly blocks combined single-host readiness, not portability PASS. | [source](../docs/acceptance/wrapper-20261108/setup-split-host-blocked.json) |
