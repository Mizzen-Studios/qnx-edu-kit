#!/bin/sh
set -eu
cd "$(dirname "$0")"
case "${1-}" in
  "") make host-check; exec python3 scripts/live_verify.py ;;
  --host-only) make host-check; echo "SKIP: live QNX checks (explicit host-only); no target acceptance claimed." ;;
  *) echo "usage: verify.sh [--host-only]" >&2; exit 64 ;;
esac
