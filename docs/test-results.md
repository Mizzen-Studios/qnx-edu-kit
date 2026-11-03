# Host verification evidence — 2026-11-03

Host only: Ubuntu ARM64, Python 3.12.3, GNU make 4.3. QEMU 8.2.2 TCG installed;
Linux boot/PCI enumeration observed, ZERO register rows verified; QNX never run.
No SDK/QSTI, target driver, secpol validation, physical DMA or target restart proof.

## Current repeatable checks

- ./verify.sh --host-only: exit 0; redistribution guard PASS, 36 tests PASS,
  six live checks explicitly SKIP. No third-party Python dependencies.
- ./verify.sh: exit 1; all six live steps BLOCKED after host tests.
- make check-step1 through check-step6: each exit 2, BLOCKED.
- make deploy: exit 2; nothing copied.
- python3 scripts/render_site.py --check: exit 0.
- git diff --check: clean.

Tests: 11 foundation/guard/gate tests, 14 initial source-pinned model/lifecycle
tests, 7 packaging/link/diagram tests, 4 independent-review regression tests.
Eight accessible SVG designs and matching Mermaid sources are present. These
are contracts, not target execution diagrams. claat and Go absent; local static
renderer tested, upstream claat export unverified. No Pages publication.

## Two fresh-agent HOST packaging checks

Independent collector agents followed README/codelab host commands read-only.
Both observed 32 tests passing before review fixes, host-only exit 0, full verify
exit 1 and blocked target checks. First agent independently audited 27 HTML pages,
121 local href/src references, 26 Markdown sources and 54 local links, no broken
links. This is NOT two clean-machine QNX learner runs or visual browser QA.

Second review found model integer-validation, owned-IRQ and endpoint-publication
issues, plus stale evidence text. Fixed with four regression tests: reject bool/
fraction DMA inputs; preserve unowned IRQ bits; explicitly separate endpoint
acquisition from publication; publish only after owned-status drain. Updated
current results are 36 tests, not a retroactive claim about original reviews.

## Target release blockers

Actual SDP build/version and QSTI provenance, real QNX build and boot, six target
implementations/checks, deployment path, register-row live evidence, policy deny/
allow tests, DMA/IST/resmgr/restart/trace evidence, two full clean learner runs,
non-Linux host path and mandatory on-QNX capture. No durations or benchmark
claims measured. Linux mmap-helper/toolchain work is an independent next step,
not an SDK-only blocker; see register-evidence.md.
