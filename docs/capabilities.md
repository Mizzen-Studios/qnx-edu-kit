# Capability ledger

qnx-edu-kit learner-owned fault-to-fix lab

Supported topology: split-host licensed SDK guest build, STOP/REAP guest, then capped HOST QEMU under sole lease. Recorded native rows retain original immutable source/ELF/IFS/disk bindings, not a current-tip rerun. Single-host BLOCKED_NATIVE_TIMEOUT (Nov9), root cause UNVERIFIED; no retries/tuning/cap increases. HOST notes and native observations distinct. No second-SDK/human/platform-health claim; pathname policy BLOCKED. C6 STOPPED; no video; private £0; independent review pending.

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
| own-session-cockpit | host | workflow | PASS | HOST local notes/export companion with labeled split guest-build/STOP-REAP/host-run handoff. Standalone split receipts are not automatically notebook attempts; not human acceptance. | [source](../docs/learner-cockpit.md) |
| own-wrapper-step3 | native | learner-run | PASS | Recorded Nov8 split-host, explicit environment path mapping, not a current-tip rerun: Actual notebook wrapper wrong stage FAIL despite app0, corrected PASS; all attempts preserved and own source/build/native bindings retained. | [source](../docs/acceptance/wrapper-20261108/correct-native.json) |
| own-wrapper-dev-edu | native | learner-run | PASS | Recorded Nov8 split-host, explicit environment path mapping, not a current-tip rerun: Actual own wrapper /dev/edu write10/read3628800 with IRQ completion1 and ack0; no reference import or all-platform acceptance. | [source](../docs/acceptance/wrapper-20261108/finish-native.json) |
| ability-stage | native | learner-run | PASS | Same ELF separate processes: denied IO yields EPERM, narrowed IO subrange0..0 permits IO_LEVEL_1. Ability control only, not /dev pathname policy or platform minimum. | [source](../docs/acceptance/ability-20261108/receipt.json) |
| pathname-policy | native | runtime | UNVERIFIED | BLOCKED: SDK tools available; loaded policy identity and attach/connect pathname enforcement not established. | [source](../docs/acceptance/prereq-20261108/receipt.json) |
| single-host-readiness | host | setup | UNVERIFIED | BLOCKED_NATIVE_TIMEOUT: Nov9 package/user-bus setup PASS and own build PASS; native timeouts before learner markers/appRC. Root cause UNVERIFIED. Wrong FAIL/app0 not observed; corrected PASS not run. No retries/tuning/cap increases. | [source](../docs/acceptance/choice-a-20261109/receipt.json) |
