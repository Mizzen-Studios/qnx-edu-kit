# edu-kit — learner-owned QNX fault-to-fix lab

Private development milestone. [Private evidence review](REVIEW.md) audits claims and missing bindings. **Experimental native QNX components; not a production driver or fully reproduced learner tutorial.** Intended finish line: write 10 to /dev/edu and read 3628800 on QNX in QEMU. That normal-I/O finish line now passes on the native target; lifecycle/learner acceptance remains pending. No performance or functional evaluation of QNX is published here.

Canonical [capability ledger](docs/capabilities.md): host checks, native compilation,
reference-run and learner-run are separate. [Fresh clean-platform step3](docs/acceptance/clean-step3-20261107/native-clean/NOTES.md)
now records intended wrong-edit FAIL despite app exit 0, followed by corrected
native PASS. No reference receipt transfers.

**Clean path demonstrated on one pinned configuration; owner gate not independently reassessed.**
[Setup](docs/clean-step3-setup.md): unmodified stock generic kernel, 512 MiB SDK guest
plus 1 GiB disk-backed guest swap, unchanged 100% CPU / 1 GiB host / nice 15 caps.
The prior OOM receipts remain preserved. Both native logs retain an unattributed
startup Memory fault after Starting sshd: no healthy-SSH/all-services claim.
Broad portability and human learner validation remain UNVERIFIED.
The distinct [learner /dev/edu finish](docs/learner-dev-edu.md) has one scoped normal-I/O result, not independent learner acceptance.

## Criteria map

| Criterion | Planned proof | Current evidence |
|---|---|---|
| Technical implementation | PCI attach, IRQ, resmgr on QNX | original diagnostic compiles; native BAR/ID/factorial, one-shot IRQ and 64-byte polled DMA observed; normal resmgr I/O PASS; robustness PENDING |
| Design | incremental, bounded checks | [codelab source](codelab/codelab.md), [local site](docs/site/index.html), explicit blocking framework |
| Impact | reproducible teaching without hardware | two clean-machine learner runs PENDING |
| Innovation | verified PCI/IRQ/DMA learning path | no novelty/first/smallest/correctness claim established |

## Host-only quick start

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

## API acceptance (not yet passed)

| Area | Planned evidence | file:function | Status |
|---|---|---|---|
| PCI server | attach/BAR/detach transcript | native/edu_probe.c:main | experimental BAR/polling observed; full lifecycle PENDING |
| IAT/InterruptWait | thread, INTx, ack, detach | native/edu_probe.c:main | one-shot raise/wait/ack PASS; robustness PENDING |
| Abilities/secpol | deny/allow and least privilege | native/edu_resmgr.c and native/edu_accept.c | normal I/O PASS; lifecycle/policy PENDING |
| Resource manager | real /dev/edu I/O and errors | native/edu_resmgr.c and native/edu_accept.c | normal I/O PASS; lifecycle/policy PENDING |
| DMA | mask, transfer and IRQ evidence | native/edu_dma.h | 64-byte polled round-trip PASS; DMA IRQ/error injection PENDING |

Original native/edu_probe.c now uses installed QNX headers and compiles against libpci; it is an experimental diagnostic, not a resource manager or completed exercise. No QNX declarations, compatibility shims, fake target functions or made-up signatures are supplied. Starter/solution folders now contain readable E1-derived incremental C snapshots and bounded TODOs; see [E2 build order](docs/e2-build-order.md). All twelve snapshots have [qcc compile-only evidence](docs/acceptance/e2-qcc-20261107/receipt.json); the separately edited step3 BAR slice and one edited step6 normal-I/O finish have learner-run proof; other learner stages remain unverified. A source-pinned host behavioral model and transactional re-probe design tests are included in host/edu_model.py and tests/test_model.py. They are explicitly NOT QNX, do not perform MMIO/DMA, and cannot substitute for live checks.

## Release gates and limitations

See [verification checklist](docs/verification-checklist.md), [host test evidence](docs/test-results.md) and [learning notes](docs/learning-notes.md). Every edu register must be verified against a live device in the pinned QEMU before any register tutorial or publication. Eight accessible SVG design diagrams, Mermaid sources, six rich starter/solution specifications, a local static site and host lifecycle tests are now available. Full SDK/API review, actual secpol, production driver/resmgr, DMA IRQ/error injection/restart/trace, two fresh target learner runs and mandatory on-QNX capture remain PENDING. No 45-minute completion claim is validated.

CI is host-only, not Stage-1 QNX acceptance. CI downloads no QEMU, SDK or target image. Local owner-authorized feasibility testing used apt QEMU and official checksum-verified Alpine Linux artifacts outside this repository; see [TCG feasibility](docs/tcg-feasibility.md). A licensed SDK and private target image now exist outside this repository; neither is redistributed. Redistribution guard scans ignored/untracked files, names, signatures and selected markers; it is conservative, not a complete licence/content detector. SDKs, binaries, archives and images must stay outside this repo (also outside ignored folders). Python stdlib only; no dependencies are installed.

## Credit and licence

Original foundation under [Apache-2.0](LICENSE). QEMU edu documentation/source are the proposed future register-reference authority, not live proof: https://www.qemu.org/docs/master/specs/edu.html and https://gitlab.com/qemu-project/qemu/-/blob/master/hw/misc/edu.c (unpinned references; source not vendored). QNX 8.0 local documentation must govern API implementations. No upstream code or SDK content is copied. The host model pins QEMU source by commit and checksum; see [register evidence](docs/register-evidence.md). The failed sysfs probe was superseded by actual QEMU qtest register, factorial, INTx and DMA experiments. See the row ledger: QEMU device behavior is verified, NOT QNX APIs.

Repository stays private. No Pages, upstream PR, video, account creation, submission or spending is authorized by this milestone.

## Local learning materials

- [Write your first QNX 8.0 PCI driver in QEMU](docs/write-first-qnx8-pci-driver-qemu.md): expanded private draft, real build/crash-diagnostic checkpoint and observed BAR/IRQ/polled-DMA/resource-manager checkpoints and remaining learner gates.

- [Static site design and rendering](docs/site-design.md): dependency-free, relative links, nothing published.
- [Policy specification](docs/security-policy.md): not validated secpol syntax.
- [Restart/re-probe contract](docs/restart-policy.md): host design model, not target recovery.
- [Eight diagram sources](docs/diagrams/environment.mmd) and [learning support](docs/learning-notes.md).

Host · repository root: run python3 scripts/render_site.py, then open docs/site/index.html.
For stale-output checking use python3 scripts/render_site.py --check. Actual pinned upstream claat export is separately verified; see [export scope](docs/claat-export.md). This local renderer does not claim to be claat.

### Scoped learner /dev/edu result — 7 November 2026

Edited step6 starter on the same fresh stock generic platform passed actual normal write/read10→3628800 and IRQ completion/ack. Source, binary, image, disk and caps are bound in the [learner finish evidence](docs/acceptance/learner-finish-clean-20261107/NOTES.md). No reference checker, host result injection or polling fallback. Earlier failures remain; startup Memory fault still excludes a healthy-SSH/all-platform claim. No independent re-review or safety/timing acceptance; C6 stays STOPPED.
