# Canonical learner route — supported split-host topology

**Licensed Linux x86_64 SDK guest builds → STOP and REAP guest → native QNX on capped HOST QEMU.** Hold the sole host lease across this sequence. Never run native QEMU inside the SDK guest.

Single-host: **BLOCKED_NATIVE_TIMEOUT**, [Nov9 receipt](acceptance/choice-a-20261109/receipt.json). Package/user-bus setup passed, but native attempts timed out before learner markers/appRC. Root cause **UNVERIFIED**; nested emulation is not established as the cause. No more single-host retries, timeout tuning or cap increases. C6 STOPPED; private £0; no video/publication/SDK login or activation.

## Recorded journey — not a rerun at this tip

[Nov7 supported bootstrap](acceptance/bootstrap-final-20261107/NOTES.md): fresh stock platform, wrong FAIL/app0 → corrected PASS → own /dev/edu10→3628800+IRQack. [Nov8 wrapper journey](acceptance/wrapper-20261108/NOTES.md): SDK-guest builds and host-native runs with explicit environment path handoff.

- [Wrong native](acceptance/wrapper-20261108/wrong-native.json): fixed oracle FAIL despite target exit0.
- [Correct native](acceptance/wrapper-20261108/correct-native.json): actual12345678→edcba987, PASS.
- [Own /dev/edu](acceptance/wrapper-20261108/finish-native.json): write10/read3628800, IRQcompletion1/ack0, PASS.
- [Original own export inventory](acceptance/wrapper-20261108/export-manifest.json), [55-file validation](acceptance/wrapper-20261108/export-validation.json). Manifest SHA25693da42cf3ffeadea342ea9da4585b35b8e62e0a8b2e446ac8be3fc51f130173c.

Original source/ELF/IFS/startup/disk/driver bindings stay in immutable receipts. Historical PASS does not validate new edits; documentation/host CI does not rerun QNX. No second-SDK, human learner, physical portability, performance, safety or full-platform/SSH-health acceptance.

## 0. Separate host and guest paths

Host: this checkout, Python3, Bash, flock, systemd-run and QEMU. Guest: existing licensed Linux x86_64 SDP8/compatible installed Generic x86_64 BSP with qcc/mkifs/mkqnximage. Missing legal inputs means BLOCKED, not SDK install/activation or substitution of old binaries.

On **QEMU host**, choose fresh external notebook:

~~~sh
export EDU_REPO="$(pwd -P)"
export EDU_WORK="${EDU_WORK:-$HOME/edu-learner-$(date -u +%Y%m%dT%H%M%SZ)}"
export EDU_NATIVE_LOCK="$HOME/.local/state/edu-native-test.lock"
export EDU_QEMU="$(command -v qemu-system-x86_64)"
mkdir -p "$(dirname "$EDU_NATIVE_LOCK")"
export PATH="$(dirname "$EDU_QEMU"):$PATH"
"$EDU_QEMU" --version
command -v flock systemd-run
systemctl --user show-environment >/dev/null
if test -f "$EDU_WORK/session.json"; then
  python3 "$EDU_REPO/scripts/learner_session.py" render --work "$EDU_WORK"
else
  python3 "$EDU_REPO/scripts/learner_session.py" init --work "$EDU_WORK"
fi
~~~

If README already initialized EDU_WORK, keep that value instead of assigning a new one. Open cockpit.html: predict, download notes and import via its local notes command. Both starters exist; do not reinitialize. Notebook is HOST notes/export; split standalone native receipts do **not** automatically become notebook attempts. No receipt import exists.

Choose EDU_SHARED_HOST and EDU_SHARED_GUEST for the same authorized external handoff directory; prove identical nonce bytes across mapping. Existing lab /mnt/host is environment-specific. Copy original learner_lab.py, learner_clean_preflight.py, learner_bootstrap.sh and learner-step3.build.in plus your edited C to the guest-visible share. No SDK/binary/image in git. Guest and host paths are not interchangeable.

Keep an actual owner terminal/control process holding the host flock from before SDK launch through native cleanup. All QEMU: effectiveCPU100%, MemoryMax1GiB, nice15,1vCPU/512MiB. Use existing legitimate capped SDK controller, not legacy uncapped launchers. Repository does not supply that controller/transport; stop if authorized access is absent.

## 1. Predict and edit step3 on host

