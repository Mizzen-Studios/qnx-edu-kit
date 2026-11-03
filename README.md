# edu-kit — teaching kit for QNX® 8.0

Private, SDK-independent milestone. **Not a working QNX driver or a runnable tutorial.** Intended finish line: write 10 to /dev/edu and read 3628800 on QNX in QEMU. That finish line has not been demonstrated. No performance or functional evaluation of QNX is published here.

## Criteria map

| Criterion | Planned proof | Current evidence |
|---|---|---|
| Technical implementation | PCI attach, IRQ, resmgr on QNX | BLOCKED; no target code |
| Design | incremental, bounded checks | [codelab source](codelab/codelab.md), [local site](docs/site/index.html), explicit blocking framework |
| Impact | reproducible teaching without hardware | two clean-machine learner runs PENDING |
| Innovation | verified PCI/IRQ/DMA learning path | no novelty/first/smallest/correctness claim established |

## Host-only quick start

Host, repository root (Python 3 and POSIX shell, GNU make):

```sh
./verify.sh --host-only
make check-step1    # intentionally BLOCKED, nonzero
./verify.sh         # intentionally BLOCKED, nonzero
```

Host mode runs guard and framework tests, then explicitly SKIPs six live checks. Full verify never returns success in this milestone. Each check-step1 through check-step6 exits 2; make may report its own error status. make deploy is blocked and copies nothing. No DRYRUN pretends to build/deploy.

## Build environment

| Field | State |
|---|---|
| Foundation host | Ubuntu 24.04.5 LTS, ARM64 (aarch64) |
| KVM / QEMU / SDK | No KVM; installed QEMU 8.2.2 TCG + user emulation; SDK pending |
| QNX SDP | 8.0 intended; build ID PENDING, not installed |
| QSTI / QEMU | QSTI image pending; apt QEMU 8.2.2 Ubuntu1.18 verified |
| Target | x86_64 Linux TCG boot verified; QNX has not booted here |
| Toolchain | qcc target selection PENDING local SDK confirmation |
| macOS / Windows | UNTESTED; no verified Docker path provided |
| Last live verification | NEVER |

## API evidence (none yet)

| Area | Planned evidence | file:function | Status |
|---|---|---|---|
| PCI server | attach/BAR/detach transcript | not implemented | BLOCKED |
| IAT/InterruptWait | thread, INTx, ack, detach | not implemented | BLOCKED |
| Abilities/secpol | deny/allow and least privilege | not implemented | BLOCKED |
| Resource manager | real /dev/edu I/O and errors | not implemented | BLOCKED |
| DMA | mask, transfer and IRQ evidence | not implemented | BLOCKED |

No QNX declarations, compatibility shims, fake target functions or made-up signatures are supplied. Starter/solution folders currently contain task/acceptance specifications, not compilable exercises. A source-pinned host behavioral model and transactional re-probe design tests are included in host/edu_model.py and tests/test_model.py. They are explicitly NOT QNX, do not perform MMIO/DMA, and cannot substitute for live checks.

## Release gates and limitations

See [verification checklist](docs/verification-checklist.md), [host test evidence](docs/test-results.md) and [learning notes](docs/learning-notes.md). Every edu register must be verified against a live device in the pinned QEMU before any register tutorial or publication. Eight accessible SVG design diagrams, Mermaid sources, six rich starter/solution specifications, a local static site and host lifecycle tests are now available. SDK review, actual secpol, all target code, live DMA/restart/trace, upstream claat export, two fresh target learner runs and mandatory on-QNX capture remain PENDING. No 45-minute completion claim is validated.

CI is host-only, not Stage-1 QNX acceptance. CI downloads no QEMU, SDK or target image. Local owner-authorized feasibility testing used apt QEMU and official checksum-verified Alpine Linux artifacts outside this repository; see [TCG feasibility](docs/tcg-feasibility.md). No QNX SDK/image has been downloaded. Redistribution guard scans ignored/untracked files, names, signatures and selected markers; it is conservative, not a complete licence/content detector. SDKs, binaries, archives and images must stay outside this repo (also outside ignored folders). Python stdlib only; no dependencies are installed.

## Credit and licence

Original foundation under [Apache-2.0](LICENSE). QEMU edu documentation/source are the proposed future register-reference authority, not live proof: https://www.qemu.org/docs/master/specs/edu.html and https://gitlab.com/qemu-project/qemu/-/blob/master/hw/misc/edu.c (unpinned references; source not vendored). QNX 8.0 local documentation must govern API implementations. No upstream code or SDK content is copied. The host model pins QEMU source by commit and checksum; see [register evidence](docs/register-evidence.md). A real Linux MMIO attempt failed; no register row is claimed live verified.

Repository stays private. No Pages, upstream PR, video, account creation, submission or spending is authorized by this milestone.

## Local learning materials

- [Static site design and rendering](docs/site-design.md): dependency-free, relative links, nothing published.
- [Policy specification](docs/security-policy.md): not validated secpol syntax.
- [Restart/re-probe contract](docs/restart-policy.md): host design model, not target recovery.
- [Eight diagram sources](docs/diagrams/environment.mmd) and [learning support](docs/learning-notes.md).

Host · repository root: run python3 scripts/render_site.py, then open docs/site/index.html.
For stale-output checking use python3 scripts/render_site.py --check. Upstream claat is unavailable; this local renderer does not claim to be claat.
