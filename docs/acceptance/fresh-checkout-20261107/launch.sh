#!/bin/bash
set -eu
B=/mnt/host/rereview-20261107
swapon /var/tmp/edu-build.swap
free -m > "$B/memory-before.log"
chown -R qnx:qnx "$B"
systemd-run --unit=edu-rereview-clean --property=User=qnx --property=OOMPolicy=stop --property=RuntimeMaxSec=1830 --property=StandardOutput=file:$B/build.log --property=StandardError=inherit /usr/bin/timeout --kill-after=15 1800 /bin/bash "$B/build.sh"
