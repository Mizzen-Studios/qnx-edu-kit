#!/bin/sh
# HOST path checks only: no SDK reads, controller calls, guest or lease.
set -eu
for name in EDU_CONTROLLER EDU_SHARE EDU_STOCK EDU_SDP_ENV EDU_NATIVE_LEASE; do
  eval "value=\${$name-}"
  if [ -z "$value" ]; then echo "BLOCKED: set $name to your existing operator-approved path; see docs/learner-route.md." >&2; exit 2; fi
  case "$value" in /absolute/*|*" "*|*[![:print:]]*) echo "BLOCKED: replace placeholder/unsafe $name path." >&2; exit 2;; /*) ;; *) echo "BLOCKED: $name must be absolute." >&2; exit 2;; esac
done
[ -f "$EDU_CONTROLLER" ] || { echo "BLOCKED: EDU_CONTROLLER must be an existing reviewed controller file; no download or execution performed." >&2; exit 2; }
[ -d "$EDU_STOCK" ] || { echo "BLOCKED: EDU_STOCK must be your existing legally supplied stock directory." >&2; exit 2; }
[ -d "$EDU_SHARE" ] && [ -w "$EDU_SHARE" ] && [ -x "$EDU_SHARE" ] || { echo "BLOCKED: EDU_SHARE needs an existing writable/searchable directory; choose an approved directory, do not sudo/chmod system paths." >&2; exit 2; }
echo "PASS: HOST paths only; stock hashes, SDK environment inside guest and actual lease remain separate strict native gates. No controller/SDK/guest invoked."
