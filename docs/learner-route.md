# Canonical learner route: predict → edit → observe → diagnose → explain

**Start here: step3 first, then your own /dev/edu.** Private conditional acceptance;
Nov8 scoped upgrades authorized; no new council acceptance. No reference PASS transfers to your edits. Existing automated
native observations are not fresh SDK installation, second-SDK portability or
independent human acceptance. C6 STOPPED; SocketCAN UNVERIFIED. No publication.

Use the [local own-source cockpit](learner-cockpit.md) to save your prediction, diagnosis and explanation, retain every build/run attempt and export your own source-bound pack. It uses this same CLI and stage oracles; it never executes shell commands from a browser or imports reference PASS as learner work. The parameterized single-host setup planner is documented there; native policy additions remain separately gated.

## 0. Choose legal inputs and preflight

Use Bash and Python3 on a licensed **Linux x86_64 single host** where possible.
Clone anywhere and cd into that clone. Override EDU_SDP_ENV with your legal SDK.
All other paths have external user-owned defaults; choose a new EDU_WORK for each
attempt. No SDK/artifacts inside any checkout; snippet paths must have no spaces.

```sh
export EDU_REPO="${EDU_REPO:-$(pwd -P)}"
export EDU_WORK="${EDU_WORK:-$HOME/edu-learner-$(date -u +%Y%m%dT%H%M%SZ)}"
export EDU_SDP_ENV="${EDU_SDP_ENV:-$HOME/qnx800/qnxsdp-env.sh}"
export EDU_PLATFORM="${EDU_PLATFORM:-$EDU_WORK/platform}"
export EDU_ACTIVE="${EDU_ACTIVE:-$EDU_WORK/step3/bundle}"
export EDU_QEMU="${EDU_QEMU:-$(command -v qemu-system-x86_64)}"
export EDU_NATIVE_LOCK="${EDU_NATIVE_LOCK:-$HOME/.local/state/edu-native-test.lock}"
export EDU_SOURCE="$EDU_WORK/step3/main.c"
export EDU_SNIPPET="$EDU_REPO/scripts/learner-step3.build.in"
mkdir -p "$(dirname "$EDU_NATIVE_LOCK")"
export PATH="$(dirname "$EDU_QEMU"):$PATH"
python3 "$EDU_REPO/scripts/learner_lab.py" --help
python3 "$EDU_REPO/scripts/learner_clean_preflight.py" --sdp-env "$EDU_SDP_ENV" --fresh-work "$EDU_PLATFORM"
```

Run the preflight **inside your already licensed Linux x86_64 SDK host**, not
merely the ARM QEMU host. A single-host reader runs it locally; split hosts run it
after copying the original script. A missing ARM-host SDK is only a negative check,
not evidence that your existing SDK in another host is unavailable. It checks compiler/image tools and stock startup/kernel/
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

Before notebook initialization, optionally run the read-only setup planner with
--work "$EDU_WORK" and --probe-sdk. It requires a fresh work directory. If you
already used README init, do not rerun that planner against your existing work:
retain this notebook and use the stock-platform preflight above (it checks the
fresh EDU_PLATFORM, not the notebook directory). Never delete a notebook to make
a setup probe pass. The single-host planner and split-host checks are alternatives,
not a second initialization.

## 1. Predict and edit step3

Write a prediction externally: complement32(12345679)=edcba986, but the fixed
stage expects write12345678/readedcba987. The wrong variant must fail even if your
application incorrectly returns0. Then create your notebook only if README has not already initialized it:

```sh
if test -f "$EDU_WORK/session.json"; then
  python3 "$EDU_REPO/scripts/learner_session.py" render --work "$EDU_WORK"
else
  python3 "$EDU_REPO/scripts/learner_session.py" init --work "$EDU_WORK"
fi
```

Open the printed cockpit.html. Save your prediction, download notes and run its
notes import command before building. Record diagnosis/explanation there after
each observation. Both starters already exist; never reinitialize them.

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

