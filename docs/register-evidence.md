# Register evidence boundary

No register offsets are taught by the codelab until **every row** has live
pinned-device evidence. This is not blocked only by the missing SDK: Linux QEMU
can independently establish MMIO semantics, and a real attempt was made.

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
copied into this worktree's ignored .tmp/edu-probe (no other worktree writes).
QEMU: TCG single thread, pc machine, one CPU, 256 MiB, edu, no networking,
no display/listener, serial stdio, enforced 60-second timeout. Guest enumerated
edu at 0000:00:03.0 and a 1 MiB memory BAR. An od read of sysfs resource0
failed with "read error" and RESOURCE_READ_RC=1; Linux sysfs memory BARs require
mmap rather than a plain read. BusyBox lacks devmem and no x86 C toolchain is
installed. Guest powered down normally. The probe did NOT read the ID or any
register, and verified ZERO register rows. Raw serial evidence is in
register-probe-linux.txt. A shell command exit of zero after poweroff is not
register success. No QNX claim is made.

Next independent task: build/use a provenance-pinned x86 mmap-capable Linux
helper in a separate authorized environment, map resource0 safely and validate
all widths, liveness patterns, factorial state, IRQ raise/ack and DMA directions,
counts, completion and mask behavior. Never substitute sysfs enumeration for
MMIO proof. Actual interrupt delivery and DMA require more than register reads.
