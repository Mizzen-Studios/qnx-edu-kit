#!/bin/bash
set -eu
B=/mnt/host/clean-step3-20261107
A=/home/qnx/clean-step3-swap-20261107/learner-active
R="$B/native-clean/finish"
mkdir "$R"
swapon --show > "$R/swap-before.log"
if ! swapon --noheadings --show=NAME | grep -qx /var/tmp/edu-build.swap; then swapon /var/tmp/edu-build.swap; fi
free -m > "$R/memory.log"
cp "$B/learner-finish-source/main.c" "$A/finish.c"
cp "$B/learner_lab_finish.py" "$A/learner_lab_finish.py"
cp "$B/build-finish.sh" /home/qnx/edu-build-finish.sh
chown -R qnx:qnx "$R" "$A"
chmod 755 /home/qnx/edu-build-finish.sh
systemd-run --unit=edu-clean-finish-build --property=User=qnx --property=OOMPolicy=stop --property=RuntimeMaxSec=930 --property=StandardOutput=file:"$R/build.log" --property=StandardError=inherit /usr/bin/timeout --kill-after=15 900 /bin/bash /home/qnx/edu-build-finish.sh
