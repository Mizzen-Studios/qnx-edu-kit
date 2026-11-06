# Native crash isolation and SSH recovery — 6 November 2026

Private QNX 8 / QEMU 8.2.2 TCG experiment; licensed files remain external.

## SSH packaging recovered, workaround still required

The system partition mounts at /system, not /usr. Existing generated configuration already sets SshdSessionPath /system/bin/sshd-session. Install sshd-auth into the same bin directory and explicitly override SshdAuthPath. The prior /libexec destination yielded /system/libexec, not the daemon's default /usr/libexec.

In the external mkqnximage project, system_files.custom now adds (expand the locally licensed SDK path at build time):

    [perms=0755] bin/sshd-auth=$QNX_TARGET/x86_64/usr/libexec/sshd-auth

Boot diagnostic:

    OPENSSL_ia32cap=0 /system/bin/sshd -t -e -f /system/etc/ssh/sshd_config -o SshdAuthPath=/system/bin/sshd-auth
    OPENSSL_ia32cap=0 /system/bin/sshd -e -f /system/etc/ssh/sshd_config -o SshdAuthPath=/system/bin/sshd-auth

Observed both exit 0. Both helpers are executable at /system/bin. Host ssh-keyscan against loopback-only QEMU forwarding returned exit 0, one host-key row, SSH-2.0-OpenSSH_10.4. This proves transport handshake, NOT authenticated login or a permanent image configuration fix. OPENSSL_ia32cap=0 is still an experimental workaround; the underlying OpenSSL/TCG fault is not diagnosed. No password/authentication policy changed.

## EDU crash isolated further

Recompiled original diagnostic with qcc -Vgcc_ntox86_64 -g -Wall -Wextra -Werror -lpci. Zero-initialized BAR array, bounded returned count, and added markers. Target output:

    EDU PROBE BEGIN
    EDU PCI attached
    EDU read_ba BEGIN
    Memory fault (core dumped)
    EDU_PROBE_RC=139

No read_ba END: crash is inside the call (or its return path), before our BAR iteration/MMIO. Installed header confirms pointer handle and API argument types; signature mismatch was not established. Private core/library investigation remains needed. Native IRQ, DMA and resource manager remain BLOCKED; no host test substitutes for them. Tutorial draft now describes this crash-first boundary, not a working learner exercise.

## Safety and tests

QNX probe: CPUQuota=100%, MemoryMax=1G, nice15, 1 vCPU/512MiB. SDK build guest: CPUQuota=200%, MemoryMax=4G, nice15; observed cpu.max=200000 100000 and memory.max=4294967296. Separate fresh CAN gate passed 100/100 RX and TX byte-exact with explicit PIRQ correction. Host suites: CANopy 91 tests/3 skipped, edu-kit 43 tests/1 skipped. Native failures are independent of green host tests.
