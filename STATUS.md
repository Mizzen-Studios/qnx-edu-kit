# Status — 7 November 2026

## Current bounded validation — 7 November 2026

Fresh stock generic build completed with 512 MiB guest RAM + 1 GiB disk-backed
swap; host caps remain 100% CPU / 1 GiB / nice 15. Builder isolated from
host-queue.service; queue stayed active with zero restarts. Original diagnosis900
receipts are unchanged. [Build evidence](docs/acceptance/clean-step3-20261107/swap-attempt/NOTES.md).

Fresh [clean learner step3](docs/acceptance/clean-step3-20261107/native-clean/NOTES.md):
wrong edit stage FAIL/1 despite app exit 0, corrected native PASS/0. Only the wrong
MMIO readback check failed; all provenance, caps and QEMU cleanup checks passed.
Both logs preserve an unattributed startup Memory fault after Starting sshd.
No full-platform/SSH-health, broad portability or independent-review claim.
Learner /dev/edu is separately assessed, never transferred from reference PASS.
C6 remains STOPPED. Everything private; no deployment, contacts or spend.

## Preserved earlier milestones (not current clean-path claims)

## Historical unchanged E1 reference acceptance

**PASS: fresh native reference functional acceptance and clean-checkout end-to-end verify.sh.**

- Direct parent-owned acceptance returned0 with all six target markers, IRQ raise/wait/ack,64-byte byte-exact RAM→EDU→RAM DMA (polled; not DMA-IRQ proof), and actual shell echo10/cat3628800 through the IAT IRQ-driven resource manager.
- Receipt validates CPU100000/100000, memory1073741824bytes, nice15. Guest1vCPU/512MiB; no other native guest ran concurrently.
- Clean detached checkout `387ba38ce696c92bb3d8332ea7f01d5a0630cbfc` ran full `verify.sh`, exit0. Host suite55cases:53pass+2explicit optional/live integration skips. Fresh native steps1–6 allPASS; no saved transcript accepted as input. Checkout stayed clean.
- Evidence: [direct receipt](docs/acceptance/native-20261107/receipt.json), [serial](docs/acceptance/native-20261107/serial.txt), [clean-checkout receipt](docs/acceptance/native-20261107/clean-checkout-receipt.json), [complete verify output](docs/acceptance/native-20261107/clean-checkout-verify.txt). Source/image hashes bound in each receipt.

All observations are **observed in this QEMU run · app budget, not a QNX benchmark**.

## Recovery and remaining boundaries

The old worker was killed/stalled, the handoff file absent, and no owned QEMU remained. The coordinator took over directly without file-event waiting. No live processes needed killing to free the stale lease. The cap collector fix includes the exec-replaced QEMU root PID; the failed old null-cap receipt is not promoted to success. The original source-bound image worked; an unfinished dedicated-startup rebuild was not required or represented as completed.

Target is custom licensed SDP8 Generic BSP/QNX8, **not established QSTI provenance**. Functional PASS is not a certification, least-privilege/security-policy, physical-device, graceful-stop, comprehensive fault injection or two-fresh-learner acceptance claim. No licence/SDK/header/library/image/binary/QSC/credential material is committed. Guests stopped/reaped after each owned run, shared native lease free. Repos private; nothing published and no spending or outreach.

## E2 host-only teaching scaffold — 7 November 2026

Six incremental C solutions and bounded starter TODOs now derive from unchanged
E1 native source (387ba38 acceptance). Codelab teaches PCI/BAR/factorial/IAT/
polled DMA/IAT resmgr only. Source drift is rejected before check-step launches
a fresh native reference; no transcript replay or learner-binary claim.
See [build order](docs/e2-build-order.md). All six solution snapshots passed actual qcc -Werror and all six starters
compiled (TODOs remain). [Receipt](docs/acceptance/e2-qcc-20261107/receipt.json).
Per-snapshot native execution and fresh learners remain pending; QSTI provenance unverified.

## E2 recovery host/docs milestone — 11:06 UTC

Reconciled build-order text with existing twelve-snapshot qcc receipt; added step boundary/runtime checklist and regression binding all12 source hashes to that compile-only receipt. Fresh host suite62 cases:60pass,2explicit skips; local static render refreshed. No new guest or native snapshot execution; per-snapshot runtime and fresh learners remain pending. C6 focused attempt failed; its native lane is stopped.

## Learner-owned step3 review milestone

Actual edited C was cross-compiled, imaged and freshly booted twice in serialized QEMU:
- Wrong edit: write12345679/readedcba986, target exit0 and application PASS, independent stage exit1 (expected FAIL).
- Correct edit: write12345678/readedcba987, target exit0, independent stage exit0 (PASS).
- Exact edits, receipts and raw logs: docs/acceptance/learner-20261107/ (including NOTES.md); [learner journey](docs/learner-lab.md). Source, ELF, image, disk and driver hashes recorded; reference checker unchanged.
- Effective host CPU100%/1GiB/nice15, guest1vCPU/512MiB. Guests stopped/reaped and lease released. C6 never started.

Observed in this QEMU run · app budget, not a QNX benchmark. Local E1 BSP substrate adapted externally; clean learner BSP portability UNVERIFIED. A private debug-stripped licensed kernel copy avoided SDK relink OOM without increasing caps or changing SDK originals. Raw logs preserve a pre-learner SSH startup memory fault: no SSH health claim. No IRQ/DMA or /dev/edu learner PASS, QSTI provenance, malicious-output resistance or human validation. Await independent journey review before expansion.

## Final conditional-gate host verification

Detached clean checkout d419bce ran ./verify.sh --host-only exit0: 79 total / 77 PASS / 2 SKIP; site, ledger and redistribution checks PASS. [Source-bound parent receipt](docs/acceptance/clean-step3-20261107/parent-review.json) pins actual host log and OOM/compile/cleanup evidence. Host PASS does not resolve the clean native bootstrap BLOCKED/UNVERIFIED gate.