The original `scripts/learner_bootstrap.sh` below supports stock-platform setup; it is not an SDK installer. Narrow tested configuration:
SDP8, Generic x86_64 BSP0.0.1.00050T202311201204L,
mkqnximage0.5.0.00132T202605281115L, QEMU8.2.2 pc TCG. Missing compatible legal
SDP/BSP or matching disk means **BLOCKED**, not second-install portability PASS.
Existing SDK reuse is not a fresh SDK install.

### Default: single licensed Linux x86_64 host

Finish your step3 edit first; preflight must pass. The helper uses EDU_SOURCE and
EDU_SNIPPET from section0 and creates the preseed, fresh platform and snippets.
The preseed is NOT learner completion. It does not launch a Linux VM.


```sh
flock "$EDU_NATIVE_LOCK" bash "$EDU_REPO/scripts/learner_bootstrap.sh"
```

No SDK VM, guest swap, shared mount or host-queue service is required on an ordinary
single host. Stop on build failure and preserve logs; never substitute owner images.
Skip the optional section below and continue at "Now replace the preseed".

### Optional: constrained split-host SDK VM only

The following is environment-specific, NOT a single-host requirement.

Keep the stock kernel unmodified. On the constrained SDK guest, arrange authorized
1GiB disk-backed guest swap and an isolated transient guest build service before
linking:512MiB without swap previously OOMed. Do not lift caps or strip the kernel.
Stop on OOM, transport loss or nonterminal service status. The following explicit preparation is required; historical launchers are not shortcuts.
#### Split-host mapping and isolated service

Choose EDU_SHARED_HOST (external directory on the QEMU host) and EDU_SHARED_GUEST
(the same directory as mounted inside Linux). Prove the mapping by writing a nonce
on the host and reading identical bytes inside the guest before copying scripts.
For the existing private VM only, the parent share is mounted at /mnt/host; this
is an environment mapping, not a portable assumption. EDU_WORK may be that shared
mapping; EDU_PLATFORM and EDU_ACTIVE should be guest disk directories, not 9p.
Copy learner_lab.py, learner_clean_preflight.py, learner_bootstrap.sh and
learner-step3.build.in from this exact revision into the chosen share. Copy only
original scripts and your edited C. At the guest set EDU_SOURCE to the wrong
main.c, EDU_SNIPPET to that copied fragment, EDU_SDP_ENV, EDU_PLATFORM and
EDU_ACTIVE to their guest paths; host paths are not interchangeable.

Choose EDU_SWAP on the Linux guest disk and EDU_BUILD_USER as the existing licensed
user. As guest root, reactivate the existing authorized 1GiB file (no overwrite,
no fstab edit); check disk, owner, size and active state first:


define these variables in Bash before running:

```sh
export EDU_SWAP=/absolute/guest-disk/existing.swap
export EDU_BUILD_USER=existing-licensed-user
export EDU_UNIT=learner-bootstrap-unique
export EDU_JOB=/absolute/guest-visible-share/job.sh
export EDU_LOG=/absolute/guest-visible-share/build.log
df -h "$(dirname "$EDU_SWAP")"
stat "$EDU_SWAP"
test "$(stat -c %s "$EDU_SWAP")" = 1073741824
swapon --show
if ! swapon --show=NAME --noheadings | grep -Fx "$EDU_SWAP"; then swapon "$EDU_SWAP"; fi
free -m
systemctl is-active host-queue.service
systemctl show host-queue.service -p NRestarts
systemd-run --unit="$EDU_UNIT" --property="User=$EDU_BUILD_USER" --property=OOMPolicy=stop --property=RuntimeMaxSec=1830 --property="StandardOutput=file:$EDU_LOG" --property=StandardError=inherit /usr/bin/timeout --kill-after=15 1800 /bin/bash "$EDU_JOB"
# Wait for terminal inactive/failed state; active + status0 is NOT success.
systemctl show "$EDU_UNIT" -p ActiveState -p Result -p ExecMainCode -p ExecMainStatus -p MainPID
systemctl show host-queue.service -p ActiveState -p NRestarts
```

