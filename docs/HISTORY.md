# Dated project history

Archived README narrative through 20 November 2026. Historical counts, private-state instructions and native outcomes describe their own checkpoints, not current status. See [current judge entry](../README.md). No raw receipts were rewritten.

# edu-kit — learn QNX by making a convincing wrong edit
[Judges: start here](../docs/JUDGES.md)

QNX Global Hackathon 2026 entry (Low-level Software; Best Codelab/Tutorial). Apache-2.0.

## Two explicit stock admission routes

New: [build your own stock platform](../docs/independent-stock.md) in your existing legal SDP, with a controlled recipe and separately bound cooperative owner completion. Different per-user image hashes are admitted only through the explicit independent route, never by changing the historical pins. [Current source-bound result](../docs/acceptance/independent-stock-20261119/RESULT.md) distinguishes native execution from HOST tests. No independent-human or fresh-install claim.

## Current Nov13 working stock recipe

**[Coherent OWN journey verified](../docs/acceptance/coherent-stock-20261113/RESULT.md):** one notebook wrong FAIL/app0 → corrected PASS → own10→3628800 with IRQack/private pulse/slog2 →108-file verified export. Exact runtime source `769a4c906c6b172c3624f8fe897b71e3c5d7e6b8`; three fresh application builds, unchanged reused stock IFS/disk, no retries. Later documentation commits report that source-bound run, not another execution at the final tip.

**Earlier step6-only [clean-clone own checkpoint](../docs/acceptance/coldreader-stock-20261113/RESULT.md):** one fresh step6 application build and stock-native run passed10→3628800/IRQack/private pulse/slog2; own41-file export verified after a documented offline CRLF validator fix. New notebook/source, reused approved stock IFS/disk; no image rebuild or native retry. Untouched step3 stays unvalidated.

Follow the [working stock learner recipe](../docs/learner-route.md): existing licensed SDK Linux guest1GiB, HOST2GiB/TCG256/reserve64/CPU100/nice15/smp1/swap0, QNX target512MiB. [Stock generation and MMIO gates succeeded](../docs/acceptance/stock-retry-20261113/RESULT.md); [actual10→3628800 + IRQack/private pulse/slog2](../docs/acceptance/irq-retry-20261113/RESULT.md) uses explicit --pci-line (config11 vs API10), no routing rewrite. The fresh cold-reader adapter compiles OWN code and explicitly reuses those hashed external stock artifacts; no new image-generation claim. SSH faults/networking remain UNVERIFIED; serial transfer only. Earlier OOM/default-IRQ failures below are dated history, not the current stock blocker. No media/CAN/C6 or broader acceptance promotion.

A learner-owned PCI-to-/dev/edu lab: **wrong edit FAIL despite application exit0 → corrected PASS → shell write10/read3628800**.
**QNX proven:** current coherent source-bound journey above; [Nov8 wrong/correct/finish logs](../docs/acceptance/wrapper-20261108/NOTES.md) remain separately dated historical evidence.
**HOST only:** editable notebook, provenance/export checks and CI; these cannot certify your QNX edits or human learning.
**How to build:** [cold-reader codelab, prerequisites and exact commands](../codelab/codelab.md) — existing licensed SDK guest build → **STOP/REAP guest** → capped HOST QEMU, one lease.
No paid resources used. SSH/platform health and independent learner acceptance remain UNVERIFIED.

## Historical Nov13 SDK512 gate — OOM before native (superseded)

[Exact clean-stock receipt](../docs/acceptance/stock-20261113/NOTES.md): **BLOCKED_CLEAN_STOCK_IFS_OOM**. Fresh standard mkqnximage project, explicit512M/1CPU; only authored snippet added -device edu through verified QEMU_OPTIONS, no lesson/custom IFS integration. Guest killed PID1620 at329384KiB anon RSS during Generating ifs; IFS=0bytes, no bootable disk. HOST monitored peak1105190912bytes under enforced2GiB; swap0 and sampled HOST OOM events0. This was a guest memory failure, not a demonstrated HOST cap breach. SDK reaped, lease free. At that bounded SDK512 attempt the stock native gates were NOT_RUN. The later explicitly authorized SDK1GiB stock build and config-line finish above supersede this blocker; this failed receipt remains unchanged. Historical advanced source and receipts remain unchanged.

