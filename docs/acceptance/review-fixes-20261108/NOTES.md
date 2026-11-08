# Independent-review host fixes — 2026-11-08

Baseline bbefa51dd. Fixes only host notebook/export and regression tests; no native
source or learner_lab.py driver change. Historical native receipts remain unchanged.

- Export selects validation by action and native artifacts, not display label.
  Successful standalone builds revalidate source/ELF/startup/IFS hashes; native
  artifacts always invoke the existing independent oracle/build/disk/driver checks.
  Action/stage/status/exit/label inconsistencies fail closed, including HOST relabel,
  BLOCKED relabel of a valid observation, and orphan native logs. Failed exports
  retain INCOMPLETE.txt and never produce pack.json.
- Historical attempt PASS/FAIL remains. Cockpit qualifies each source mismatch and
  reports CURRENT_STAGE_NOT_VALIDATED unless the current edit matches a recorded
  successful own observation. Pack current_sources records source hash/state;
  export rerenders the cockpit, so a forgotten render cannot export stale UI.
  CURRENT_SOURCE_RECORDED_PASS is explicitly recorded evidence, not re-execution.
- Browser drafts carry their authoritative note content hash. Same-base intentional
  drafts survive reload; changed CLI notes and legacy drafts require explicit
  Restore/Discard. CLI values remain visible and saving/downloading is blocked
  until resolution. Identical imported drafts clear harmlessly. Resolution download
  and CLI roundtrip tested: newer authoritative notes do not silently revert.

Evidence:
- initial-repros.log preserves independent pre-fix acceptance bypasses.
- host.log: 31 focused learner tests PASS; artificial fixtures are not QNX evidence.
- browser.log: actual Chromium 1280/768/520/360 x900 PASS, no errors/overflow;
  drafts/save/reload/conflict/restore/discard/legacy/source mismatch/download/import/
  commands/evidence navigation/export. Browser sandbox: independent review
  run-focused.sh, read-only app mounts, unshared network/PID, MemoryMax1G CPU100%,
  TasksMax200 RuntimeMax110s. No media/server/target execution.
- browser-initial-harness.log and browser-second-harness.log preserve two QA-only
  harness mistakes (strict locator with two historic rows; reusing identical source
  text on the second viewport). Corrected locator and unique edit, all sizes passed.
- actual-export.json: original external 55-file pack independently rehashed against
  original manifest 93da42cf3ffeadea342ea9da4585b35b8e62e0a8b2e446ac8be3fc51f130173c;
  all nine real own attempts validated with fixed host validator, all four successful
  build archives checked, both historical wrong/finish FAIL retained, corrected runs
  PASS. Fresh host export of those existing artifacts also has 55 matching hashes.
  verify_actual.py contains executable verification (four positional paths).
- receipt.json binds implementation/test/log hashes. No full suite/site/claim lint
  run in this lane: parent owns reconciliation and packaging gates.

No SDK/QEMU rerun, native source edits, historical repin, C6, media, upload,
publication, deployment, contact, spending or credentials. Local licensed binary,
image and disk remain external; git contains hashes/log receipts only. Host state
is cooperative local evidence, not untrusted-pack authenticity/attestation.
