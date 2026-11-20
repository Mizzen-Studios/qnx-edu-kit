# Historical proof / claim diagnostics

20 November 2026: tools/proof_capture.py and tools/claim_lint.py are HISTORICAL dry-proof audits, not the supported HOST quickstart. Their old frozen assets/pins no longer match living tutorial prose. Both currently exit 1 (FAIL); this failure is retained, not promoted to PASS or hidden by changing validators, pins or exit codes. They now identify their historical scope on stderr.

Do not run --write to reseal the old proof pack after editing current docs. Run ./verify.sh --host-only and deterministic render/review checks for current HOST regression. The public demo and later source-bound coherent journey are separate receipts, not repairs to the old dry proof.
