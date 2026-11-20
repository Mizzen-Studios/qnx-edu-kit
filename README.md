# edu-kit — learn QNX by diagnosing a wrong edit

A learner-owned PCI-to-/dev/edu lab: wrong edit FAIL despite application exit 0 → corrected PASS → write 10 / read 3628800. [Watch the demo](https://youtu.be/hI8-QtwMg8A).

## Five-minute HOST ONLY judge path

No QNX hardware, SDK, image or QEMU required. From the repository root with Python 3, POSIX shell and GNU make:

1. Read [the source-bound wrong/correct/finish journey](docs/JUDGES.md).
2. Inspect [the one-notebook checklist](docs/coherent-journey.md) and [codelab](codelab/codelab.md); reading does not execute native commands.
3. Run HOST checks only:

~~~sh
./verify.sh --host-only
python3 scripts/render_site.py --check
~~~

Then open [the local tutorial](docs/site/index.html). Predictions and HOST provenance checks are not QNX runtime proof or independent human learning acceptance.

## Status — 20 November 2026

| Area | Evidence-backed state |
|---|---|
| Repository | PUBLIC; historical private/visibility-pending wording is stale. No visibility change performed here. |
| HOST regression | 164 Python tests: 162 passed, 2 skipped; host-only, not target acceptance. |
| Coherent recorded journey | Historical source 769a4c9: wrong FAIL/app0 → corrected PASS → own normal I/O finish; reused pinned stock image. |
| Independent stock route | Implemented at 28daa16; fresh stock build BLOCKED by unchanged 2GiB host / 64MiB reserve gate; new native journey NOT_RUN. |
| Historical diagnostics | Old proof/claim scripts FAIL against their historical pins. See [diagnostic scope](docs/HISTORICAL-DIAGNOSTICS.md); not repaired by weakening gates. |
| Limits | Independent human / second SDK / platform health UNVERIFIED; C6 STOPPED, SSH / SocketCAN UNVERIFIED. |

**Demo in QEMU; not a safety or latency claim.** Native evidence remains bound to its recorded source/image, not the current documentation tip.

[Current independent-stock result](docs/acceptance/independent-stock-20261119/RESULT.md) · [Canonical licensed learner route](docs/learner-route.md) · [Capability ledger](docs/capabilities.md) · [Dated history](docs/HISTORY.md) · [Path preservation policy](docs/PATHS.md).

Apache-2.0; Python stdlib only. No licensed SDK, image, secret or binary is distributed. Missing legal setup is BLOCKED; HOST checks cannot replace it. Native/full verify is not part of the judge path.
