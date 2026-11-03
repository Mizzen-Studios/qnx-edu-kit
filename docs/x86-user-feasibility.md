# x86_64 Linux host-tool emulation on ARM64

Tested 2026-11-03 21:21 UTC on this Ubuntu ARM64 VM, kernel 7.0.0-1013-oracle.

## Verdict
Viable for three distinct tested x86_64 ELF files: dynamic busybox, dynamic apk, and musl loader, plus external subprocess/pipeline execution. Explicit qemu and transparent binfmt both work. This is NOT proof QNX SDP/qcc works: no SDK supplied or executed.

## Evidence and reproduction
Run bash test.sh; full commands, file/readelf metadata, outputs, exit statuses and GNU time measurements are in evidence.log. Parent-provided emulator: qemu-x86_64 8.2.2, package 1:8.2.2+ds-0ubuntu1.18. Binfmt enabled with interpreter /usr/libexec/qemu-binfmt/x86_64-binfmt-P, flags POF.

Official pinned archive: https://dl-cdn.alpinelinux.org/alpine/v3.22/releases/x86_64/alpine-minirootfs-3.22.2-x86_64.tar.gz
Official checksum fetched from that URL plus .sha256, and sha256sum -c passed. SHA256: 412454ed98025ad9cd910d13f3d448b184e81502baa83180e89f98d0f13674be. This establishes HTTPS/checksum consistency, not independent signature verification. Archive 3.49 MiB; directory including extracted root 13 MiB.

## Single observations on THIS VM only
- Dynamic busybox uname -m: explicit qemu -L 0.04 s, transparent binfmt 0.01 s; x86_64, exit 0.
- Dynamic apk --version: explicit 0.05 s, transparent 0.05 s; apk-tools 2.14.9 x86_64, exit 0.
- Musl loader --list busybox: explicit and transparent 0.01 s each; libc resolved, exit 0.
- x86_64 ash launches explicit x86_64 ELF children, subshell, pipe and wait: 0.12 s; uname, empty SHA256 and SUBPROCESS-OK correct, exit 0.
- x86_64 busybox SHA256 of archive: 0.11 s, same official checksum. Native ARM64 sha256sum: 0.00 s at timer resolution, same checksum. Do not derive a reliable slowdown ratio from this.
- Peak observed process RSS 9664 KiB. Per-command timeout and CPU limit 30 seconds; no parallel stress. These are single warm/cold-uncontrolled observations, not SDK compile benchmarks. No compiler installed; subprocess test provides inexpensive extra coverage.

## Loader and SDK dependencies
Explicit: qemu-x86_64-static -L ROOT ROOT/bin/busybox uname -m
Transparent: QEMU_LD_PREFIX=ROOT ROOT/bin/busybox uname -m
Negative control without prefix failed exit 255: cannot open /lib/ld-musl-x86_64.so.1. Binfmt registration does not provide x86_64 libraries. -L or QEMU_LD_PREFIX provides loader/library lookup, NOT a chroot or filesystem security boundary. No chroot used. External children need binfmt and inherited QEMU_LD_PREFIX; do not assume explicit parent -L alone configures children.

Actual QNX Linux host tools likely require supported x86_64 glibc userspace and specific C++/other libraries, not this musl root. Inspect SDK ELF interpreter and NEEDED dependencies, provide suitable isolated root/container/chroot or scoped prefix, and legitimate QNX_HOST/QNX_TARGET/license setup. Owner-supplied licensed SDK and activation are required before qcc/compiler/linker subprocess-chain or output-correctness claims. QNX target executables are not Linux-user programs: this only addresses Linux SDK host executables.

Simple process exec, pipes, subshells and wait passed. Pthreads/TLS-heavy workloads, compiler correctness, signals/debuggers/ptrace, exotic syscalls, SIMD feature dependencies, atomics/futexes, licensing helpers and full SDK ABI compatibility remain UNTESTED. User-mode translation uses host Linux kernel, not a virtual x86_64 kernel. No KVM needed here; this does not establish QNX full-system boot/performance.

All child writes confined to this user/ artifact directory. No apt/packages installed by child, no system config/repo changes, accounts, SDK access, guest boot or spend.
