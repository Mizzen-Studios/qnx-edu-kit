#!/bin/sh
set -eu
case "${1-}" in
  1|2|3|4|5|6) ;;
  *) echo "usage: check-step.sh {1|2|3|4|5|6}" >&2; exit 64 ;;
esac
echo "REFERENCE ONLY: unchanged accumulated E1; not learner binary acceptance."
python3 "$(dirname "$0")/../tools/step_sources.py" --check
exec python3 "$(dirname "$0")/live_verify.py" --step "$1"
