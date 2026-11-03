# Foundation verification — 2026-11-03 UTC

Environment: Ubuntu 24.04.5 LTS ARM64, Python 3, GNU make; no /dev/kvm, qemu-system-x86_64 or qcc present. No SDK or image downloaded. These are host framework results, not QNX functional/performance evaluations.

| Command | Observed outcome |
|---|---|
| PYTHONDONTWRITEBYTECODE=1 ./verify.sh --host-only | exit 0; guard PASS, 11 host tests OK, all six live checks SKIP |
| PYTHONDONTWRITEBYTECODE=1 ./verify.sh | exit 1; host checks OK, six BLOCKED, full verification BLOCKED |
| make check-step1 through check-step6 | each nonzero (make exit 2), each reports BLOCKED |
| sh -n verify.sh scripts/check-step.sh scripts/check-no-sdk.sh | exit 0 |
| git diff --check | exit 0 |

Negative tests cover SDK/image/archive paths, renamed executable/archive signatures, markers beyond prefix/across chunks, symlinks, ignored/untracked artifacts, missing scan root, invalid steps and fabricated environment claims. Temporary fixtures contain only synthetic text/signature bytes, never SDK files or usable images, and are cleaned automatically. No register model or target-code test is present.

Tests also check all 12 starter/solution task documents and Apache-2.0 text exist. These structural checks prove no target behavior. CI workflow is provided but remote execution must be independently observed; local results do not establish GitHub Actions success.

Outstanding: all live ledger rows; claat export; diagrams; QNX APIs/driver/policy/build/deploy; mandatory target capture; two clean-machine learner runs. macOS and Windows UNTESTED.