## Historical Nov10 feature gate: stopped at stock image build

[Measured bounded receipt](../docs/acceptance/features-20261110/NOTES.md): **BLOCKED_STOCK_MKIFS_OOM**. Own wrong-step3 source compiled and linked serially in the existing licensed SDK; stock platform image generation then OOM-killed a mkifs child (PID1617, anon RSS328616KiB). ifs.bin is zero bytes, not a bootable image. No HOST native run followed. Step6 compilation, new IRQ→private pulse→publication, bounded slog2 runtime capture and optional trace remain **NOT_RUN / UNVERIFIED**. Same caps; no swap/platform/package changes; SDK stopped/reaped and lease free. Historical Nov8 wrong/correct/finish receipts are unchanged, not proof of this new code. No new native PASS. Stop for independent owner review.

## Historical Nov9 single-host timeout

Historical Nov9 single-host **BLOCKED_NATIVE_TIMEOUT** ([receipt](../docs/acceptance/choice-a-20261109/receipt.json)); cause **UNVERIFIED**. No retries/tuning/cap increases.

## Start here: predict → edit → observe → diagnose → explain

**Advanced lab, not a turnkey browser exercise:** first read the [working stock prerequisite gate](../docs/learner-route.md). You need an existing licensed SDP, exclusive SDK/QEMU lease and the approved hashed IFS/disk handoff. No installation or bundled licensed artifacts.

Then follow the [one-notebook wrong → correct → finish checklist](../docs/coherent-journey.md). Create a notebook in the existing SDK shared mount, not an unrelated home directory:

```sh
export EDU_WORK="$EDU_SHARE/$EDU_CASE/own" # shared mount/case from canonical route
python3 scripts/learner_session.py init --work "$EDU_WORK"
# Open the printed $EDU_WORK/cockpit.html locally; notes stay private.
```

The generated notebook has persistent predictions, diagnosis, labeled split-host handoff commands
and private HOST notes export. A browser cannot execute shell commands;
import downloaded notes with the printed CLI. [Cockpit help](../docs/learner-cockpit.md). Follow the **[canonical learner route](../docs/learner-route.md)**: verify the existing licensed
SDK, controller, QEMU and approved stock artifact handoff; predict/edit step3, observe the wrong-write
failure, diagnose/fix/rebuild and explain it; then edit your own step6 starter
and observe normal write10/read3628800 through /dev/edu. Setup/build/run commands
and stop gates are integrated in order, not a scavenger hunt.
Do not start with make check-reference-step*: those are reference runs, never
your completion. Missing legal setup is BLOCKED, not solved by host checks.


[Evidence review](../REVIEW.md) audits claims and missing bindings. **Experimental native QNX components; not a production driver or human-validated tutorial.** Intended finish line: write 10 to /dev/edu and read 3628800 on QNX in QEMU. That normal-I/O finish line passed in the coherent journey at exact runtime source769a4c9; later documentation changes are not another native run; lifecycle robustness and independent human-learner acceptance remain unvalidated. No performance or functional evaluation of QNX is published here.

Canonical [capability ledger](../docs/capabilities.md): host checks, native compilation,
reference-run and learner-run are separate. [Fresh clean-platform step3](../docs/acceptance/clean-step3-20261107/native-clean/NOTES.md)
now records intended wrong-edit FAIL despite app exit 0, followed by corrected
native PASS. No reference receipt transfers.

## Recorded scope — 8 November 2026 (history)

Owner independent completion gate: **CONDITIONAL, receipt-inspected, not re-run**, at accepted tip ada5d0ff03533a2fec0983f3fedbd9bada9df8a9. That historical gate is not acceptance of the Nov8 upgrade. Nov8 ability-only and own-wrapper observations are source-bound; current provenance validation is offline. New council review remains pending. Existing licensed SDK reuse and owner-lab paths only; no fresh install, second SDK, human learner or platform-health validation. CANopy native evidence was not rerun. sshd internal cause UNVERIFIED; C6 FAIL / STOPPED; SocketCAN UNVERIFIED. The repository and tutorial are public; licensed artifacts and learner notes remain local.

Start only with the **[canonical learner route](../docs/learner-route.md)**. Its [supported-bootstrap receipts](../docs/acceptance/bootstrap-final-20261107/NOTES.md) bind wrong stage FAIL/app0, corrected PASS and own /dev/edu write10/read3628800 + IRQack. The startup failing component is sshd; internal cause remains UNVERIFIED. Historical setup/lesson pages are reference material, not alternative entry routes.

