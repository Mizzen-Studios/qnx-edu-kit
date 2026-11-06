# Experimental native /dev/edu resource manager

**Real SDP 8.0 cross-build and native QNX normal-I/O acceptance passed, 6 November 2026. Robustness and least-privilege acceptance remain pending.**
Original application source: native/edu_resmgr.c (repository path).
No copied SDK implementation, API shim, host factorial, subprocess or model is used.
This is separate from the IRQ/DMA diagnostic and does not implement either feature.

## Build and run gate

Verified licensed-SDP build against the real QNX 8 headers:

~~~sh
mkdir -p "$HOME/edu-build"
qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -fno-omit-frame-pointer \
  -Wall -Wextra -Werror native/edu_resmgr.c -lpci -o "$HOME/edu-build/edu_resmgr"
~~~

Keep those diagnostic flags. Do not place SDK files or built target binaries in
this repository. This document is not an installation or deployment instruction.
Run only on the authorized QNX target with its PCI server and QEMU EDU function,
and with no competing probe/driver attached. The process needs public-channel,
pathname-registration, physical-memory mapping and level-1 I/O permissions under
the target policy; this source neither grants abilities nor demonstrates least
privilege/secpol. Ownership is the process effective UID/GID, initial mode 0660.

One main/dispatch thread requests checked
ThreadCtl(_NTO_TCTL_IO_LEVEL, (void *)(uintptr_t)_NTO_IO_LEVEL_1), without
inheritance. It exclusively attaches PCI 1234:11e8, obtains BAR0 through
pci_device_read_ba(), maps 4096 noncached bytes and checks ID 010000ed before
registering /dev/edu. All PCI/MMIO and request handlers remain on that thread.
No thread pool, interrupt handler or DMA exists here. The tested probe's physical
BAR address is deliberately not hard-coded.

## Device contract

- A blocking write is one complete command: one or two ASCII decimal digits,
  optionally followed by LF, value 0 through 12 inclusive. Leading zeroes within
  two digits are allowed. Maximum payload is three bytes; no NUL terminator.
- Commands are atomic: no successful short write or cross-write accumulation.
  Splitting "10" into writes "1" then "0" requests two separate factorials.
  A zero-length write returns zero without MMIO.
- A validated write disables factorial IRQ generation, writes the operand to
  BAR0+0x08, polls busy at BAR0+0x20, then reads the hardware result at BAR0+0x08.
  Success acknowledges all input bytes only after completion. No software
  factorial calculation is present.
- Polling uses a one-second CLOCK_MONOTONIC deadline, at most 1000 iterations,
  and sleeps at most 1 ms per iteration. It does not bound scheduling latency,
  IPC queue delay or a CPU fault/stalled MMIO bus access. Waiting for new IPC
  requests while idle is normal, not a device-completion wait.
- Reads return decimal result plus LF. A successful write resets that descriptor's
  read offset. A new reader snapshots the most recent completed result on its
  first nonempty read. Partial reads advance the OCB offset; then EOF. Existing
  reader snapshots remain coherent even if another client writes. Reopen to
  obtain a newer result (or issue a successful write on the same O_RDWR OCB).
  Duplicated descriptors share the normal OCB/offset semantics.
- Before the first result, a nonempty read returns EAGAIN, not fabricated data.
  A zero-length read returns zero. A valid nonempty O_NONBLOCK write returns
  EAGAIN without starting hardware work; synchronous completion is intentional.
- Oversized writes: EMSGSIZE. Malformed/empty command text, signs, whitespace,
  embedded NUL and extra LF: EINVAL. Parsed values 13..99: ERANGE. A message
  declaring unavailable payload bytes: EBADMSG. Unsupported read/write xtype
  (including positioned I/O): ENOSYS. iofunc verification errors propagate.
- Already-busy hardware: EBUSY. Deadline expiry: ETIMEDOUT. Polling interruption
  or clock failure propagates its error and latches failure if work was started;
  subsequent new reads/writes return EIO until restart. Previous reader snapshots
  may still finish. There is no cancellation/reset/recovery claim. Invalid input
  is rejected before MMIO and leaves an existing result intact.

## Observed target acceptance

Original native/edu_accept.c was cross-built with -Wall -Wextra -Werror and
executed inside the capped QNX VM, not on a host model. It first ran the native
BAR/IRQ/DMA probe, then launched its owned resource manager. Observed:

- Character node mode0660; initial nonempty read EAGAIN.
- Actual MMIO write10/read3628800, 0->1 and 12->479001600.
- Malformed negative/text, range13, oversized1234, embedded NUL, nonblocking
  writes and zero-length I/O returned their expected results.
- One-byte partial reads, EOF, same O_RDWR descriptor and independent reader
  snapshots while another writer updates passed.
- Owned server SIGTERM/reap removed the node. This is OS teardown, not proof of
  graceful signal cleanup or restart.
- EDU RESMGR ACCEPT PASS (normal I/O only; robustness pending), probe exit0.

Private transcript: .openclaw/tmp/qnx-followup9/native-resmgr.log in the operator
workspace. The same run observed native libcan RX100/100 and independent
TX100/100 byte-exact. No target binaries or SDK files are distributed.

## Remaining / extended target acceptance

The following checklist retains the full intended scope. Cross-build and the
normal cases listed above passed; unchecked variants and fault cases remain pending.

1. Cross-build with the flags above; inspect real headers for handler signatures,
   _IO_READ/WRITE_GET_NBYTES, OCB allocator callbacks, iofunc_mount_init and
   dispatch/resmgr lifecycle. The parent cross-build validated the actual installed SDK headers.
2. Check actual /dev/edu character-node mode/ownership and denied access for an
   unauthorized client. Capture PCI attach, mapping and startup failures.
3. On target, write 10 with LF and read exactly 3628800 with LF; check 0 -> 1 and
   12 -> 479001600. Use both reopen/read and the same O_RDWR descriptor.
4. Check one-byte reads, EOF, zero-length I/O, concurrent independent reader
   snapshots, repeated commands, and split-write semantics.
5. Capture errno for malformed, out-of-range, oversized and nonblocking writes;
   include embedded NUL, negative input, trailing spaces, 13, 99 and 1234.
   Check that rejection does not trigger an MMIO transaction.
6. Exercise busy/deadline/failure behavior with an authorized target/device fault
   setup, without a host fake. Verify no stale new result is reported after failure.
7. Check stop/restart, device reattach and client cleanup. Default signal
   termination relies on OS process teardown: graceful signal-driven shutdown,
   hot-unplug, ACL policy, hard real-time service and production safety are NOT
   implemented or accepted. Error paths explicitly detach/unmap/release I/O level.

## Public API references

- [QNX 8 resource-manager read messages](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.resmgr/topic/read_write_HANDLING_READ_MSG.html)
- [Write messages](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.resmgr/topic/read_write_HANDLING_WRITE_MSG.html)
- [iofunc_read_verify](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.lib_ref/topic/i/iofunc_read_verify.html), [iofunc_write_verify](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.lib_ref/topic/i/iofunc_write_verify.html)
- [resmgr_msgread](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.lib_ref/topic/r/resmgr_msgread.html), [resmgr_attach](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.lib_ref/topic/r/resmgr_attach.html)
- [iofunc_mount_t and allocator callbacks](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.lib_ref/topic/i/iofunc_mount_t.html), [iofunc_mount_init](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.lib_ref/topic/i/iofunc_mount_init.html)
- [dispatch_create](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.lib_ref/topic/d/dispatch_create.html)
