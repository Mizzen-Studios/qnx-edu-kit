#!/bin/bash
set -eu
R=/mnt/host/clean-step3-20261107/swap-attempt
W=/home/qnx/clean-step3-swap-20261107
mkdir "$R/prebuild-rejection"
for f in build.log service-exit.log isolation.log queue-after.log started finished dmesg-after.log output-files.log output-hashes.log; do test ! -f "$R/$f" || mv "$R/$f" "$R/prebuild-rejection/$f"; done
test -f "$W/build.sh"
mv "$W/build.sh" /home/qnx/edu-clean-swap-build.sh
test -z "$(ls -A "$W")"
systemctl reset-failed edu-clean-swap-build.service
date -u +%FT%TZ > "$R/started"
systemd-run --unit=edu-clean-swap-build-actual --property=User=qnx --property=OOMPolicy=stop --property=RuntimeMaxSec=1830 --property=StandardOutput=file:"$R/build.log" --property=StandardError=inherit /bin/bash /home/qnx/edu-clean-swap-build.sh
systemctl show host-queue.service edu-clean-swap-build-actual.service -p Id -p ControlGroup -p OOMPolicy -p MainPID > "$R/isolation.log"
