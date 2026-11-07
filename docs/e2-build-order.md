# E2 build order — private teaching draft

Canonical [capability ledger](capabilities.md): compile, reference-run and learner-run
are distinct. This page describes historical snapshot/reference infrastructure;
the [step3 learner slice](learner-lab.md) executes actual learner edits rather than source-equivalence checking (local native wrong-edit FAIL/corrected-edit PASS). No reference receipt satisfies learner acceptance.

## Start from verified E1

E1 commit 387ba38 records actual fresh native functional acceptance of all six
markers, IAT resource-manager completion, shell 10 → 3628800 and 64-byte polled
DMA. See [receipt](acceptance/native-20261107/receipt.json) and
[serial](acceptance/native-20261107/serial.txt). Target: custom QNX 8.0 x86_64
IFS under QEMU 8.2.2 TCG; QSTI provenance remains unverified. Those files are
historical evidence, not inputs that can satisfy a new live check.

The historical E2 scaffold below did not modify native/ or build a new guest. The separate learner slice now builds and boots edited source. It replaces the
old unconditional-include exercises with readable E1-derived C snapshots.
Steps1–4 stop after their own operation; step5 adds IAT and polled DMA;
step6 is the IAT-backed resource manager. Starter TODOs refuse completion.
Each source compiles separately, not linked together with other main functions.

## 1. Safe host checks

From repository root (Python standard library, shell, make):

```sh
python3 tools/step_sources.py --check
./verify.sh --host-only
python3 scripts/render_site.py --check
```

No host check means a QNX source compiled or ran. The source checker rejects
snapshot drift; it does not execute a C compiler. Host tests do not provide
replacement QNX declarations, fixtures disguised as target output, or SDK files.
The generator's write mode restores reference snapshots; do not run it over
learner edits you want to keep.

## 2. Compile one snapshot at a time — authorized SDP only

Use a separate learner copy and an already initialized licensed SDP 8.0 shell.
Set EDU_OUT to an existing absolute build directory outside the checkout, then:

```sh
test -n "$EDU_OUT" && test -d "$EDU_OUT" || exit 2
n=1 # repeat 1 through 6 in order; inspect each boundary before continuing
qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -Werror \
  -o "$EDU_OUT/step$n-solution" "steps/step$n/solution/main.c" -lpci
qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra \
  -o "$EDU_OUT/step$n-starter" "steps/step$n/starter/main.c" -lpci
```

Starter unused scaffolding warnings are expected until the TODO is completed.
No target success is inferred from compilation. These per-snapshot commands
were exercised for all twelve current snapshots using the licensed SDK. The
[source-bound compile receipt](acceptance/e2-qcc-20261107/receipt.json) records
exit0 and source hashes. Solutions passed -Werror; starter TODOs remain.
This twelve-snapshot receipt is compilation evidence only. Separately edited step3 native execution is recorded; other learner stages are pending.
Do not run QNX executables on the Linux host. Do not run two exclusive PCI
owners simultaneously. Steps1–5 are finite diagnostics; step6 stays in dispatch.
A separately reviewed IFS/boot integration must package any learner executable;
the separate scripts/learner_lab.py build interface invokes qcc/mkifs with your licensed BSP; it does not supply a portable BSP or deployment.

## 3. Recheck the unchanged native reference — owner-controlled target

Only the owner controlling the serialized guest lane supplies EDU_LIVE_BUNDLE
(external manifest/image/disk) and EDU_NATIVE_LEASE=granted. Then:

```sh
make check-reference-step1 # repeat through check-reference-step6 only while authorized
```

Every selected gate first checks source snapshot equivalence, then invokes
scripts/live_verify.py for a NEW accumulated reference boot. The manifest must
match every native source hash and the image checksum, and effective QEMU caps
must be at most 100% CPU, 1 GiB, nice 15. All six gates, complete exit record,
IRQ resource-manager/client and shell output are required for success.
A selected step does not skip later gates. No --transcript/replay option exists.
Missing bundle/lease is BLOCKED, status 2; make may report its own error code.
Reference acceptance does not certify an independently compiled snapshot or
learner edits: changed snapshots are refused before guest launch, and changed
native files require a rebuilt external bundle. Preserve each new raw log and
receipt. Never replace live execution with the historical artifacts above.

scripts/build-target.sh records the existing owner's PRIVATE E1 SDK-guest
recipe, with specific mounted source/buildfile paths and inherited image
infrastructure. It is not a portable setup script and should not be blindly
executed in a new environment. E2 adds no CAN module or CAN teaching dependency;
the inherited E1 runner/image still has unrelated experimental devices. Removing
those from that already-verified image requires a separate native rebuild.

## Remaining gates

Per-snapshot qcc compilation is recorded for all six solutions and six starters.
The separately edited step3 BAR slice has native wrong/fixed evidence; other learner stages and two fresh learners remain pending.
QSTI provenance, full security policy, arbitrary concurrency, timeout/fault
injection, restart/re-probe and physical hardware portability are not claimed.
Durations are private planning estimates, not measured learner completion times.
No SDK/header implementation, target binary/image or claat binary is committed.
