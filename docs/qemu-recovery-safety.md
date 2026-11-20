> Portable paths: set EDU_NATIVE_LEASE to your operator-approved shared native lock and QNX_GUESTCTL to your reviewed external controller. These are licensed native prerequisites, not HOST judge steps. Do not invoke native commands without separate authority.

# QEMU recovery safety — 4 November 2026

**HISTORICAL REFERENCE ONLY — superseded launch instructions below must not be
executed for the learner route.** In particular scripts/qemu-capped.sh and the
old owner guestctl example use historical200%CPU/4GiB, not today's authorized
100%CPU/1GiB/nice15 and guest1vCPU/512MiB. No guestctl bootstrap is provided.
Use the [canonical learner route](learner-route.md), legal supplied SDK/BSP/QEMU
paths and shared exclusive lease; stop at unavailable setup. Old observations
and failed hypotheses below remain preserved, not current launcher approval.


Use `scripts/qemu-capped.sh COMMAND [ARG ...]` for every QEMU launch, including the SDK guest controller and EDU qtest tests. Example:

    ./scripts/qemu-capped.sh python3 "$QNX_GUESTCTL" start

The wrapper creates a user systemd scope with CPUQuota=200%, MemoryMax=4G and nice 15. All descendants inherit limits. Failure to establish the scope is fatal: no uncapped fallback. This is a per-launch cap, not an aggregate cap; do not run multiple wrappers concurrently without budgeting their sum. On this four-core host, reserve at least one core for SSH/Gateway; the recovery run uses 200% for the SDK guest and 100% for one bounded QNX probe. Stop guests when finished. Do not use all four cores for parallel guest builds.

The reboot/hang's cause is not proven. These limits mitigate resource starvation, not a diagnosis of the outage. No system services, timers or Gateway config were changed.

Live verification: systemd accepted both recovery scopes; SDK scope CPUQuotaPerSecUSec=2s and MemoryMax=4294967296. Three launcher tests cover exact limits/argv preservation, cap failure without retry, and missing-command rejection. Use the wrapper for host test commands that themselves spawn QEMU, too.

## 6 November follow-up: queue/lifetime and fast IFS rebuilds

- Keep the managed SDK-start tool alive with an explicit, bounded lifetime longer than the intended build session; collect it after graceful guest stop. A tool supervisor lifetime killed the first SDK VM in this run. This was not evidence of OOM or a reason to raise CPU/memory caps. Stale exit.json is not proof that a current VM is running: inspect QMP/process state.
- SDK scripts serialize through the existing shared queue. An exec waiter timeout does NOT cancel the queued/running job. Retain its ID and inspect its existing log/rc before retrying. If the VM died before the queued script started, restart the same capped guest and let that job run once; do not enqueue a duplicate.
- For an application-only update, the already-reviewed external mkqnximage project can reuse its generated output/build/ifs.build: cross-compile the external application, inspect its manifest entry, then run mkifs -v output/build/ifs.build /external/new-ifs.bin from that project directory. This was tested for the diagnostic and a separate acceptance IFS. It avoids rebuilding the unchanged system disk. It is not a universal BSP image recipe. Do not overwrite an attached disk/image, and keep outputs/SDK files outside Git.
- Record actual cgroup cpu.max/memory.max after restart. This run retained SDK200%/4GiB and one native probe100%/1GiB, nice15. Do not silently add guests to the aggregate budget.
- Require completion markers AND observed RX/TX counts AND the native probe/client exit result. A legacy private traffic runner returned exit0 even on a missing marker; that result was rejected and a fail-closed private wrapper used thereafter. Host tests, a successful compiler, and CAN traffic alone do not prove native EDU/resmgr acceptance.

## Native x86 prerequisites recovered

The BAR fault was resolved by a checked per-thread ThreadCtl IO_LEVEL_1 request before PCI access. Do not request level2, inheritance or broad process-ability grants to hide a denied prerequisite. The main/dispatch thread owns hardware access; a future worker must acquire its own documented permissions.

The next IRQ failure was redundant initial InterruptUnmask returning EAGAIN at mask countzero. Default InterruptAttachEvent already handles initial unmasking. The corrected one-shot probe raised, waited and acknowledged successfully. Device acknowledgement and kernel masking remain separate operations; this is not a production IST or storm/timeout proof.

The DMA helper is a fixed x86 QEMU/no-IOMMU diagnostic, not a portable allocator or physical-hardware quiescence contract. Follow native-dma.md and retain the external bounded VM recovery path.