EDU_JOB is a user-owned Bash file OUTSIDE EDU_PLATFORM. It exports the chosen
variables, runs the standalone preflight (retain JSON), then calls
`bash "$EDU_SHARED_GUEST/learner_bootstrap.sh"` instead of manually repeating the
stock/preseed/snippet block above. It must use set -eo pipefail and stop at the
first failure. The guest service must terminate Result=success, ExecMainStatus=0,
MainPID=0; retain its log externally and hash it, do not commit proprietary
compiler/platform output. If swap is absent, stop for authorized disk-swap setup;
no automatic creation, installation or cap increase is provided. Reuse the same
isolated-service pattern for each learner build. Set HOME for the licensed user.
For this optional split route only, the native commands below are the single-host
notebook form. Use these equivalent standalone actions inside the SDK guest and
on the QEMU host respectively; do not invoke a notebook wrapper whose paths point
at the other host. Preserve source and all numbered own receipts externally:

```sh
# SDK guest, existing isolated service (STAGE=step3 or step6, chosen source/bundle):
python3 "$EDU_SHARED_GUEST/learner_lab.py" build --stage "$STAGE" --source "$EDU_SOURCE" --out "$EDU_ACTIVE" --sdp-env "$EDU_SDP_ENV" --buildfile "$EDU_PLATFORM/output/build/ifs.build" --bsp-cwd "$EDU_PLATFORM"
# Stop/reap SDK guest; transfer original own bundle and matching disk externally.
# QEMU host, actual caller-held sole lock; pick a fresh receipt basename each time:
flock "$EDU_NATIVE_LOCK" env EDU_NATIVE_LOCK="$EDU_NATIVE_LOCK" EDU_NATIVE_LEASE=granted python3 "$EDU_REPO/scripts/learner_lab.py" run --stage "$STAGE" --source "$EDU_SOURCE" --bundle "$EDU_ACTIVE" --disk "$EDU_PLATFORM/output/disk-qemu" --receipt "$EDU_RECEIPT"
```

This split path retains the original direct source-bound oracle but does not
pretend that cross-host standalone observations are notebook-invoked attempts.
Keep notebook notes and standalone packs separately labeled; no reference receipt
import, no single-host readiness claim. The ordinary single-host route below uses
learner_session build/run and automatically archives attempts.

The Linux controller is existing environment infrastructure, not supplied by this
repository; its supported console/transport must run these commands as root and
collect terminal service status. Stop/reap its VM before each native run.

Now replace the preseed with a freshly compiled source-bound bundle:

```sh
flock "$EDU_NATIVE_LOCK" python3 "$EDU_REPO/scripts/learner_session.py" build --work "$EDU_WORK" --stage step3 --sdp-env "$EDU_SDP_ENV" --buildfile "$EDU_PLATFORM/output/build/ifs.build" --bsp-cwd "$EDU_PLATFORM"
```

Preserve the entire bundle externally before replacing it with another variant.
For the optional split route, use the original standalone learner_lab build/run
commands instead of notebook CLI orchestration across hosts unless your full
notebook paths and scripts are mapped identically. Transfer that bundle and matching output/disk-qemu externally,
and set EDU_ACTIVE/EDU_PLATFORM to the QEMU-host copies. The current edited source
must also match. Never substitute a historical binary or edit manifest hashes.

## 3. Observe, diagnose, fix and explain step3

Stop/reap the SDK guest; hold the exclusive native lease on the QEMU host:

```sh
flock "$EDU_NATIVE_LOCK" env EDU_NATIVE_LOCK="$EDU_NATIVE_LOCK" EDU_NATIVE_LEASE=granted python3 "$EDU_REPO/scripts/learner_session.py" run --work "$EDU_WORK" --stage step3 --disk "$EDU_PLATFORM/output/disk-qemu"
```

