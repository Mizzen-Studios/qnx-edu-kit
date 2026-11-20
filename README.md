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

## Evidence at a glance

| Evidence route | State |
|---|---|
| Recorded journey | Bounded source-bound observations; not current live health. |
| HOST checks | 166 Python tests (164 passed / 2 skipped); not native acceptance. |
| Native / reproduction scope | [Complete current status and limits](STATUS.md); separate licensed setup required. |
| Repository | PUBLIC; earlier private-state wording is stale. |

**Demo in QEMU; not a safety or latency claim.** Native evidence remains bound to its recorded source/image, not the current documentation tip.

[Current independent-stock result](docs/acceptance/independent-stock-20261119/RESULT.md) · [Canonical licensed learner route](docs/learner-route.md) · [Capability ledger](docs/capabilities.md) · [Dated history](docs/HISTORY.md) · [Path preservation policy](docs/PATHS.md).

Apache-2.0; Python stdlib only. No licensed SDK, image, secret or binary is distributed. Missing legal setup is BLOCKED; HOST checks cannot replace it. Native/full verify is not part of the judge path.

## Why QNX

The lesson uses QNX PCI attachment, MMIO, interrupt acknowledgement, a same-owner private pulse and resource-manager read/write handling at /dev/edu. Wrong and corrected observations teach why application exit 0 alone is not a device oracle.

## How we used AI

Developed with an AI coding agent under human direction: implementation, tests, documentation and evidence review were AI-assisted. HOST checks and recorded native receipts support only their stated scope; AI output is not independent human learner validation, attestation or QNX acceptance.
