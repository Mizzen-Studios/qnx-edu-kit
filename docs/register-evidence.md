# Register evidence boundary

The host-side gate now runs against actual installed QEMU 8.2.2 EDU, not a
handwritten model. This is **NOT QNX API validation**. The earlier failed
sysfs attempt is retained below as historical evidence, superseded by qtest.

## Source pin (not live proof)

- QEMU v8.2.2 tag object: 03e36c72c2c44f9afb116858d5e7c92be66a32b1.
- Peeled commit: 11aa0b1ff115b86160c4d37e7c37e6a6b13b77ea.
- File: hw/misc/edu.c.
- SHA256: 198754be868d35d72dd7f83c91491856cbd76cf5d9fc4ad71bf950ab761d7ad6.
- URL: https://github.com/qemu/qemu/blob/11aa0b1ff115b86160c4d37e7c37e6a6b13b77ea/hw/misc/edu.c

The original stdlib model implements selected behavioral contracts only. Explicit
completion replaces QEMU threads/timers. Input/range rejection is a driver design
choice, not claimed QEMU behavior. The model omits MMIO widths, endian behavior,
MSI/INTx delivery, physical DMA and cache ownership. No QEMU source is vendored.
Ubuntu's installed QEMU is 8.2.2 Ubuntu1.18; source pin is an upstream reference,
not proof of byte-for-byte identity with the distro-patched executable.

## Actual independent Linux probe, 2026-11-03

Used the existing checksum-verified Alpine 3.22.7 rootfs and Linux 6.12.114 kernel,
initially copied into this worktree's .tmp/edu-probe, then moved out to
.openclaw/tmp/qnx-core-20261103/edu-register-evidence/edu-probe so the
conservative guard can remain intact. No other worktree writes.
QEMU: TCG single thread, pc machine, one CPU, 256 MiB, edu, no networking,
no display/listener, serial stdio, enforced 60-second timeout. Guest enumerated
edu at 0000:00:03.0 and a 1 MiB memory BAR. An od read of sysfs resource0
failed with "read error" and RESOURCE_READ_RC=1; Linux sysfs memory BARs require
mmap rather than a plain read. BusyBox lacks devmem and no x86 C toolchain is
installed. Guest powered down normally. The probe did NOT read the ID or any
register, and verified ZERO register rows. Raw serial evidence is in
register-probe-linux.txt. A shell command exit of zero after poweroff is not
register success. No QNX claim is made.

## Successful qtest verification, 2026-11-04 UTC

Operator: automated assistant; independent human review pending. Base commit,
exact executable/probe SHA256 and full command are recorded in
[register-qtest-live.txt](register-qtest-live.txt). Installed package:
1:8.2.2+ds-0ubuntu1.18; host aarch64 Ubuntu24.04 / Linux7.0.0-1013-oracle;
emulated x86_64 PC TCG single-thread. No guest OS or SDK is used.
Upstream docs/specs/edu.rst SHA256:
fedc8a6b4dc2f3d6d127c5390f7c3580eb8a3ff24d0846bf1674d42a0c420d3c.
Source/docs at the peeled pin were fetched, checksummed and inspected at
edu_mmio_read/write, dma_rw, edu_dma_timer, edu_check_range, edu_clamp_addr,
edu_fact_thread and pci_edu_realize. No upstream file/binary is vendored.
Distro identity is recorded separately, not represented as an upstream build.

### Reproduce from repository root

- PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_edu_source.py (explicit online pin check)
- PYTHONDONTWRITEBYTECODE=1 python3 scripts/edu_qtest.py --run
- make live-edu-check (opt-in actual executable integration test)
- make host-check (live test skipped unless EDU_LIVE_QTEST=1)

Only stdlib Python and installed qemu-system-x86_64 are needed: no compiler,
apt, SDK, account or paid resource. The probe configures PCI CF8/CFC, sizes
and assigns BAR0, enables MEM+MASTER, then performs qtest readl/writel/readq/
writeq and physical RAM writes/reads. PIIX routes PIRQ to IRQ11;
irq_intercept_in ioapic proves actual INTx controller-input assertion,
partial/full acknowledgement and repeat delivery. Factorial runs the actual
QEMU worker, with three-second bounded polling and a large-input busy test.

This distro has TCG but **no -accel qtest**; clock_step returns Unknown command.
QMP cont/stop instead advances virtual time for the 100ms DMA timer. An original
four-byte CLI/HLT/JMP reset loop in generated 64KiB firmware prevents normal
BIOS reassigning PCI while time advances. It is created only under workspace
.tmp, deleted by TemporaryDirectory and never checked in. This is test firmware,
not Linux/QNX or a redistributed BIOS. No TCP listener/network is created; QMP
uses a temporary workspace Unix socket. Transport/startup/factorial/process
waits are bounded; processes cleaned up; core dumps disabled.

DMA round-trips compare bytes at counts1/100/4096 and device offsets4095/17/0.
32-bit command1 and 64-bit commands3/7 prove direction/no-IRQ/completion IRQ0x100. Default28-bit and
explicit24-bit masks (last two bytes and first-above wrap also checked) prove high host RAM addresses clamp without altering the
stored source/dest registers. Separate isolated QEMU processes prove count0,
4097, device address0x41000 and crossing0x40fff cause EDU range diagnostics and
SIGABRT. These are expected QEMU failures, **not safe driver error returns**.
The driver must reject bad inputs before touching the device.

The [row ledger](verification-checklist.md) covers every candidate register.
Residuals are explicit: MSI, QNX interrupt attachment/delivery, QNX ownership,
physical-address/cache APIs, full alignment/mask matrix. None are excused as SDK blockers where host testing remains
possible; only QNX-specific validation requires SDK/target. This evidence permits
a QEMU-device reference appendix, not target-verified QNX tutorial/API code.

Transcript SHA256: 5658631e4a2841e95efc5b39776604842e27b298a2ffd5972b4b383bb0156b72.
