# Write your first QNX 8.0 PCI driver in QEMU

**Companion/reference details: start with the [canonical learner route](learner-route.md), integrating step3 then your own /dev/edu.**

**Private working draft, 6 November 2026. Not a completed or runnable learner tutorial.**
No completion-time, first-ever, safety-certification or performance claim. The experimental native probe compiles and now demonstrates BAR mapping and factorial polling after requesting per-thread I/O level1; native one-shot interrupt completion and a 64-byte polled DMA round-trip now pass; normal resource-manager I/O now passes, while robustness and full learner acceptance remain pending. Host models and qtest prove neither QNX PCI API correctness nor a working /dev/edu.

## What we are building

A small resource manager for QEMU's edu device, PCI vendor 0x1234/device 0x11e8. Intended finish line: write 10 to /dev/edu, read 3628800. Learn discovery/ownership, BAR mapping, bounded polling, interrupt acknowledgement, DMA ownership, and request validation. That normal-I/O finish line now passes on QNX; full learner reproducibility and lifecycle robustness have not passed.

## 0. Establish a private, bounded environment

Use a locally authorized QNX SDP 8.0 installation and x86_64 target image. Keep SDKs, target headers, images, core dumps and compiled binaries outside the repository, including ignored folders. This draft does not provide an SDK downloader or a redistribution licence.

Record host architecture, QEMU version, target/SDK build, image hash, start command and log destination. ARM64 host with x86 TCG is an experiment; it is not a KVM or supported-performance claim. Boot the existing image first, without changing authentication policies. Preserve the known-good image; do not rebuild over an attached disk.

For an existing operator-reviewed QEMU command, this host uses a transient scope:

	systemd-run --user --scope --quiet -p CPUQuota=100% -p MemoryMax=1G nice -n 15 qemu-system-x86_64 ...

The ellipsis is deliberately NOT a runnable image recipe: BSP/image setup remains an acceptance gate. Native probe uses 1 vCPU and 512MiB guest RAM; the historical SDK 200% CPU / 4GiB scope is superseded: all SDK/native QEMU now use 100% CPU / 1GiB / nice15. Inspect actual cgroup cpu.max/memory.max. Use bounded runtime/logs and terminate only the owned VM. Never lift caps to make a slow test pass.

## 1. Build the experimental diagnostic

From this repository, in an authorized SDK build environment, using an external output directory:

	src="$PWD"
	source /path/to/qnx800/qnxsdp-env.sh
	mkdir -p "$HOME/edu-build"
	qcc -Vgcc_ntox86_64 -g -Wall -Wextra -Werror "$src/native/edu_probe.c" -o "$HOME/edu-build/edu_probe" -lpci

This command cross-compiles only; it does not deploy, boot, grant abilities, or create /dev/edu. Add the resulting executable through the existing private image's reviewed file list. Do not invent a target image build command from an unrelated BSP. The local mkqnximage project and image manifest remain external.

**Checkpoint:** compiler exits zero, external executable exists, repository redistribution guard passes. This checkpoint is verified with real SDP 8.0; clean-machine learner reproducibility is pending.

## 2. Discover, attach and diagnose BAR retrieval

Run the diagnostic in the private guest. It searches the edu vendor/device ID, requests exclusive attachment and calls pci_device_read_ba(). Per QNX 8 documentation, EXCLUSIVE implies ownership. The handle is a pointer token; NULL indicates failed attachment. Pass the actual capacity in nba, a valid array and UNSPECIFIED request type. Bound the returned count before iterating. Never use a guessed physical BAR address to bypass a failing API.

Expected progress markers (not a promise of success):

	EDU PROBE BEGIN
	EDU LIBPCI base=... file=... read_ba=...
	EDU PCI attached
	EDU read_ba BEGIN
	EDU read_ba END

Earlier runs stopped before END with exit139. The x86 PCI access path lacked per-thread I/O privilege. The probe now checks ThreadCtl(_NTO_TCTL_IO_LEVEL, (void *)(uintptr_t)_NTO_IO_LEVEL_1) before PCI access, requests neither inheritance nor level2, and fails closed if the existing process policy denies it. It does not grant itself new process abilities or change policy. With this request, the fresh native run printed END, BAR0=0xfea00000, size1048576, ID010000ed and factorial10=3628800. Normal cleanup relinquishes the thread I/O level. Least-privilege deny/allow tests remain pending.

The diagnostic now records signal/code/fault number/instruction/address using an async-signal-safe write handler, then exits nonzero. Its handler deliberately does not invoke printf(), malloc(), dladdr() or PCI cleanup; symbol lookup runs before the fault. Signal-handler exit means no new core is produced by this diagnostic. Existing core-dump collection should instead be used with the uninstrumented version when needed.