Edit EDU_WORK/step3/main.c, not solution/reference sources. Complete BAR TODO: per-thread I/O level1, metadata, memory BAR0 extent≥0x1000, uncached mapping, actual IDr[0], volatile write/readr[1]. Preserve errors/unmap/detach. Emit exactly one parser row with actual register values (not constants):

~~~c
printf("LEARNER_MMIO id=%08x write=%08x read=%08x\n", id, written, observed);
~~~

Use real variables from your implementation. Require EDU ID010000ed; reject wrong ID/BAR bounds.

Predict wrong12345679→edcba986. Program may check that complement and exit0, but fixed stage requires12345678→edcba987. Wrong observation must FAIL despite app0; printing PASS is insufficient. Save prediction, then diagnosis/explanation after observing.

## 2. Build only inside existing licensed SDK guest

Choose guest absolute paths: EDU_GUEST_LAB (copied standalone learner_lab.py), EDU_GUEST_SOURCE (your copied C), EDU_GUEST_BUNDLE (fresh output), EDU_PLATFORM (fresh guest-disk platform), EDU_SDP_ENV, EDU_SNIPPET (copied original fragment). No spaces in snippet paths. Verify guest source SHA256 equals current host source.

Inside **SDK guest**, existing licensed user:

~~~sh
export EDU_SOURCE="$EDU_GUEST_SOURCE"
export EDU_ACTIVE="$EDU_GUEST_BUNDLE"
python3 "$EDU_SHARED_GUEST/learner_clean_preflight.py" --sdp-env "$EDU_SDP_ENV" --fresh-work "$EDU_PLATFORM"
bash "$EDU_SHARED_GUEST/learner_bootstrap.sh"
python3 "$EDU_GUEST_LAB" build --stage step3 --source "$EDU_GUEST_SOURCE" --out "$EDU_GUEST_BUNDLE" --sdp-env "$EDU_SDP_ENV" --buildfile "$EDU_PLATFORM/output/build/ifs.build" --bsp-cwd "$EDU_PLATFORM"
~~~

Bootstrap uses installed mkqnximage, fresh stock kernel/disk and learner-only snippets; preseed is not completion. Recorded versions: SDP8/Generic x86_64 BSP0.0.1.00050T202311201204L, mkqnximage0.5.0.00132T202605281115L; native host QEMU8.2.2 pcTCG. Existing SDK reuse is not new installation.

### Constrained guest prerequisites

On512MiB SDK guest, inspect/reactivate only existing authorized1GiB disk swap: owner/size/free-space checks first; no overwrite/fstab/cap change, stop if absent. Platform/bundle on guest disk, not9p. Existing authorized guest root runs user-owned job via isolated transient service, HOME set for licensed user; keep queue separate:

~~~sh
# Guest root; chosen external job/log and existing licensed user:
systemd-run --unit="$EDU_UNIT" --property="User=$EDU_BUILD_USER" --property=OOMPolicy=stop --property=RuntimeMaxSec=1830 --property="StandardOutput=file:$EDU_LOG" --property=StandardError=inherit /usr/bin/timeout --kill-after=15 1800 /bin/bash "$EDU_JOB"
# Wait for terminal state, not active/status0:
systemctl show "$EDU_UNIT" -p ActiveState -p Result -p ExecMainStatus -p MainPID
systemctl show host-queue.service -p ActiveState -p NRestarts
~~~

Require inactive/Resultsuccess/ExecMainStatus0/MainPID0, queue active/no restart. EDU_JOB exports guest variables, set -eo pipefail, exact guest build sequence above. Retain logs externally; stop on OOM/failure/transport uncertainty. Do not substitute notebook build pointing to host paths.

## 3. Transfer own bundle/disk, STOP/REAP guest, observe on HOST

Before shutdown copy whole fresh bundle and matching output/disk-qemu through authorized share with source/binary/image/startup/disk SHA256 inventory. Preserve immutable per-attempt copies before rebuilding. Licensed bytes stay external.

**STOP and REAP SDK guest with existing controller; collect terminal exit and prove no SDK QEMU process.** Retain host lease. Set EDU_HOST_SOURCE to matching source snapshot, EDU_HOST_BUNDLE to transferred bundle, EDU_HOST_DISK to transferred disk, EDU_RECEIPT to new external basename. Compare transfer hashes with guest inventory. **QEMU host only**:

