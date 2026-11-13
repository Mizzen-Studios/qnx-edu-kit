# Status — bounded stock checkpoint 13 November 2026

## Current Nov13 working stock recipe

**[Coherent OWN journey verified](docs/acceptance/coherent-stock-20261113/RESULT.md):** one notebook wrong FAIL/app0 → corrected PASS → own10→3628800 with IRQack/private pulse/slog2 →108-file verified export. Exact runtime source `769a4c906c6b172c3624f8fe897b71e3c5d7e6b8`; three fresh application builds, unchanged reused stock IFS/disk, no retries. Later documentation commits report that source-bound run, not another execution at the final tip.

**Earlier step6-only [clean-clone own checkpoint](docs/acceptance/coldreader-stock-20261113/RESULT.md):** one fresh step6 application build and stock-native run passed10→3628800/IRQack/private pulse/slog2; own41-file export verified after a documented offline CRLF validator fix. New notebook/source, reused approved stock IFS/disk; no image rebuild or native retry. Untouched step3 stays unvalidated.

Follow the [working stock learner recipe](docs/learner-route.md): existing licensed SDK Linux guest1GiB, HOST2GiB/TCG256/reserve64/CPU100/nice15/smp1/swap0, QNX target512MiB. [Stock generation and MMIO gates succeeded](docs/acceptance/stock-retry-20261113/RESULT.md); [actual10→3628800 + IRQack/private pulse/slog2](docs/acceptance/irq-retry-20261113/RESULT.md) uses explicit --pci-line (config11 vs API10), no routing rewrite. The fresh cold-reader adapter compiles OWN code and explicitly reuses those hashed external stock artifacts; no new image-generation claim. SSH faults/networking remain UNVERIFIED; serial transfer only. Earlier OOM/default-IRQ failures below are dated history, not the current stock blocker. No media/CAN/C6 or broader acceptance promotion.

## Historical Nov13 SDK512 gate — OOM before native (superseded)

[Exact clean-stock receipt](docs/acceptance/stock-20261113/NOTES.md): **BLOCKED_CLEAN_STOCK_IFS_OOM**. Fresh standard mkqnximage project, explicit512M/1CPU; only authored snippet added -device edu through verified QEMU_OPTIONS, no lesson/custom IFS integration. Guest killed PID1620 at329384KiB anon RSS during Generating ifs; IFS=0bytes, no bootable disk. HOST monitored peak1105190912bytes under enforced2GiB; swap0 and sampled HOST OOM events0. This was a guest memory failure, not a demonstrated HOST cap breach. SDK reaped, lease free. At that bounded SDK512 attempt the stock native gates were NOT_RUN. The later explicitly authorized SDK1GiB stock build and config-line finish above supersede this blocker; this failed receipt remains unchanged. Historical advanced source and receipts remain unchanged.

## Historical Nov10 feature gate: stopped at stock image build

[Measured bounded receipt](docs/acceptance/features-20261110/NOTES.md): **BLOCKED_STOCK_MKIFS_OOM**. Own wrong-step3 source compiled and linked serially in the existing licensed SDK; stock platform image generation then OOM-killed a mkifs child (PID1617, anon RSS328616KiB). ifs.bin is zero bytes, not a bootable image. No HOST native run followed. Step6 compilation, new IRQ→private pulse→publication, bounded slog2 runtime capture and optional trace remain **NOT_RUN / UNVERIFIED**. Same caps; no swap/platform/package changes; SDK stopped/reaped and lease free. Historical Nov8 wrong/correct/finish receipts are unchanged, not proof of this new code. No new native PASS. Stop for independent owner review.

## Historical Nov9 product lock — supported split-host, copy-only

Follow [the canonical route](docs/learner-route.md): licensed SDK guest builds → **STOP/REAP guest** → capped **HOST QEMU**, with one exclusive lease. Recorded [Nov8 wrapper journey](docs/acceptance/wrapper-20261108/NOTES.md) retains wrong FAIL despite app exit0, corrected PASS and original own export bindings. No native rerun at this documentation tip. HOST notes and standalone split receipts remain separately labeled.

