# Clean step3 attempt — 7 November 2026

In progress: original setup instructions and a read-only licensed-host preflight
were added. No oracle semantics changed. Portability remains **UNVERIFIED**;
no clean native negative/corrected acceptance is claimed.

The existing licensed x86_64 SDK lives inside an external Ubuntu VM. This task
started that VM while holding actual shared flock
/home/ubuntu/qnx-host/native-test.lock. Observed PID 144372: cpu.max 100000 100000,
memory.max 1073741824, nice 15, guest -smp 1 -m 512. No other QEMU was running.
Only installed-file inventory was queued initially; no login/install/licensing
operation, download or private platform bundle was used.

Final results and stop/reap receipts follow in the next milestone.
