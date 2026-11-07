# Canonical learner route: predict → edit → observe → diagnose → explain

**Start here: step3 first, then your own /dev/edu.** Private conditional acceptance;
native feature freeze. No reference PASS transfers to your edits. Existing automated
native observations are not fresh SDK installation, second-SDK portability or
independent human acceptance. C6 STOPPED; SocketCAN UNVERIFIED. No publication.

## 0. Choose legal inputs and preflight

Use Bash and Python3 from any working directory. Replace these absolute placeholders
with your chosen paths. Keep SDKs, ELFs, IFS and disks outside every checkout,
including ignored folders. Snippet paths must have no spaces.

```sh
export EDU_REPO=/absolute/path/to/qnx-edu-kit
export EDU_WORK=/absolute/external/edu-learner
export EDU_SDP_ENV=/absolute/licensed/qnx800/qnxsdp-env.sh
export EDU_PLATFORM=/absolute/external/new-clean-platform
export EDU_ACTIVE=/absolute/external/learner-active
export EDU_QEMU=/absolute/path/to/qemu-system-x86_64
export EDU_NATIVE_LOCK=/absolute/external/native-test.lock
export PATH="$(dirname "$EDU_QEMU"):$PATH"
python3 "$EDU_REPO/scripts/learner_lab.py" --help
python3 "$EDU_REPO/scripts/learner_clean_preflight.py" --sdp-env "$EDU_SDP_ENV" --fresh-work "$EDU_PLATFORM"
```

Run the preflight **inside your already licensed Linux x86_64 SDK host**, not
merely the ARM QEMU host. It checks compiler/image tools and stock startup/kernel/
PCI files, not activation, complete BSP compatibility or bootability. Exit2 is
**BLOCKED: stop and retain JSON**. Do not install/activate an SDK or substitute an
owner image. Trust the supplied environment script before sourcing it.
On a split host, copy the original standalone learner_lab.py and
learner_clean_preflight.py plus your source to the SDK host; replace EDU_REPO script
paths there with those copied absolute script paths. Neither imports a companion
module currently. On the QEMU host check the chosen executable and host utilities:

```sh
"$EDU_QEMU" --version
command -v flock
command -v systemd-run
systemctl --user show-environment >/dev/null
```

Presence is not proof of effective resource caps. Serialize all SDK/native QEMU
phases under the same exclusive lock: host100%CPU/1GiB/nice15,
guest1vCPU/512MiB. Stop/reap SDK QEMU before native QEMU. Do not use old uncapped
guestctl. Set EDU_NATIVE_LEASE=granted only while actually owning the lock.

## 1. Predict and edit step3

Write a prediction externally: complement32(12345679)=edcba986, but the fixed
stage expects write12345678/readedcba987. The wrong variant must fail even if your
application incorrectly returns0. Then initialize your own source:

```sh
python3 "$EDU_REPO/scripts/learner_lab.py" init --stage step3 --work "$EDU_WORK/step3"
```

Edit EDU_WORK/step3/main.c, not a solution/generated snapshot. Complete the BAR
TODO: request per-thread I/O level1 only, obtain BAR metadata, require memory
BAR0 of at least0x1000 bytes, map uncached, read ID r[0], write r[1] and read
r[1] back through volatile MMIO. Start with wrong write0x12345679. Emit actual
values, not constants:

```c
printf("LEARNER_MMIO id=%08x write=%08x read=%08x\n", id, written, observed);
```

Check ID010000ed/complement, return nonzero on mismatch, preserve unmap/detach.
A program's own PASS is not the stage oracle.

## 2. Legal clean platform and source-bound build

This is a setup gate, not a bundled bootstrap. Narrow tested configuration:
SDP8, Generic x86_64 BSP0.0.1.00050T202311201204L,
mkqnximage0.5.0.00132T202605281115L, QEMU8.2.2 pc TCG. Missing compatible legal
SDP/BSP or matching disk means **BLOCKED**, not second-install portability PASS.
Existing SDK reuse is not a fresh SDK install.

On the SDK host under the shared SDK lease, source the trusted SDP and preseed
only to resolve the later application snippet files. The preseed image is NOT
learner completion. Keep launchers outside the empty platform directory.

```sh
source "$EDU_SDP_ENV"
mkdir -p "$EDU_ACTIVE"
qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -Wno-unused-variable -o "$EDU_ACTIVE/learner_bin" "$EDU_WORK/step3/main.c" -lpci
printf '#!/bin/sh\nexit 2\n' > "$EDU_ACTIVE/learner-start.sh"
mkdir "$EDU_PLATFORM"
cd "$EDU_PLATFORM"
mkqnximage --type=qemu --arch=x86_64 --build --ssh-ident=none
mkdir -p local/snippets
sed "s|@OUT@|$EDU_ACTIVE|g" "$EDU_REPO/scripts/learner-step3.build.in" > local/snippets/ifs_files.learner
printf 'waitfor /dev/pci/server_id_1 30\nsh /proc/boot/learner-start.sh\n' > local/snippets/post_start.learner
mkqnximage --build
```

