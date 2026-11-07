# Initial clean learner finish — failed

Fresh source-bound native run: the daemon registered /dev/edu and attached IRQ10,
but printf10 timed out; cat returned EIO. Wrapper exit1, no IRQ completion marker.
Source/binary/image/disk bindings, target identity and QEMU cleanup checks passed;
normal-I/O/IRQ/exit checks failed. Raw receipts are preserved, not overwritten.

Inspection found the scaffold kept the dispatch thread attached as an IST across
message dispatch. QNX documents that an IST may block only in InterruptWait. The
next edited-source run changes to transaction-scoped attach/wait/ack/detach and
NO_UNMASK + wait-UNMASK. This corrects an API-lifetime issue; the exact cause of
the earlier timeout is not independently isolated. No timeout extension, polling
fallback, reference pre-run, image substitution or oracle change is used.

The startup Memory fault after Starting sshd is also retained and not fixed.