Single-host **BLOCKED_NATIVE_TIMEOUT**: [immutable receipt](docs/acceptance/choice-a-20261109/receipt.json), root cause **UNVERIFIED**. No more single-host runs, timeout tuning or cap increases. No video; C6 STOPPED; private £0; independent review required.

## Recorded Choice A wave — 9 November: setup PASS, native BLOCKED

[Nov9 receipts](docs/acceptance/choice-a-20261109/NOTES.md): same existing licensed SDK host booted normally with real /boot and /boot/efi mounts; no boot repair needed. Expressly approved dpkg recovery, free distro QEMU and real packaged systemd user bus succeeded. Fresh own source/ELF/IFS/disk build PASS. Canonical nested-TCG native observations timed out at180s and one bounded900s retry, before learner markers/appRC: wrongFAIL/app0 NOT_OBSERVED, correctedPASS NOT_RUN. Validated own failure-evidence export retained, not learner acceptance. Inner/outer caps unchanged; all QEMU reaped and lease free. No further work scheduled; supported topology is split-host. Earlier single-host setup blockers below are historical, not current package/session state.

## Recorded upgrade — 8 November 2026, implemented; scoped verification complete, council gate pending

Olly approved the substantive [upgrade package](docs/upgrade-acceptance-20261108.md); the earlier feature-freeze statements below are preserved history, not the current instruction. Previous independent acceptance remains conditional and does not transfer to these new features.

[Fresh prerequisite receipts](docs/acceptance/prereq-20261108/NOTES.md): same-ELF IO ability deny/allow in separate runs, bounded structured slog2 capture and actual co-located observer death/separate recorder survival were observed in the bound QEMU run. **Pathname policy BLOCKED**: installed tools alone do not establish attach/connect enforcement or loaded policy identities. Ability control is not /dev path policy or least-privilege proof.

The [own-session cockpit](docs/learner-cockpit.md) is implemented with persisted notes, fixed CLI commands, own-source build/run orchestration and local evidence export. Host/browser checks remain HOST-only. Fresh actual wrapper runs are now [receipt-backed](docs/acceptance/wrapper-20261108/NOTES.md): wrong-step FAIL despite app0, corrected PASS, own /dev/edu10→3628800 with IRQ completion1/ack0; all nine attempts retained. The [ability-only stage](docs/ability-lesson.md) has same-ELF separate-process deny EPERM versus narrowed IO0..0 allow proof; it is not pathname policy. [Integrity review fixes](docs/acceptance/review-fixes-20261108/NOTES.md) now validate exports by action/assets, qualify historical-source PASS, and require explicit draft conflict resolution. Independent focused recheck PASS for all four assigned integrity findings; [final host verification and chronology](docs/acceptance/final-upgrade-20261108/NOTES.md) records exact tested revisions. This is not new council acceptance or a full audit. That earlier setup blocker is superseded by Nov9 BLOCKED_NATIVE_TIMEOUT above; no fresh-install, second-SDK or human-learning acceptance.

C6/native safety STOPPED; SocketCAN UNVERIFIED. No heartbeat, actuation, recording, publication or deployment. recorded:false. Videos remain deferred until all features and final verification, with the separate recording gate preserved. sshd internal cause UNVERIFIED; no platform-health, safety, timing or continuous-availability claim.

## Preserved prior review and milestone history


Start only with the [canonical learner route](docs/learner-route.md).

## Historical completion gate — 7 November, 20:03 UTC

