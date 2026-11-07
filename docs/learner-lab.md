# Learner-owned step3: BAR complement

**Companion/reference details: start with the [canonical learner route](learner-route.md), integrating step3 then your own /dev/edu.**

This first vertical slice builds and boots **your edited C file**, separately from
reference verification. No reference receipt or transcript is an input mode.
Scope: PCI attachment, BAR0 mapping, ID and complement register only. Not IRQ,
DMA, security policy or /dev/edu assessment. C6/safestop remains stopped.

## Legal prerequisites and current portability limit

The [clean legal bootstrap](clean-step3-setup.md) now has fresh source-bound wrong-edit
FAIL and corrected native PASS on one pinned configuration, using guest disk swap
and the unmodified stock kernel. [Evidence](acceptance/clean-step3-20261107/native-clean/NOTES.md)
retains the startup Memory fault caveat. Broad portability, human validation and
independent gate reassessment remain unverified. Earlier E1 receipts are historical.

Bring your own licensed QNX 8 SDP, x86_64 BSP/buildfile, PCI services and boot disk
(if required by that BSP), plus host Python 3, QEMU and systemd user scopes.
Nothing downloads an SDK, image or private owner bundle. Keep all SDKs, target
ELFs and boot images **outside this checkout**. Paths below are learner-chosen.

The build interface accepts `--sdp-env`, `--buildfile` and `--bsp-cwd`. The original
application-only fragment `scripts/learner-step3.build.in` is a starting point, not
a bootable BSP. Adapt YOUR BSP to include the two files and run
`sh /proc/boot/learner-start.sh` after PCI server readiness. Include the licensed
PCI library/hardware modules from your setup. Do not copy someone else's BSP.
The fresh generic integration uses documented local snippets and a matching clean
disk; no E1/private stripped kernel is used in the current clean path. Historical
E1 adapter experiments remain preserved in their own earlier acceptance notes.
The separately selected `--stage step6` [finish](learner-dev-edu.md) cannot accept
step3 or reference manifests.

## Edit → build → run → diagnose → fix

1. On the source host: `python3 scripts/learner_lab.py init --work /absolute/external/lab`.
   This copies step3's TODO starter to `main.c` and refuses to overwrite edits.
2. Complete the BAR TODO in that file. Request thread I/O level 1 only. Read BAR
   metadata, validate BAR0 is memory and at least 0x1000 bytes, map uncached, check
   `r[0] == 0x010000ed`, write `0x12345678` to `r[1]`, then capture its volatile
   read-back in a variable. Expected complement is `0xedcba987`. Preserve cleanup.
   Emit the observation from those actual values, **not constants or PASS**:

   `printf("LEARNER_MMIO id=%08x write=%08x read=%08x\n", id, written, observed);`

   Return nonzero on a wrong ID/complement. A wrong-but-compiling write such as
   `0x12345679` should read back `0xedcba986` and fail the fixed stage oracle,
   even if your application incorrectly calls that a pass.
3. Inside your licensed SDK host, with this script and source accessible:

   `python3 learner_lab.py build --source /external/lab/main.c --out /external/lab/build --sdp-env /licensed/sdp/qnxsdp-env.sh --buildfile /licensed/bsp/learner.build --bsp-cwd /licensed/bsp`

   The output directory contains a source snapshot, target ELF, startup wrapper,
   image and source/binary/image-bound manifest. It runs qcc and mkifs, not a
   cached reference binary. Copy that entire build directory externally to the
   QEMU host if necessary. The run command checks the current source hash too.
4. Serialize **all** SDK/native work under the same exclusive lease. On this
   validation host the lock is `$EDU_NATIVE_LOCK (your chosen external shared lock)`. Stop and
   reap the SDK guest before native boot. Set `EDU_NATIVE_LEASE=granted` only
   while actually holding that lock. The runner checks that the named lock is
   held, but the caller is responsible for owning it, not another process.
   Example on a learner host:

   `flock /external/native-test.lock env EDU_NATIVE_LOCK=/external/native-test.lock EDU_NATIVE_LEASE=granted python3 scripts/learner_lab.py run --source /external/lab/main.c --bundle /external/lab/build --disk /licensed/bsp/disk.raw --receipt /external/lab/result`

   The host refuses overlapping QEMU, enforces 100% CPU / 1 GiB / nice 15 with
   guest 1 vCPU / 512 MiB, boots fresh (180-second timeout, 2 MiB output bound),
   captures the target's exit code and stops
   and waits for QEMU. Host status 0 means this stage passed; 1 means failed;
   2 means blocked configuration/build/binding. The QEMU wrapper is terminated
   after target completion, so its signal status is separate from target status.
5. Read `result.json` and `result.log`. Expected fields are ID `010000ed`,
   write `12345678`, read `edcba987`, one target exit `0`, matching source and
   binary boot binding, and QNX 8.0 identification. Merely printing STEP3 PASS
   cannot satisfy the oracle. Fix your source, rebuild, and rerun; stale source,
   changed ELF/image, missing MMIO data or a reference manifest is rejected.

This is a cooperative learning oracle, not protection against a malicious learner
fabricating device output/buildfiles. Hashes bind the recorded build chain and
fresh boot; they are not remote attestation or independent hardware tracing.
All saved receipts are observations, never transferable learner completion.