**Stop gate:** if END is absent, retain private fault addresses/library identity and diagnose the call/library/CPU path. Do not continue into MMIO, IRQ or DMA and do not mark this chapter passed.

## 3. Validate mapped registers and bounded polling — experimental native checkpoint

Only after BAR retrieval succeeds: choose memory BAR0, validate size/address, obtain required mapping abilities from the installed policy, map device memory uncached, then verify the edu identification value 0x010000ed. The experimental probe checks the complement register and factorial(10)=3628800 with a finite wait. Cleanup unmaps only successfully mapped memory and detaches only the acquired handle.

The fresh native run supplied BAR address, ID/complement validation and factorial result. Complete acceptance still requires invalid-device behaviour and cleanup/reprobe evidence. Do not infer these from the host model or Linux qtest. See register-evidence.md for the distinct device-model evidence.

## 4. Receive an interrupt — one-shot native checkpoint

Read the assigned IRQ through the owned device handle; attach a notification using APIs/abilities from the installed QNX 8 headers, unmask deliberately, arm a bounded wait, request an edu interrupt, confirm pending status, acknowledge the device, and verify it cleared. Separate device acknowledgement from kernel unmasking. Exercise timeout and detach cleanup. The native one-shot event-wait probe now raises status1, wakes with status1 and acknowledges it clear. Historical event-attachment diagnostics preceded the current reference IAT path. Current InterruptAttachThread attachment handles the initial unmask; the removed redundant InterruptUnmask returned EAGAIN at mask countzero. Do not blindly unmask twice. This is not a complete production interrupt service thread.

Acceptance: target raise/wait/ack transcript, timeout test, teardown/restart, no interrupt storm. A configured IRQ number is not evidence of interrupt delivery.

## 5. DMA ownership and completion — basic polled native checkpoint

The original native/edu_dma.h now performs a byte-exact 64-byte RAM->EDU->RAM round-trip with polled completion on the fixed x86 QEMU configuration. See [native DMA contract](native-dma.md): one uncached contiguous page, checked physical offset/range, explicit 32-bit device mask, bus-master enable/readback, bounded waits and QEMU-specific quiescence before release. DMA IRQ and fault-injection acceptance remain pending. Do not use this diagnostic on physical hardware. First verify the installed allocation/physical-address/ability APIs, edu DMA mask and mapping contract. Allocate a bounded buffer, establish physical contiguity and address range, initialize known bytes, transfer both directions with finite completion waits, and compare every byte. Never pass a virtual pointer as a DMA address. Quiesce DMA/interrupts before unmapping or freeing; verify timeout/error paths cannot reuse an in-flight buffer.

Acceptance: QNX-allocated buffer identity, mask/range validation, byte-exact transfers, completion IRQ, timeout, cleanup/reprobe. Host qtest DMA is device-behaviour evidence only.

## 6. Resource manager — normal-I/O checkpoint; learner gates pending

Original native/edu_resmgr.c and the target-side native/edu_accept.c now cross-build with the licensed SDK and pass actual QNX write10/read3628800, 0/12 bounds, malformed/range/oversize/NUL/nonblocking rejection, zero I/O, partial reads/EOF, same-descriptor use and independent reader snapshots. See [resource-manager contract](native-resmgr.md). This is a polling-only service, separate from the IRQ/DMA diagnostic. Owned SIGTERM teardown removed the node; graceful cleanup, restart, fault recovery and least-privilege policy are not accepted. Validate and bound requests, reject malformed/overflowing input, serialize device ownership, define partial read/write behaviour and permissions, and return failures rather than fabricated results. Keep long-running work out of an unbounded dispatch path. On shutdown stop work, quiesce DMA/IRQ, detach and unmap in a proven order.

Remaining acceptance: true simultaneous-client stress, disconnects, graceful termination/restart, injected failures, least-privilege deny/allow evidence, then two fresh learner runs. Until then verify.sh correctly refuses full target acceptance.

## References and publication gate

- QNX 8 PCI APIs: https://www.qnx.com/developers/docs/8.0/com.qnx.doc.pci_server/topic/pci_device_attach.html and pci_device_read_ba.html in the same section.
- QNX signal fault metadata: https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.lib_ref/topic/s/siginfo_t.html
- QEMU edu specification: https://www.qemu.org/docs/master/specs/edu.html (pin the tested source revision for reproducibility).

No SDK text/headers or upstream implementation is reproduced. Keep all publication, video, Pages and submission gates closed until owner approval and demonstrated target acceptance.
