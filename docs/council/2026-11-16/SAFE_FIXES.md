# EDU safe fixes — 16 November 2026

Scope: owner-authorized host foundation maintenance only. Baseline main/origin
`3438bdf9647be69afaeb7e6735754f9cc0a28763`; existing untracked `.openclaw/`
preserved. No native execution or new acceptance claim.

## Root cause and repair

Publication commit `76c513cf25b36f93d0c189b2fda61a29bac5094d` changed
README, codelab, JUDGES and the companion reference without regenerating
site/review outputs. Reproduced baseline: 143 tests, 139 pass, 2 skip,
1 failure (review inventory), 1 error (site freshness).

Regenerated current HTML and review appendix to a fixed point; changed only
the renderer title/header from private-draft labels to public-tutorial labels
consistent with current source. Historical receipt prose remains historical.
`make refresh-docs` now orders render -> review inventory -> render -> both
read-only freshness checks. Run it twice and compare tracked bytes.
No tests, workflows, native source, learner admission or historical pins changed.

## Validation and boundaries

Observed locally: full unchanged 143-test suite (141 pass, 2 opt-in skips),
redistribution guard, source-generator check, renderer and review checks PASS.
Two complete freshness runs produced byte-identical tracked diffs. Full verify
with both external-bundle variables absent exited2 with the existing BLOCKED
missing-bundle diagnostic after the same 143 tests passed. Protected source,
receipt, dry-pack, test and workflow paths are byte-identical to baseline.
Clean remote checkout and exact-tip GitHub host-foundation results follow in
the final parent handoff; no CI result is inferred from these local checks.

**Additional pre-existing frozen-copy gate remains denied, not suppressed:**
`python3 tools/proof_capture.py` and `python3 tools/claim_lint.py` detect
T01 changed frozen assets `codelab/codelab.md` and `README.md` (proof check
also reports its historical `report.json` stale). These current
publication files differ from the old instruction-copy freeze. Original native
pins, dry pack, script and historical report remain unchanged. No proof
validator is relaxed and no fresh recording or tutorial acceptance is inferred.
Changing those bindings requires separate scope clarification; this repair
does not claim all proof gates green. Current claim inventory records FAIL.

No QEMU/SDK/licence/media/Devpost/YouTube/visibility/outreach/spend work.
C6 untouched. Material features, new lessons/studies, native handoffs and
independent learner admission remain outside this maintenance milestone.
