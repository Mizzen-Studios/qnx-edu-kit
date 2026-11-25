# QNX trap checker acceptance — 25 November 2026

Implemented five per-step HOST reasoning checks, original source-grounded codelab, strict Python CLI and offline browser worksheet. Entry points: README first content action, Start here, deterministic local site. Uses official QNX codelabs metadata/H2/Duration structure, reviewed at upstream eaddbfbcb271db18645fc760ee411c0293a30d6a; no upstream PR or outreach.

## Actual HOST acceptance

- [Host transcript](host.txt): 178 tests, 176 passed, 2 explicit optional/live skips; no live invocation. Nine new test methods cover every wrong choice/correct/missing, schema/version/hash tampering, duplicate keys, unsupported choices/steps, invalid UTF-8, malformed and oversized input, CLI exit0/1/2, per-step/full scope, deterministic outputs and no learner execution routes.
- [Browser receipt](browser.json): actual Chromium at360/520/768/1280×900, first-screen worksheet link, missing feedback, wrong/correct each step, all-step count, actual download then Python parity, stale-summary clearing, reload reset, codelab navigation, no overflow/page errors/external page requests. Only loopback static HTTP used. Browser and server closed in finally. No managed profiles/cookies touched.
- Four full-page screenshots kept in untracked .openclaw/trap-browser, with [hashes](receipt.json);360px visually inspected and readable. These are HOST UI screenshots, not QNX native evidence. No independent human learning, physical phone or screen-reader acceptance claimed.
- Deterministic site and review packet regenerated and checked; local-link, SDK-redistribution guard and whitespace gates pass. Existing archival pins/FAIL tools/receipts untouched. Historical native source claims remain bounded, not promoted to current tip.

## Failures retained in this report

Initial uppercase upstream README URL returned404; actual lowercase readme/template/example were then read. Several command-construction escaping errors stopped before intended patch dispatch; a JS download newline and a non-ASCII Python bytes literal were caught by syntax/tests and corrected. Initial full HOST suite caught missing review-inventory coverage, the old all-pages-no-JS assumption and incorrect generated-site links. Fixed coverage and exact local worksheet script exception (not a blanket allowance), and generalized docs/site destination mapping; all178 tests then passed. Sandboxed distro Chromium denied file URLs, then failed download copy/cancelled under snap confinement. Retested the full workflow through loopback with the already installed Playwright Chromium binary: all four widths and actual downloads passed. No package/browser installation or guest recovery occurred.

## Limits and reproduction

NativeLab validation **NOT_RUN**. This is formative selected-answer feedback, not a C compiler, runtime simulator, source verifier, anti-cheating system or native receipt validator. Expected observations are teaching scenarios. Catalog digest is content binding only; answers are intentionally readable. Inputs cannot run shell/code. No SDK/QEMU/guest/lease/queue operations, artifacts or secrets. C6 STOPPED, £0. A owns native authority; none used here.

~~~sh
sh verify.sh --host-only
python3 scripts/render_site.py --check
python3 docs/review/build_packet.py --check
python3 scripts/check_traps.py --template
# Optional explicit HOST browser QA: installed playwright or playwright-core + Chromium required.
# Set EDU_QA_PLAYWRIGHT and EDU_QA_CHROMIUM to your existing local installations if needed.
node tests/browser_traps.cjs
~~~

Core implementation milestone f60979a4f97e6fadbce78f12d33583daca6fd151 was pushed. CI status is verified separately against the final pushed tip; no native acceptance is inferred from green Actions.
