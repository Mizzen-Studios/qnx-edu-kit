# Independent final integrity recheck — 2026-11-08

## Result
PASS for all four assigned original findings. No remaining actionable finding identified in this bounded recheck. This is not a full audit or native/platform certification.

Reviewed actual current implementation at EDU 0610fda2ffda125d3e3b4888c74c70ecbcf7eb69 and CANopy 32a4ae17b8401e30590437a68f86f403f802c315. Parent-owned STATUS/REVIEW/claim/generated changes were in progress; these were not part of the implementation recheck. No repository files were edited by this reviewer.

## Finding resolution
- P1 EDU export-by-label: FIXED. scripts/learner_session.py validate_attempt now dispatches by action and native asset presence; every PASS build is independently verified. Native records must have consistent action/label/status/exit and valid existing oracle/source/build/disk bindings. Independent corruption/relabel/status/action mutations all rejected; failed exports have INCOMPLETE.txt and no pack.json.
- P1 CAN unrelated-control isolation falsepositive: FIXED. tools/incident_pack/core.js v2 requires two distinct structured members sharing exact process identity, distinct before/after observations, independent ordered trigger/termination/cofailure observations, and a separate same-identity survivor pair. Query excludes control trigger from the primary kill and does not count the control's recorder as the primary survivor. tools/incident_pack/native.js only infers the known main/joined-observer topology when source lineage matches the actual native/prereq_containment.c SHA256 and the preserved raw samples/ready/kill/waitpid+EOF/post-kill/survivor sequence supports it. Actual preserved capture re-adapts exactly to committed v2; changed-copy omissions/wrong PID/no cofailure/no survivor/ambiguous raw and unknown topology cannot infer isolation. No native program executed.
- P2 EDU stale PASS/current source: FIXED. History is retained but mismatched rows explicitly say HISTORICAL — SOURCE MISMATCH; current stage is CURRENT_STAGE_NOT_VALIDATED. Export includes recomputed current source SHA256 and validation state, retaining historical disk evidence. Independently reproduced source edit and confirmed both UI qualification and exported state.
- P2 EDU browser draft authority: FIXED. Stage-specific authoritative content revisions prevent silently overwriting newly imported CLI notes. Conflicts show authoritative notes and require explicit restore/discard before save/download. Actual Chromium verified restore persists after reload, discard retains CLI notes, legacy drafts require explicit handling, and resolved downloads/imports do not revert notes.

## Actual executions
All commands ran with read-only repositories/toolchain, isolated network/PID, explicit empty allowlisted environment, scratch-only writes, transient systemd MemoryMax=1G CPUQuota=100% TasksMax=200 RuntimeMaxSec=110, timeout=100s, LimitFSIZE=32MiB. Runner: run-focused.sh. No SDK/QEMU/native execution, installation, outbound request, media capture, public action, or C6.

1. EDU: python3 -m unittest discover -s tests -p test_learner_session.py -v — 13/13 PASS (edu-host.log).
2. CAN: node --test tests/incident_pack/core.test.js tests/incident_pack/native.test.js — 59/59 PASS (can-host.log). Includes actual preserved-capture replay and changed-copy negatives, not a new native run.
3. EDU Chromium: node tests/browser_learner_session.cjs /scratch/edu-browser — PASS 1280/768/520/360; draft conflict/restore/discard/legacy/download/import; historical source mismatch; command disclosure/evidence navigation; no overflow/page errors (edu-browser.log).
4. CAN Chromium: node tests/incident_pack/control-browser.cjs — PASS 1280/360; actual v2 four answers/evidence expansion; unrelated surviving control UNKNOWN; missing control isolation UNKNOWN; legacy v1 UNKNOWN; no overflow/errors/external requests (can-browser.log).
5. Independent recheck.py: build-only corrupt binary; valid-native relabel; native status BLOCKED; native action build; relabel+corrupt log all REJECTED. Current-source edit remains exportable only as historical evidence with current stage NOT VALIDATED (mutation-hashes.log).
6. Independent hash-check.py: all 12 EDU receipt-bound files and 26 CAN source/evidence/native-original files SHA256 MATCH (mutation-hashes.log).

## Boundaries retained
Cooperative local evidence is not hostile-host attestation. Environment declarations are not independent native proof. Process-wide cofailure does not prove per-thread death timing. Survivor snapshots do not prove continuity. Historical outcomes remain historical; only scoped host contracts/browser behavior were rechecked. Existing C6 STOPPED, SocketCAN/unproven native/platform/safety/timing boundaries are unchanged.

Logs/harnesses are under workspace/.openclaw/tmp/final-upgrade-independent/. No test failures or harness failures occurred during this recheck.
