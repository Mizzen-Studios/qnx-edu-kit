# QEMU recovery safety — 4 November 2026

Use `scripts/qemu-capped.sh COMMAND [ARG ...]` for every QEMU launch, including the SDK guest controller and EDU qtest tests. Example:

    ./scripts/qemu-capped.sh python3 /home/ubuntu/qnx-host/guest/guestctl.py start

The wrapper creates a user systemd scope with CPUQuota=200%, MemoryMax=4G and nice 15. All descendants inherit limits. Failure to establish the scope is fatal: no uncapped fallback. This is a per-launch cap, not an aggregate cap; do not run multiple wrappers concurrently without budgeting their sum. On this four-core host, reserve at least one core for SSH/Gateway; the recovery run uses 200% for the SDK guest and 100% for one bounded QNX probe. Stop guests when finished. Do not use all four cores for parallel guest builds.

The reboot/hang's cause is not proven. These limits mitigate resource starvation, not a diagnosis of the outage. No system services, timers or Gateway config were changed.

Live verification: systemd accepted both recovery scopes; SDK scope CPUQuotaPerSecUSec=2s and MemoryMax=4294967296. Three launcher tests cover exact limits/argv preservation, cap failure without retry, and missing-command rejection. Use the wrapper for host test commands that themselves spawn QEMU, too.
