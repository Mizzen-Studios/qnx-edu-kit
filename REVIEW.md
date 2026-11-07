# Private capability review — 7 November 2026

## Current completion gate — 20:03 UTC

Owner independent completion gate: **CONDITIONAL, receipt-inspected, not re-run**, at accepted tip ada5d0ff03533a2fec0983f3fedbd9bada9df8a9. This packaging follow-up does not rerun native evidence or broaden acceptance. Existing licensed SDK reuse and owner-lab paths only; no fresh install, second SDK, human learner or platform-health validation. CANopy native evidence was not rerun. sshd internal cause UNVERIFIED; C6 FAIL / STOPPED; SocketCAN UNVERIFIED. Everything private.


Historical initial offline inspection of EDU e9174bd73412c98fcf17b40a9e5b6d931ebc4dec. No guest, SDK, QEMU, network runtime, demo or native work performed. No publication.
[Detailed appendix](docs/review/appendix.json) covers every nonempty line in README, STATUS, codelab and all site source pages, generated HTML projections, exact receipt/log SHA-256s and every receipt hash field. Candidate line mappings are NOT blanket acceptance: this bounded catalog governs. Archival commits are NOT tested commits.

## Bounded claim catalog

Receipt IDs resolve to exact paths/full hashes in the appendix; missing bindings remain UNVERIFIED.

| Capability claims, including expected markers and design instructions | Label and exact scope |
|---|---|
| E1 QNX process, PCI attach/BAR/ID/complement, factorial10, one-shot IAT raise/wait/ack,64-byte polled DMA, normal resmgr/shell/client error/read checks | **observed in this QEMU run**: reference and reference-clean, complete serial/verify logs. Four source hashes and image 7f23eb12551cd6b093c6de5d52fb66941c35f5b6f9d3e7468d087f1e02844d4c. Tested commit, ELF and disk bindings **UNVERIFIED in receipts**; STATUS associates 387ba38ce696c92bb3d8332ea7f01d5a0630cbfc, not receipt proof. No DMA-IRQ/lifecycle/general API correctness transfer. |
| Twelve E2 starter/solution compilations; qcc/build instructions | Compilation only: compile and raw compile log; appendix extracts all12 ELF hashes. Twelve source hashes present; tested commit **UNVERIFIED**, archived at 2d436b91aa4bd5b0f9492efcb22fe92af87e0fe2. Solutions Werror; starter warnings retained. No per-snapshot runtime claim. |
| Stock generic build,512MiB RAM+1GiB guest swap, isolated builder and queue snapshot | Observed SDK build only: stock-build and raw build/service/queue logs. IFS/disk hashes present; tested commit **UNVERIFIED**. Queue snapshot is not an availability guarantee. |
| Wrong-edit rejected despite application PASS/exit0; corrected BAR edit accepted at slot5 | **observed in this QEMU run**: step3-wrong and step3-correct, corresponding raw logs. Exact source/ELF/IFS/disk hashes present; tested repository commit **UNVERIFIED**. Archived source is not a tested-commit binding. |
| One edited step6 real write10/read3628800, IRQ completion/ack0 | **observed in this QEMU run**: finish → docs/acceptance/learner-finish-clean-20261107/unmasked/native.json and native.log. Source 42b3cc31935090db26140c62b67a0dd3f7998f81ab226a3103b2ad9df8b9a965; ELF 0253b89fa66aa171418f8ba496ec9a57a1e4c600fb770901cba3f5b54b2f0c40; IFS a48335ec842c824d52bb2c713365e7afcf0ae8ec259369f3c20c0c723eccec2b; disk 64db806fb1307b5cb4b3b8451c35427e39c65ff55c0db63f284b2398db82bb03. Tested commit **UNVERIFIED**; source archived at 03fcadd7dedb7d80fdacf1975614f6678ebc3f9c. Root manifest is an earlier failure, not success. Daemon termination143 is not graceful-stop proof. |
| Caps, serialization, stability and reaping for learner runs | **observed in this QEMU run**: individual receipts/checks/commands. CPU100000/100000,memory1073741824,nice15;1vCPU/512MiB. Historical snapshots, not current process state or timing/availability proof. |
| Models, guard, blocked live/deploy paths, source contracts, tests, static pages, diagrams, incremental sources | **host-only**: host binds cec75567bfd65f02b4afb3ebb674ffe5116906d8,83total/81pass/2skip and raw log; old-host pins historical79total. Current repo/host tests establish packaging/design only. Guard conservative, not complete detection. No MMIO/target transfer. |
| Upstream claat export,6 steps/12 sources/8SVG/local links | **host-only**: export pins tool/source hashes; tested commit **UNVERIFIED**. Appendix compares current codelab source hash. Not browser, hosting, offline, privacy or external-service availability acceptance. Local renderer is distinct; site inherits source limits. |
| QEMU register/INTx/DMA reference behavior | **observed in this QEMU run**, NOT QNX: qtest raw log records executable/probe hashes and BASE 7afd82275940f45e0b0b0105205a58c255cb713c. Distro executable not proven identical to upstream source pin. API walkthroughs are instructions/design unless supported by narrow native claims above. |
| SDP installation/version, host identity/KVM/environment/hello history | Installation narrative docs/sdk-install-result-20261104.md and feasibility pages; underlying external SDK logs not inspected here. Exact install/host identity/activation/hello bindings **UNVERIFIED** in this packet. QSTI provenance **UNVERIFIED**; macOS/Windows untested. |
| Teaching impact, portability, full learner journey,44/45-minute completion, novelty/first/smallest, full lifecycle, DMA IRQ/errors/restart/trace, least privilege/secpol, physical hardware/production correctness | **UNVERIFIED**: estimates/plans/source contracts, no qualifying receipts. No capability promotion. |
| Startup Memory fault origin; healthy SSH/platform | Fresh unchanged baseline reproduced; separately traced image attributes process to **sshd**, with sshd.core/no sshd in pidin. Internal root cause and healthy-SSH/platform **UNVERIFIED**. See docs/acceptance/startup-diagnosis-20261107/NOTES.md. |
| C6 safety/heartbeat and SocketCAN | **UNVERIFIED**. C6 **STOPPED, no retries**. SocketCAN ABI historically failed; no EDU receipt establishes SocketCAN. No safety, timing or availability claims. |

