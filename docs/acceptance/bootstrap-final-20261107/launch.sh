#!/bin/bash
set -eo pipefail
B=/mnt/host/bootstrap-final-20261107
cat "$B/mapping-nonce"
export EDU_SWAP=/var/tmp/edu-build.swap
export EDU_BUILD_USER=qnx
export EDU_UNIT=learner-bootstrap-final-20261107
export EDU_JOB=$B/job.sh
export EDU_LOG=$B/build.log
df -h "$(dirname "$EDU_SWAP")"
stat "$EDU_SWAP"
test "$(stat -c %s "$EDU_SWAP")" = 1073741824
swapon --show
if ! swapon --show=NAME --noheadings | grep -Fx "$EDU_SWAP"; then swapon "$EDU_SWAP"; fi
free -m
systemctl is-active host-queue.service
systemctl show host-queue.service -p NRestarts
chown -R qnx:qnx "$B"
systemd-run --unit="$EDU_UNIT" --property="User=$EDU_BUILD_USER" --property=OOMPolicy=stop --property=RuntimeMaxSec=1830 --property="StandardOutput=file:$EDU_LOG" --property=StandardError=inherit /usr/bin/timeout --kill-after=15 1800 /bin/bash "$EDU_JOB"
