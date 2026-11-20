#!/bin/sh
set -eu
cd "$(dirname "$0")"
if ! command -v make >/dev/null 2>&1; then
  echo "BLOCKED: GNU make is required for host checks; install it before running verify.sh." >&2
  exit 2
fi
case "${1-}" in
  "") make host-check; exec python3 scripts/live_verify.py ;;
  --host-only) make host-check; echo "SKIP: live QNX checks (explicit host-only); no target acceptance claimed." ;;
  *) echo "usage: verify.sh [--host-only]" >&2; exit 64 ;;
esac
