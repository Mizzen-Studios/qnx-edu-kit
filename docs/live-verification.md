# Fresh QNX target verification

Full verification boots an external source-bound image. No saved transcript is
accepted as live input. Fresh IRQ-resmgr acceptance is pending until the new run
completes; the old polling receipt is insufficient.

Owner workflow (private local machine only):

1. Obtain exclusive SDK lease; stage native sources into the distinct external
   qnx-host/guest/shared/edu-followup10 directory.
2. Run scripts/build-target.sh inside the licensed SDK guest. Existing owner
   base buildfile required; this is not an SDK installer/distributor.
3. Create external manifest.json: sources (repository-relative native paths to
   SHA256), image_sha256, disk (compatible external raw disk path).
4. Release SDK after all requested builds. Obtain exclusive native lease.
   Set EDU_LIVE_BUNDLE to the external directory, EDU_NATIVE_LEASE=granted,
   then ./verify.sh. make check-stepN performs another fresh accumulated run,
   never replaying the previous receipt. A failed prerequisite fails closed.

Launcher requests and inspects CPUQuota100%, MemoryMax1GiB, nice15,
1vCPU/512MiB. Snapshot mode preserves shared disk. Raw log and source/image/cgroup
JSON receipt are stored outside Git. Missing lease/bundle, stale source or changed
image rejects before boot. Each run must show all six target markers, exit0,
real shell echo/cat 3628800, and IAT-backed resmgr IRQ completion/ack clear.

The resource manager has no polling fallback: its dispatch thread attaches with
InterruptAttachThread; blocking writes request factorial IRQ, wait with monotonic
deadline, acknowledge, unmask and publish device result only. No software factorial.
No least-privilege, graceful-stop, fault-injection or physical-hardware claim.
Observed in this QEMU run · app budget, not a QNX benchmark.
