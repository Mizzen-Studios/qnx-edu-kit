#!/bin/bash
set -e
swapon /var/tmp/edu-build.swap
chown -R qnx:qnx /mnt/host/rereview-20261107
systemd-run --unit=edu-rereview-finish --property=User=qnx --property=OOMPolicy=stop --property=RuntimeMaxSec=930 --property=StandardOutput=file:/mnt/host/rereview-20261107/finish-build.log --property=StandardError=inherit /usr/bin/timeout --kill-after=15 900 /bin/bash /mnt/host/rereview-20261107/finish-corrected-build.sh
