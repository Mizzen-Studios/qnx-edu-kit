#!/bin/sh
# Scan working tree, including ignored/untracked files. No downloads or SDK needed.
set -eu
cd "$(dirname "$0")/.."
exec python3 scripts/check_no_sdk.py "$@"