Expect host1 for the wrong edit; host2 is a setup/binding BLOCKED, not the intended
learning failure. Read the numbered attempts/*-step3-run/native.json and native.log: actual ID/write/read, target exit
and device_readback check. Explain why edcba986 establishes the wrong write and
why application exit0 cannot pass the fixed oracle. Fix write to12345678, rebuild
with the same build command, then repeat run with a new automatically numbered attempt; no overwrite.
Require host0, readedcba987, QNX8 identification, matching source/binary/image/disk
bindings, bounded completion and stopped/reaped QEMU. Stale hash means rebuild,
not replay a saved log. Explain the changed observation and cleanup externally.

## 4. Predict and edit your own /dev/edu

Predict: normal write10 plus cat returns3628800, with one IRQ completion and ack0.
A node existing alone, reference PASS or printed constant does not suffice.

```sh
python3 "$EDU_REPO/scripts/learner_session.py" render --work "$EDU_WORK"
export EDU_FINISH_SOURCE="$EDU_WORK/step6/main.c"
```

Edit EDU_WORK/step6/main.c: complete dispatch setup, bounded handlers, per-open
snapshots and /dev/edu attachment. Correct the starter IAT lifetime: attach normally
inside the write's factorial transaction (initial unmask before trigger), wait
using _NTO_INTR_WAIT_FLAGS_UNMASK, acknowledge and detach before stdio/dispatch
and on errors. Remove explicit InterruptUnmask after that wait; do not unmask
twice. Do not attach at daemon startup or block an IST in dispatch. Earlier failed
implementations remain preserved. The notebook already created this starter; save/import your step6 prediction.
This starter supplies IRQ/factorial scaffolding;
it does not assess all earlier stages from scratch or authorize new native features.

## 5. Observe, diagnose and explain your /dev/edu

The notebook builds to EDU_WORK/step6/bundle. Repoint the existing learner
fragment before the step6 build (this changes no SDK/BSP installation):

```sh
export EDU_ACTIVE="$EDU_WORK/step6/bundle"
# Preseed only, never completion: the following real notebook build replaces it.
mkdir -p "$EDU_ACTIVE"
cp "$EDU_WORK/step3/bundle/learner_bin" "$EDU_ACTIVE/learner_bin"
printf '#!/bin/sh\nexit 2\n' > "$EDU_ACTIVE/learner-start.sh"
sed "s|@OUT@|$EDU_ACTIVE|g" "$EDU_SNIPPET" > "$EDU_PLATFORM/local/snippets/ifs_files.learner"
# Recompute the generated buildfile using the existing installed platform tools.
flock "$EDU_NATIVE_LOCK" bash -c 'set -eo pipefail; source "$EDU_SDP_ENV"; cd "$EDU_PLATFORM"; mkqnximage --build'
```

Build inside the same legal SDK platform, then stop/reap SDK QEMU before the
exclusive native run on the QEMU host (transfer fresh external bundle if split):

```sh
flock "$EDU_NATIVE_LOCK" python3 "$EDU_REPO/scripts/learner_session.py" build --work "$EDU_WORK" --stage step6 --sdp-env "$EDU_SDP_ENV" --buildfile "$EDU_PLATFORM/output/build/ifs.build" --bsp-cwd "$EDU_PLATFORM"
flock "$EDU_NATIVE_LOCK" env EDU_NATIVE_LOCK="$EDU_NATIVE_LOCK" EDU_NATIVE_LEASE=granted python3 "$EDU_REPO/scripts/learner_session.py" run --work "$EDU_WORK" --stage step6 --disk "$EDU_PLATFORM/output/disk-qemu"
```

Read the new numbered attempts/*-step6-run/native.json and native.log. The wrapper starts YOUR daemon, waits for /dev/edu,
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

Videos are deferred until final feature freeze, final verification and independent gate, then separate Olly OK. They are not the current blocker.
