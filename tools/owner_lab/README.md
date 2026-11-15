# Existing owner-lab controller contract

Configurable source equivalent of the external controller used by the recorded journey, **not a newly runtime-tested controller**. No installation, SDK download, image creation or licence activation is provided. No guests run in host tests.

Set EDU_LAB_DIR to an existing external directory containing guest.qcow2 (licensed SDK Linux guest), seed.iso (existing configuration), and shared/{queue,results}. Existing guest needs qnx user, legal SDP8.0 environment and a root queue agent. Queue script and service source are included for review, not automatically installed: existing root service runs /usr/local/sbin/host-queue. The 9p hostshare mounts at /mnt/host. Queue access grants root guest command execution: restrict it to the trusted owner. No image or SDK bytes belong in Git.

Run python3 guestctl.py start|status|stop, or exec SCRIPT [SECONDS], with EDU_LAB_DIR set every time. For scripts/stock_sdk_owner.py --controller, place a reviewed copy of guestctl.py inside EDU_LAB_DIR: the wrapper expects qemu.pid and shared/ beside its controller. The environment directory MUST equal that external copy's parent. Alternatively keep the existing reviewed external controller. This does not alter the recorded recipe or its receipts.

The direct run entry fails closed unless effective ancestor cgroup-v2 limits prove CPU<=100%, memory<=2GiB and swap0, with actual nice15. This host-tested guard hardens the source equivalent; it has not been guest/native validated.

start uses existing systemd user scope CPU100%, memory2GiB, swap0, nice15, one CPU and TCG256. EDU_SDK_MEMORY_MIB=1024 opts into SDK1GiB. Native512MiB runner is separate. Exclusive lease and stock-route preflight checks remain mandatory: this low-level controller alone is not the lease/resource monitor. Use scripts/stock_sdk_owner.py for monitoring and cleanup. Never overlap SDK and native. STOP/REAP and verify zero QEMU before releasing lease.

Only Python stdlib and existing QEMU/systemd utilities are needed. No credentials configured. An exec timeout does not cancel its queued/running job: inspect results before retry. Submission-prep coverage is host-only, not another SDK/native acceptance.
