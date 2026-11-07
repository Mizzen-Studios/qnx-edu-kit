# Clean step3 bounded attempt — 7 November 2026

**Historical attempt record.** Subsequent owner-authorized [guest-swap stock build](swap-attempt/NOTES.md) completed, followed by [fresh clean wrong/correct native step3 proof](native-clean/NOTES.md). The failure text below describes earlier attempts; original raw receipts and diagnosis900 remain unchanged.

**BLOCKED: fresh unmodified generic image generation did not complete within the
240-second builder limit. Portability UNVERIFIED; native negative/corrected runs
NOT_RUN.** No E1 image/buildfile/owner bundle/stripped kernel was used.

## Previous milestone chronology

The initial 240-second result below is preserved, not the final diagnosis. The [focused fresh-directory 900-second attempt](diagnosis900/NOTES.md) established guest OOM killing the stock kernel linker before timeout. Portability remains UNVERIFIED; no clean native assessments ran. Original raw logs/JSON remain unchanged.

## Actual work and evidence

- Original narrow platform instructions: docs/clean-step3-setup.md. Read-only
  preflight: scripts/learner_clean_preflight.py. Existing stage oracle untouched.
- Inspected existing external licensed SDP/BSP inside the x86_64 Ubuntu SDK VM:
  installed-inventory.log and installed-pci-layout.log. Generic BSP archive exists;
  SDK qcc, mkifs, mkqnximage, startup/kernel and PCI components found. No missing
  licensed installation is asserted. No login/install/download/activation change.
- Initial preflight incorrectly expected usr/sbin and usr/lib: blocked exit 2
  before building. Preserved preflight-initial.json and attempt-initial.log.
  Follow-up lookup found actual QNX 8 sbin and lib layout. Fixed probe with host
  regression; preflight.json then passed prerequisites, never native acceptance.
  locate-initial-failure.log preserves one malformed find command; narrower retry
  succeeded. Inventory caller timed out at 360s during slow boot, but its queued
  read-only job subsequently finished exit 0 and its complete output was collected.
- Fresh wrong.c and correct.c were edited from starter TODO, no cached binaries.
  Both actual qcc invocations succeeded; source/binary SHA256 in compiler.json and
  build.log. Wrong variant deliberately accepts its own complement and exits 0,
  leaving stage oracle to reject wrong write/read. No execution claim is made.
- A new /home/qnx/clean-step3-20261107 platform directory was generated from the
  installed generic mkqnximage tooling. Command in attempt-driver.sh:
  timeout --kill-after=10 240 mkqnximage --type=qemu --arch=x86_64 --build.
  No --run. It generated build/startup files and system/data partition phases,
  reached "Generating ifs . . .", then reported "cc: caught signal: 15".
  The final diagnostic found output/ifs.bin **zero bytes**, no disk.raw and no
  remaining builder/timeout processes. Generated proprietary text was not copied
  to Git; only hashes/sizes are in build-final-state.log.
- The queue's .rc for that terminated build was not delivered, although a later
  diagnostic completed exit 0 and confirmed no builder remained. Thus do not
  invent a build exit 124/OOM conclusion: observed failure is bounded termination
  during IFS generation, not a demonstrated OOM. Raw original log stays external;
  build.log removes only routine QNX_HOST/QNX_TARGET/MAKEFLAGS environment lines.
- No target image/disk existed for learner_lab.py build/run, so source-bound
  negative stageFAIL despite appPASS and corrected stagePASS cannot be assessed.
  No previous E1 acceptance was reused to fill the gap.

## Caps, checks and cleanup

SDK launched under actual shared flock /home/ubuntu/qnx-host/native-test.lock,
with no other QEMU. sdk-caps.json records actual CPU 100000/100000, memory
1073741824, nice 15, guest 1 vCPU/512 MiB. Caps were never increased. No target
QEMU was launched. Stop/reap and free-lock confirmation: sdk-stop.json.

Focused learner tests: 14 PASS (host-tests.log). Full intermediate suite: 78
cases, 75 PASS, 2 skip, 1 packaging ERROR because new docs/receipt need parent-owned
site regeneration (full-host-tests.log). Parent owns site; this worker did not
render/change it. Redistribution guard PASS after moving an ignored generated
check_no_sdk bytecode cache outside checkout (the cache self-matched its own
conservative marker constants); no guard semantics changed. git diff --check PASS.

## Exact remaining prerequisite

A successfully generated **fresh unmodified licensed generic boot IFS and matching
disk within the authorized caps/bounded run** is absent. Before native validation,
the documented fresh snippet integration/PCI-ready startup also needs actual
execution. This slice stops here; no larger caps, private kernel stripping,
licensing/package changes or automatic retry. C6 remains STOPPED, no heartbeat,
DMA/IRQ/secpol/resmgr/course expansion, publication, contacts or spend.

## Final parent host integration

After acceptance-note rendering/link repair and the final QNX8-layout preflight regression, a detached clean checkout at d419bce01d35d3c92ed55b80b7f9faa854cb6ca3 ran ./verify.sh --host-only: 79 total, **77 PASS / 2 SKIP / 0 failures**, exit0, checkout unchanged. parent-review.json pins the exact source tree, raw parent-host-final.log and inspected compile/OOM/cleanup evidence. This supersedes only intermediate host/site failures, never the clean native bootstrap blocker. No native boot or portable acceptance inferred.
