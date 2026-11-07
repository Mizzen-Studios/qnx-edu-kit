# Local learner-loop acceptance, 2026-11-07

Final native proof: wrong host status 1, corrected host status 0; both actual
application status 0. Nine focused host tests pass; redistribution guard passes.

Chronology (preserving the intermediate failure):
- At learner-source commit fece074, full host discovery ran 74 tests: 71 passed, 2 skipped, 1 stale-site-render error. The original host-tests.log retains that failure.
- Parent integration at 81397e1 regenerated the local site and reran all 74 tests: **72 passed, 2 skipped, 0 failures**. See parent-review.json for that final integration receipt. A further local-link regression during integration was corrected before that final green run; no native receipt was changed or promoted.
- This reconciles host/site results only. Native wrong/correct observations below retain their original scope; host tests do not create fresh target or human learner validation.

These are fresh-build/fresh-boot observations, not imported reference completion.
The C snapshots are original application source, derived by completing the step3
starter using the supplied solution as guidance, adding actual volatile MMIO
read-back output and validating a full 0x1000-byte mapped extent.

The wrong edit deliberately writes 0x12345679 and incorrectly accepts its
complement 0xedcba986. It compiles, exits zero and even prints the application
STEP3 PASS. The independent stage oracle must nevertheless return host status 1
because the assigned challenge is 0x12345678 -> 0xedcba987. This demonstrates why
application PASS alone is insufficient. The corrected edit changes those two
constants; see fix.diff. Both exact source snapshots are retained here.

The SDK build guest used the existing licensed installation, serialized by the
same /home/ubuntu/qnx-host/native-test.lock used across the native runs. It was
stopped and its foreground process collected before native QEMU started.
All QEMUs: effective CPU 100000/100000, memory 1073741824, nice 15; guest 1 vCPU,
512 MiB. No C6/safestop execution. No IRQ/DMA or resource-manager learner claims.

Portability limitation: the local images were separately rebuilt using an
external adaptation of the existing custom E1 BSP buildfile/startup and external
boot disk. A private --strip-debug copy of the licensed relocatable kernel
reduced mkifs memory enough for the fixed 512 MiB SDK guest; no SDK originals
were edited. That substrate is NOT distributed. The checked-in build script accepts
a learner's licensed SDP environment and BSP paths, and the original application
fragment documents integration, but a clean learner-owned BSP integration has not
been executed. No QSTI provenance, malicious-output resistance or hardware claim.

Raw boots also show a pre-learner "Memory fault (core dumped)" after the
substrate SSH startup. This does not prevent PCI/MMIO learner execution; no SSH
health/continuity claim is made. The initial corrected run was rejected by an
oracle bug expecting "QNX 8.0 " rather than actual "QNX 8.0.0 "; its raw receipt
is preserved as correct-initial-oracle. The version matcher and regression test
were corrected, then BOTH negative and positive were freshly booted again.

The target exit status and host stage status differ intentionally for the bad
case. The systemd/QEMU wrapper is stopped after completion, so its signal return
status is not the target application's status.
