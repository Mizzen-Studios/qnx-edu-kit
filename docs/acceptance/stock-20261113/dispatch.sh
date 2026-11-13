#!/bin/bash
set -euo pipefail
B=/mnt/host/edu-stock-control-20261113
install -d -o qnx -g qnx "$B"
cp /mnt/host/edu-stock-plan-20261113.sh /home/qnx/edu-stock-plan-20261113.sh
chown qnx:qnx /home/qnx/edu-stock-plan-20261113.sh
test ! -e /home/qnx/edu-clean-stock-20261113
test ! -e "$B/stock-output"
free -k
cat /proc/swaps
systemd-run --unit=edu-clean-stock-20261113 --uid=qnx --setenv=HOME=/home/qnx --setenv=EDU_STOCK_GRANT=yes --setenv=EDU_SDP_ENV=/home/qnx/qnx800/qnxsdp-env.sh --setenv=EDU_STOCK_ROOT=/home/qnx/edu-clean-stock-20261113 --setenv=EDU_STOCK_EXPORT="$B/stock-output" --property=WorkingDirectory=/home/qnx --property=RuntimeMaxSec=900 --property=StandardOutput=append:/home/qnx/edu-stock-build-20261113.log --property=StandardError=append:/home/qnx/edu-stock-build-20261113.log -- /bin/bash /home/qnx/edu-stock-plan-20261113.sh
