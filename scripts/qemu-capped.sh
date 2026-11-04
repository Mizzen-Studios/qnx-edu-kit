#!/bin/sh
# All descendants inherit a real cgroup cap. Refuse an uncapped fallback.
set -eu
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 COMMAND [ARG ...]" >&2
    exit 2
fi
command -v systemd-run >/dev/null
exec systemd-run --user --scope --quiet -p CPUQuota=200% -p MemoryMax=4G nice -n 15 "$@"
