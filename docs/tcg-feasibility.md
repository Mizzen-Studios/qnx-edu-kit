# ARM64 → x86_64 TCG feasibility — 2026-11-03

Owner approved this existing Ubuntu24.04 ARM64 VM for free x86_64 software emulation, with no KVM. No new paid resource or account created. Progress stays in current session, not Discord.

## Installed and verified

- apt qemu-system-x86 and qemu-user-static:1:8.2.2+ds-0ubuntu1.18; binfmt-support:2.2.2-7. dpkg status installed; dpkg audit empty.
- QEMU8.2.2 actual binary exposes kvaser_pci, can-host-socketcan, edu and edu.dma_mask. A bounded QMP probe instantiated Kvaser10e8:8406 and EDU1234:11e8 with mask0xffffffff.
- Package-provided systemd binfmt registration for x86_64 is enabled with POF flags. Existing Python binfmt preserved. No hand-written system config replacement; unrelated pending service restarts were deferred.

## Observed on this VM — Linux smoke tests only

- Actual Alpine x86_64 Linux boot through userspace checks and poweroff:7.872s initial run;6.139s independent parent repeat. Both exit0, arithmetic/SHA256/uname successful; guest enumerated both PCI devices.1vCPU/256MiB, no network or listeners. These are two observations, not a reliable speed distribution or an SDK/QNX projection.
- x86_64 dynamic BusyBox, apk and musl loader run through explicit user-mode QEMU and transparent binfmt. Subprocesses/pipeline/wait pass. Observed0.01–0.12s individual commands. A loader-prefix negative control failed as expected; binfmt does not supply x86_64 libraries.
- Parent independently reran BusyBox uname, apk version and loader dependency resolution successfully.
- can-host-socketcan recognized, but vcan0 attachment failed because no host interface exists. Live CAN exchange is not verified.

## Verdict

Proceed with TCG development on this VM. Hardware/KVM mismatch is no longer a blocker for this approved route. Full licensed QNX boot and qcc toolchain compatibility remain UNTESTED, awaiting SDK details. Linux musl tests are not proof of glibc-based SDK tools, compiler output correctness, licensing helpers, pthreads, debugger/syscall support or realistic compile duration. Use an isolated suitable x86_64 runtime with scoped loader prefix, or an x86_64 guest if required; never use a Linux user emulator to run QNX target binaries.

Next after activation: inspect SDK ELF interpreter/library needs, test qcc/compiler/linker chain and a minimal target program; boot the licensed QNX image under TCG; verify QNX PCI enumeration then live register/IRQ/CAN gates. Still review upstream file/binary licences before copying/fetching modules. No SDK/image/header/binary belongs in Git.

## Detailed evidence

- [Guest source hashes, command and limitations](tcg-guest-feasibility.md)
- [User-mode binaries, hashes, loader and ABI limits](x86-user-feasibility.md)
- Full local logs/scripts/source artifacts:.openclaw/tmp/qnx-tcg-20261103/ on the VM, outside the repositories. Only text reports are committed; no Linux or QNX binaries/images vendored.

No QNX performance or functional evaluation is claimed. Demo of fail-safe patterns; not an ISO 26262 / IEC 61508 claim.
