# Bounded existing-environment single-host attempt — 8 November 2026

Outcome: **BLOCKED**, not silent acceptance. The actual existing licensed x86_64
Linux SDK host was booted once under the sole native lease. The original queued
read-only capability job completed rc2. SDK environment, qcc/mkifs/mkqnximage and
four required installed target components PASS. That same host has no executable
QEMU at command-v or the three explicitly checked existing locations, and its
licensed user's systemd --user bus is absent. setup-result.json therefore records
qemu_executable:false and user_scope_available:false; ready_for_attempt:false,
native_acceptance:NOT_RUN, portability:UNVERIFIED. BSP path existence is only an
inventory checkpoint, not a clean compatible BSP build proof.

The ARM host has the existing QEMU but not the native x86_64 licensed SDK. The
current supported lab remains an explicit split route: SDK compilation in its
existing licensed Linux guest, stop/reap it, then native QNX on the ARM QEMU host.
Prior wrongFAIL/app0, correctedPASS and /dev/edu finish receipts remain valid only
at their original bound sources. They do not satisfy single-host readiness. No
fresh wrong/correct/finish sequence was attempted after the actual readiness
block; no SDK copy, install, login or activation was performed. Closing this gap
requires an already authorized co-located Linux x86_64 SDK/BSP/QEMU environment
with usable effective resource scopes, or separate authorization to provision the
missing QEMU/user-scope capability in the existing licensed host. No such change
is silently authorized here.

The SDK controller was guestctl-capped.py, guest1vCPU/512MiB,
hostcpu.max100000/100000,memory.max1073741824,nice15; see probe-context.json.
Initial240s collection timeout is preserved; the original job was collected later
without requeue. Slow boot and guest watchdog messages are retained externally,
not hidden or interpreted as a QNX defect. This was a capability probe, not native
QNX execution, benchmark, platform-health or portability acceptance.

README now creates the real notebook. The old duplicate step3 init failure rc2 is
preserved in entry-initial-failure.log. Corrected route renders an existing session
or initializes a fresh one; both starter hashes remain unchanged. Setup planner
runs before init, or existing notebooks use fresh-platform preflight without
reset. Canonical notebook actions retain prediction gates and numbered attempts.
The separate ARM missing-SDK boundary is preserved, never used as the actual SDK
host blocker. Browser notebook interactions PASS1280/768/520/360 (browser.json),
no screenshots/audio/video. Initial snap download/temp-path failures preserved;
explicit accessible downloadsPath corrected the browser QA environment.