Owner independent completion gate: **CONDITIONAL, receipt-inspected, not re-run**, at accepted tip ada5d0ff03533a2fec0983f3fedbd9bada9df8a9. The 21:05 portability/diagnostics follow-up does not broaden acceptance. Canonical instruction tip 5876304a82d1c07ecde7401a9c522ef28ec268de is host-route packaging only; fresh-clone syntax/init and SDK-boundary negatives are not second-SDK portability proof. Renewed bounded diagnostic results are separately recorded in docs/acceptance/portability-20261107/. Existing licensed SDK reuse and owner-lab paths only; no fresh install, second SDK, human learner or platform-health validation. CANopy native evidence was not rerun. sshd internal cause UNVERIFIED; C6 FAIL / STOPPED; SocketCAN UNVERIFIED. Everything private.

Recorded native result: [bootstrap-final](docs/acceptance/bootstrap-final-20261107/NOTES.md), wrong FAIL/app0 → correct PASS → own /dev/edu 10→3628800, IRQ completion1/ack0. Earlier sections below are dated history, not current blockers.

[Private evidence review](REVIEW.md) records exact bindings and unresolved gaps.

[Capability ledger](docs/capabilities.md) records scoped evidence and exclusions.

## Historical bounded validation — 7 November 2026

Fresh stock generic build completed with 512 MiB guest RAM + 1 GiB disk-backed
swap; host caps remain 100% CPU / 1 GiB / nice 15. Builder isolated from
host-queue.service; queue stayed active with zero restarts. Original diagnosis900
receipts are unchanged. [Build evidence](docs/acceptance/clean-step3-20261107/swap-attempt/NOTES.md).

Fresh [clean learner step3](docs/acceptance/clean-step3-20261107/native-clean/NOTES.md):
wrong edit stage FAIL/1 despite app exit 0, corrected native PASS/0. Only the wrong
MMIO readback check failed; all provenance, caps and QEMU cleanup checks passed.
These historical logs preserve the startup Memory fault; later diagnosis attributes the process to sshd, internal cause UNVERIFIED.
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

### Scoped learner /dev/edu result — 7 November 2026

Edited step6 starter on the same fresh stock generic platform passed actual normal write/read10→3628800 and IRQ completion/ack. Source, binary, image, disk and caps are bound in the [learner finish evidence](docs/acceptance/learner-finish-clean-20261107/NOTES.md). No reference checker, host result injection or polling fallback. Earlier failures remain; startup Memory fault still excludes a healthy-SSH/all-platform claim. Current owner gate is CONDITIONAL, receipt-inspected not re-run; no safety/timing acceptance; C6 stays STOPPED.

Supported canonical route observed on one existing licensed SDK: [supported-bootstrap result](docs/acceptance/bootstrap-final-20261107/NOTES.md). Fresh stock platform, wrong stageFAIL/app0, correctedPASS and own /dev/edu write10/read3628800+IRQack. Automated reuse only, not a second SDK or human gate. Old missing-host-SDK negative preserved. All guests reaped; no platform-health claim.

## Historical 7 November 21:05 follow-up — superseded topology

**Historical statement, NOT current instructions:** a single licensed Linux x86_64 host was then the default and split-host optional. Superseded: supported topology is now **split-host**, SDK guest build → STOP/REAP guest → capped HOST QEMU; single-host BLOCKED_NATIVE_TIMEOUT, root cause UNVERIFIED. Existing SDK reused; a clean second installation remains BLOCKED unless cached free NC entitlement and complete legal offline inputs can be established without login or licensing interaction. No native feature/sshd fix, capture or publication. Historical runtime pins and the 20:03 accepted conditional gate remain unchanged.

21:05 bounded follow-up result: fresh non-owner-path host87/85pass/2skip; canonical instructions5876304. Second SDK BLOCKED at read-only metadata/entitlement boundary, no install/login/licence change. Renewed unchanged baseline and separate traced image reproduce sshd Memory fault/core; internal cause UNVERIFIED, no fix or platform-health claim. No new slog2/backtrace. Guests stopped/reaped, lease free. [Exact follow-up receipts](docs/acceptance/portability-20261107/NOTES.md).