## Criteria map

| Criterion | Planned proof | Current evidence |
|---|---|---|
| Technical implementation | PCI attach, IRQ, resmgr on QNX | original diagnostic compiles; native BAR/ID/factorial, one-shot IRQ and 64-byte polled DMA observed; normal resmgr I/O PASS; robustness PENDING |
| Design | incremental, bounded checks | [codelab source](../codelab/codelab.md), [local site](../docs/site/index.html), explicit blocking framework |
| Impact | reproducible teaching without hardware | two clean-machine learner runs PENDING |
| Innovation | verified PCI/IRQ/DMA learning path | no novelty/first/smallest/correctness claim established |

## Maintainer host checks — not the learner route

Host, repository root (Python 3 and POSIX shell, GNU make):

```sh
./verify.sh --host-only
make check-reference-step1 # unchanged E1 reference; NOT learner acceptance
./verify.sh         # fresh native gate; BLOCKED without bundle + lease
```

Host mode runs guard and framework tests, then explicitly SKIPs live checks. Full verify and check-reference-step1 through check-reference-step6 can pass only on a fresh source/image-bound native reference boot with an authorized external bundle and exclusive lease. Missing inputs exit 2; make may report its own error status. make deploy is blocked and copies nothing. No DRYRUN pretends to build/deploy.

## Build environment

| Field | State |
|---|---|
| Foundation host | Ubuntu 24.04.5 LTS, ARM64 (aarch64) |
| KVM / QEMU / SDK | No KVM; QEMU 8.2.2 TCG; licensed SDK installed inside private x86 Linux guest |
| QNX SDP | 8.0 installed and verified; see docs/sdk-install-result-20261104.md |
| QSTI / QEMU | QSTI image pending; apt QEMU 8.2.2 Ubuntu1.18 verified |
| Target | QNX 8 boots under TCG; EDU BAR/ID/factorial, IRQ raise/wait/ack and 64-byte DMA round-trip observed |
| Toolchain | qcc -Vgcc_ntox86_64 compiled the original native/edu_probe.c with -Wall -Wextra -Werror |
| macOS / Windows | UNTESTED; no verified Docker path provided |
| Last live verification | 7 November 2026; all-six-step native functional PASS at 387ba38; QSTI provenance and fresh learners NOT verified |

## API scope — observed slices and unvalidated robustness

| Area | Planned evidence | file:function | Status |
|---|---|---|---|
| PCI server | attach/BAR/detach transcript | native/edu_probe.c:main | experimental BAR/polling observed; full lifecycle PENDING |
| IAT/InterruptWait | thread, INTx, ack, detach | native/edu_probe.c:main | one-shot raise/wait/ack PASS; robustness PENDING |
| Abilities/secpol | same ELF deny/IO0..0 allow | native/ability_lesson.c | ability-only observed; pathname policy BLOCKED; platform minimum UNVERIFIED |
| Resource manager | real /dev/edu I/O and errors | native/edu_resmgr.c and native/edu_accept.c | normal I/O PASS; lifecycle/policy PENDING |
| DMA | mask, transfer and IRQ evidence | native/edu_dma.h | 64-byte polled round-trip PASS; DMA IRQ/error injection PENDING |

Original native/edu_probe.c now uses installed QNX headers and compiles against libpci; it is an experimental diagnostic, not a resource manager or completed exercise. No QNX declarations, compatibility shims, fake target functions or made-up signatures are supplied. Starter/solution folders now contain readable E1-derived incremental C snapshots and bounded TODOs; see [E2 build order](../docs/e2-build-order.md). All twelve snapshots have [qcc compile-only evidence](../docs/acceptance/e2-qcc-20261107/receipt.json); the separately edited step3 BAR slice and one edited step6 normal-I/O finish have learner-run proof; other learner stages remain unverified. A source-pinned host behavioral model and transactional re-probe design tests are included in host/edu_model.py and tests/test_model.py. They are explicitly NOT QNX, do not perform MMIO/DMA, and cannot substitute for live checks.

## Release gates and limitations

