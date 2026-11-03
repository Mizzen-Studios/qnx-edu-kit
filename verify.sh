#!/bin/sh
# Host-only checks can succeed; full verification cannot until live checks exist.
set -eu
cd "$(dirname "$0")"
mode=${1-}
case "$mode" in ''|--host-only) ;; *) echo 'usage: verify.sh [--host-only]' >&2; exit 64 ;; esac
make host-check
if [ "$mode" = '--host-only' ]; then
    echo 'SKIP: all six live QNX checks (explicit host-only mode). No target acceptance claimed.'
    exit 0
fi
failed=0
for step in 1 2 3 4 5 6; do
    if ./scripts/check-step.sh "$step"; then
        echo 'ERROR: unexpected live success in foundation milestone' >&2
        failed=1
    else
        failed=1
    fi
done
echo 'BLOCKED: full verification incomplete; no live QNX evidence.'
exit "$failed"