~~~sh
# Inside existing owner-held sole lease, NEVER SDK guest:
env EDU_NATIVE_LOCK="$EDU_NATIVE_LOCK" EDU_NATIVE_LEASE=granted python3 "$EDU_REPO/scripts/learner_lab.py" run --stage step3 --source "$EDU_HOST_SOURCE" --bundle "$EDU_HOST_BUNDLE" --disk "$EDU_HOST_DISK" --receipt "$EDU_RECEIPT"
~~~

Driver checks held lease/effective caps;1cpu/512MiB/snapshot disk; stops/reaps native QEMU. Wrong host1 with targetRC0/readedcba986 is intended negative; host2 is BLOCKED, timeout/appRCabsent is not intended negative. Read native.json/native.log, not app PASS.

Fix source12345678; restart only the serialized SDK build phase. Bootstrap/preflight fresh-platform creation runs once, not against an existing platform. Preserve the wrong bundle/disk first. For corrected step3 retain the active snippet path and rerun standalone build with the corrected source; archive its fresh bundle/disk before further changes. Alternatively choose a fresh platform/bundle and bootstrap it. Transfer verified matching bytes, STOP/REAP guest again, host run with **new receipt basename**. Require host0/readedcba987/QNX8/source+ELF+IFS+disk bindings/bounded completion/reaped. Never reuse historical PASS/edit manifests. Reading route is not authorization for new runs.

## 4. Own /dev/edu finish — same split barrier

Save step6 prediction; complete starter dispatch/iofunc, bounded handlers, per-open snapshots and final /dev/edu registration. Transaction owns IAT: initial unmask before trigger, InterruptWait with _NTO_INTR_WAIT_FLAGS_UNMASK, device acknowledge, detach before stdio/dispatch; no redundant InterruptUnmask/startup IST blocked in dispatch. No polling fallback/reference priming.

In SDK guest select step6 source/bundle, repoint snippet before regeneration. Temporary preseed is not acceptance:

~~~sh
# SDK guest only; fresh step6 source/bundle selected:
mkdir -p "$EDU_GUEST_BUNDLE"
cp "$EDU_STEP3_GUEST_BUNDLE/learner_bin" "$EDU_GUEST_BUNDLE/learner_bin"
printf '#!/bin/sh\nexit 2\n' > "$EDU_GUEST_BUNDLE/learner-start.sh"
sed "s|@OUT@|$EDU_GUEST_BUNDLE|g" "$EDU_SNIPPET" > "$EDU_PLATFORM/local/snippets/ifs_files.learner"
bash -c 'set -eo pipefail; source "$EDU_SDP_ENV"; cd "$EDU_PLATFORM"; mkqnximage --build'
python3 "$EDU_GUEST_LAB" build --stage step6 --source "$EDU_GUEST_SOURCE" --out "$EDU_GUEST_BUNDLE" --sdp-env "$EDU_SDP_ENV" --buildfile "$EDU_PLATFORM/output/build/ifs.build" --bsp-cwd "$EDU_PLATFORM"
~~~

Set EDU_SDP_ENV, EDU_PLATFORM, EDU_SNIPPET and all guest paths explicitly in the job; the snippet path must match the selected bundle. Same isolated service/hash handoff. **STOP/REAP SDK guest**, then host-only section3 standalone command with --stage step6 and matching step6 source/bundle/disk/new receipt. Require real shell write10/read3628800, IRQcompletion1/input10/result3628800/ack00000000, bindings/reaping. Daemon termination143 is not graceful lifecycle proof. Preserve failures; explain device ack/kernel unmask/dispatch ownership.

## 5. Honest evidence/export boundaries

Notebook notes export is HOST unless its own wrapper actually recorded observations. Split standalone artifacts stay in separately labeled external pack: own C/history, every build manifest/ELF/IFS/startup, native receipts/logs, original matching disks and SHA256 inventory. Licensed bytes outside git; no upload/forged notebook records/reference import. Nov8 wrapper export used explicitly mapped existing environment, not arbitrary identical guest/host paths.

Single-host remains BLOCKED_NATIVE_TIMEOUT/rootcauseUNVERIFIED. Nov9 failure export is valid failure evidence, not completion. No more single-host runs/tuning. Human learner/secondSDK/physical portability/lifecycle/timing/path policy/full-platform health unverified.

## Historical reference appendix — not another entry route

[Historical codelab](../codelab/codelab.md), six E1/E2 snapshots, check-reference-step1..6, host model/qtest remain reference. [Capability ledger](capabilities.md), [cockpit help](learner-cockpit.md), [private review](../REVIEW.md). No video; C6 STOPPED; private £0; independent review required.