See [verification checklist](../docs/verification-checklist.md), [host test evidence](../docs/test-results.md) and [learning notes](../docs/learning-notes.md). Every edu register must be verified against a live device in the pinned QEMU before any register tutorial or publication. Eight accessible SVG design diagrams, Mermaid sources, six rich starter/solution specifications, a local static site and host lifecycle tests are now available. Full SDK/API review, actual secpol, production driver/resmgr, DMA IRQ/error injection/restart/trace, independent human learner and second-SDK validation remain UNVERIFIED. A [public demo video](https://youtu.be/hI8-QtwMg8A) is available; it does not expand the receipt-backed acceptance scope. No 45-minute completion claim is validated.

CI is host-only, not Stage-1 QNX acceptance. CI downloads no QEMU, SDK or target image. Local owner-authorized feasibility testing used apt QEMU and official checksum-verified Alpine Linux artifacts outside this repository; see [TCG feasibility](../docs/tcg-feasibility.md). A licensed SDK and private target image now exist outside this repository; neither is redistributed. Redistribution guard scans ignored/untracked files, names, signatures and selected markers; it is conservative, not a complete licence/content detector. SDKs, binaries, archives and images must stay outside this repo (also outside ignored folders). Python stdlib only; no dependencies are installed.

## Credit and licence

Original foundation under [Apache-2.0](../LICENSE). QEMU edu documentation/source are the proposed future register-reference authority, not live proof: https://www.qemu.org/docs/master/specs/edu.html and https://gitlab.com/qemu-project/qemu/-/blob/master/hw/misc/edu.c (unpinned references; source not vendored). QNX 8.0 local documentation must govern API implementations. No upstream code or SDK content is copied. The host model pins QEMU source by commit and checksum; see [register evidence](../docs/register-evidence.md). The failed sysfs probe was superseded by actual QEMU qtest register, factorial, INTx and DMA experiments. See the row ledger: QEMU device behavior is verified, NOT QNX APIs.

The repository and tutorial are public. [Watch the demo](https://youtu.be/hI8-QtwMg8A). This documentation update does not authorize Pages deployment, upstream PRs, account creation, submission or spending.

## Companion/reference material — not alternative learner entry routes

- [Write your first QNX 8.0 PCI driver in QEMU](../docs/write-first-qnx8-pci-driver-qemu.md): published companion reference, real build/crash-diagnostic checkpoint and observed BAR/IRQ/polled-DMA/resource-manager checkpoints and remaining learner gates.

- [Static site design and rendering](../docs/site-design.md): dependency-free, relative links, nothing published.
- [Policy specification](../docs/security-policy.md): not validated secpol syntax.
- [Restart/re-probe contract](../docs/restart-policy.md): host design model, not target recovery.
- [Eight diagram sources](../docs/diagrams/environment.mmd) and [learning support](../docs/learning-notes.md).

Host · repository root: run python3 scripts/render_site.py, then open docs/site/index.html.
For stale-output checking use python3 scripts/render_site.py --check. Actual pinned upstream claat export is separately verified; see [export scope](../docs/claat-export.md). This local renderer does not claim to be claat.

### Scoped learner /dev/edu result — 7 November 2026

Edited step6 starter on the same fresh stock generic platform passed actual normal write/read10→3628800 and IRQ completion/ack. Source, binary, image, disk and caps are bound in the [learner finish evidence](../docs/acceptance/learner-finish-clean-20261107/NOTES.md). No reference checker, host result injection or polling fallback. Earlier failures remain; startup Memory fault still excludes a healthy-SSH/all-platform claim. Owner completion review is CONDITIONAL, receipt-inspected not re-run; no safety/timing acceptance; C6 stays STOPPED.

Supported stock-platform helper and explicit split-host/no-swap-change/exclusive-lease prerequisites are in the [canonical route](../docs/learner-route.md). Existing installed SDK reuse only; no installer or second-SDK claim. The [public demo video](https://youtu.be/hI8-QtwMg8A) complements the tutorial; the linked receipts remain the authority for native results.

Supported canonical route observed on one existing licensed SDK: [supported-bootstrap result](../docs/acceptance/bootstrap-final-20261107/NOTES.md). Fresh stock platform, wrong stageFAIL/app0, correctedPASS and own /dev/edu write10/read3628800+IRQack. Automated reuse only, not a second SDK or human gate. Old missing-host-SDK negative preserved. All guests reaped; no platform-health claim.