## Corrections and chronology

Softened README stale “only step3”/“next assessment”; corrected stale claat compile-pending wording and current IAT versus historical event description. Missing tested-commit/ELF/disk/install bindings above must remain explicit or be removed from any future unqualified summary.

Preserved: failed Linux sysfs probe; E1 privilege/crash diagnostics; adapted E1/stripped-kernel learner history; initial240s inconclusive build; oom global linker OOM (normal exit null); successful swap build; all learner IRQ failures before unmasked success; host packaging failures. Historical STATUS “No /dev/edu learner PASS” applies to its earlier milestone only. No failure receipt rewritten and no broader causal/safety inference.

## Host-only recheck

Run ./verify.sh --host-only, python3 tools/capability_ledger.py, python3 scripts/render_site.py --check, python3 docs/review/build_packet.py --check. Current validation: docs/review/validation.json. Never run live commands for this review.

## Fresh-checkout follow-up (automated, not independent human review)

See [new source-commit-bound receipts](docs/acceptance/fresh-checkout-20261107/NOTES.md) and provenance.json: wrong host1/correct host0, initial finish host1/corrected finish host0 on a freshly generated stock platform using existing legal SDK. Older missing bindings remain UNVERIFIED; no retrospective promotion. Startup process now attributed to sshd only in separately bound diagnostic image. Owner completion re-review subsequently completed conditionally; see current gate above.

Private editorial draft: [shot list and narration](docs/private-demo.md), planned below three minutes. No recording/upload or new runtime claim.

## Canonical route follow-up — host-only, native feature freeze

README/site and codelab now lead with the integrated predict → edit → observe →
diagnose → explain route: step3 then learner-owned /dev/edu. Six historical
lessons are reference appendix material. Exact commands/instruction hashes and
independent-workdir results: docs/acceptance/route-paths-20261107/receipt.json.
Unavailable legal SDK/BSP inputs on that independent host remain BLOCKED, not
PASS. No guest/native rerun, SDK install/activation, second-SDK portability,
human acceptance or runtime proof promotion. Historical failures/pins unchanged.
The historical claat source no longer matches current instructions; its original
receipt stays unchanged. A separate current host export receipt binds the new prose.

## Council conditional gate and dry capture readiness

Council re-review at01060c7c1aff834d6c0b016de7fd9f988f8f7e35 conditionally accepts only scoped recorded evidence; native features FROZEN. Earlier references to an independent review still pending describe their dated milestones. Human learning/second independent SDK remain UNVERIFIED. Historical route-path receipt checked instructions at3a4821b, host-only: missing legal SDK/BSP/buildfile/disk is BLOCKED, not native/portability PASS.

Historical 17:08 dry pack docs/proof-capture/SCRIPT.md mapped every narration line to a bounded REVIEW claim, exact frozen01060c7 files and planned frame;211words/160planned seconds. No recording/audio without separate Olly OK. Evidence pins/failures preserved, no native feature/tests expansion, no C6/sshd cause chase/heartbeat. Conditional acceptance is not full-platform health, safety, timing or availability acceptance. Structural lint/report does not certify arbitrary prose semantics.

Supported stock-platform helper and explicit split-host/swap/isolated-service prerequisites are in the [canonical route](docs/learner-route.md). Existing installed SDK reuse only; no installer or second-SDK claim. Videos deferred until final freeze, final verification, independent gate and separate Olly OK; not a current blocker.

Supported canonical route observed on one existing licensed SDK: [supported-bootstrap result](docs/acceptance/bootstrap-final-20261107/NOTES.md). Fresh stock platform, wrong stageFAIL/app0, correctedPASS and own /dev/edu write10/read3628800+IRQack. Automated reuse only, not a second SDK or human gate. Old missing-host-SDK negative preserved. All guests reaped; no platform-health claim.

## Current private packet binding

REVIEW appendix and lightweight demo asset binding: ada5d0ff03533a2fec0983f3fedbd9bada9df8a9, the exact conditionally accepted completion tip. recorded: false. Historical runtime source/ELF/image/disk pins are not rewritten. The bootstrap-final receipts supersede the earlier missing-host-SDK result for the tested existing-SDK owner-lab route only. No new installation, second SDK, human validation or full-platform health claim.