Keep the stock kernel unmodified. On the constrained SDK guest, arrange authorized
1GiB disk-backed guest swap and an isolated transient guest build service before
linking:512MiB without swap previously OOMed. Do not lift caps or strip the kernel.
Stop on OOM, transport loss or nonterminal service status. The
[setup details/history](clean-step3-setup.md) preserve swap/service operations and
failures; owner-specific historical launchers are not a portable bootstrap.
Now replace the preseed with a freshly compiled source-bound bundle:

```sh
python3 "$EDU_REPO/scripts/learner_lab.py" build --stage step3 --source "$EDU_WORK/step3/main.c" --out "$EDU_ACTIVE" --sdp-env "$EDU_SDP_ENV" --buildfile "$EDU_PLATFORM/output/build/ifs.build" --bsp-cwd "$EDU_PLATFORM"
```

Preserve the entire bundle externally before replacing it with another variant.
For split hosts, transfer that bundle and matching output/disk-qemu externally,
and set EDU_ACTIVE/EDU_PLATFORM to the QEMU-host copies. The current edited source
must also match. Never substitute a historical binary or edit manifest hashes.

## 3. Observe, diagnose, fix and explain step3

Stop/reap the SDK guest; hold the exclusive native lease on the QEMU host:

```sh
flock "$EDU_NATIVE_LOCK" env EDU_NATIVE_LOCK="$EDU_NATIVE_LOCK" EDU_NATIVE_LEASE=granted python3 "$EDU_REPO/scripts/learner_lab.py" run --stage step3 --source "$EDU_WORK/step3/main.c" --bundle "$EDU_ACTIVE" --disk "$EDU_PLATFORM/output/disk-qemu" --receipt "$EDU_WORK/step3/wrong"
```

Expect host1 for the wrong edit; host2 is a setup/binding BLOCKED, not the intended
learning failure. Read wrong.json and wrong.log: actual ID/write/read, target exit
and device_readback check. Explain why edcba986 establishes the wrong write and
why application exit0 cannot pass the fixed oracle. Fix write to12345678, rebuild
with the same build command, then repeat run with receipt EDU_WORK/step3/correct.
Require host0, readedcba987, QNX8 identification, matching source/binary/image/disk
bindings, bounded completion and stopped/reaped QEMU. Stale hash means rebuild,
not replay a saved log. Explain the changed observation and cleanup externally.

## 4. Predict and edit your own /dev/edu

Predict: normal write10 plus cat returns3628800, with one IRQ completion and ack0.
A node existing alone, reference PASS or printed constant does not suffice.

```sh
python3 "$EDU_REPO/scripts/learner_lab.py" init --stage step6 --work "$EDU_WORK/finish"
```

Edit EDU_WORK/finish/main.c: complete dispatch setup, bounded handlers, per-open
snapshots and /dev/edu attachment. Correct the starter IAT lifetime: attach normally
inside the write's factorial transaction (initial unmask before trigger), wait
using _NTO_INTR_WAIT_FLAGS_UNMASK, acknowledge and detach before stdio/dispatch
and on errors. Remove explicit InterruptUnmask after that wait; do not unmask
twice. Do not attach at daemon startup or block an IST in dispatch. Earlier failed
implementations remain preserved. This starter supplies IRQ/factorial scaffolding;
it does not assess all earlier stages from scratch or authorize new native features.

## 5. Observe, diagnose and explain your /dev/edu

Build inside the same legal SDK platform, then stop/reap SDK QEMU before the
exclusive native run on the QEMU host (transfer fresh external bundle if split):

```sh
python3 "$EDU_REPO/scripts/learner_lab.py" build --stage step6 --source "$EDU_WORK/finish/main.c" --out "$EDU_ACTIVE" --sdp-env "$EDU_SDP_ENV" --buildfile "$EDU_PLATFORM/output/build/ifs.build" --bsp-cwd "$EDU_PLATFORM"
flock "$EDU_NATIVE_LOCK" env EDU_NATIVE_LOCK="$EDU_NATIVE_LOCK" EDU_NATIVE_LEASE=granted python3 "$EDU_REPO/scripts/learner_lab.py" run --stage step6 --source "$EDU_WORK/finish/main.c" --bundle "$EDU_ACTIVE" --disk "$EDU_PLATFORM/output/disk-qemu" --receipt "$EDU_WORK/finish/result"
```

Read result.json/result.log. The wrapper starts YOUR daemon, waits for /dev/edu,
writes10 by shell redirection and cats the actual text. Require host0,
write_rc0/read_rc0/result3628800, IRQ completion1/input10/result3628800/ack00000000,
QNX identification, matching build bindings, bounded completion and reaping.
On timeout retain source/build/failure logs, inspect IAT attach/unmask/detach,
change source and rebuild. No reference priming or polling fallback.
Explain device ack versus kernel unmask versus dispatch ownership, and why daemon
termination143 is not graceful lifecycle proof. Record hashes/exact commands.
No full-platform/SSH health, lifecycle, safety, timing, least privilege, broad
portability or independent human acceptance follows. sshd attribution belongs to
a separate traced image; internal cause remains UNVERIFIED, not fixed here.

## Reference appendix — not the learner route

The six historical E1/E2 snapshot lessons, check-reference-step1..6, host model and
qtest are comparison/reference material, never your edited-source acceptance.
[Historical codelab appendix](../codelab/codelab.md),
[capability limits](capabilities.md), [private review](../REVIEW.md).
