#!/bin/bash
set -eu
B=/mnt/host/clean-step3-20261107
W=/home/qnx/clean-step3-swap-20261107
A="$W/learner-active"
R="$B/native-clean"
mkdir "$A" "$R"
cp "$B/wrong.c" "$B/correct.c" "$B/learner_lab.py" "$A/"
cp "$B/integrate-step3.sh" /home/qnx/edu-integrate-step3.sh
chown -R qnx:qnx "$A" "$R"
chmod 755 /home/qnx/edu-integrate-step3.sh
systemd-run --unit=edu-clean-learner-build --property=User=qnx --property=OOMPolicy=stop --property=RuntimeMaxSec=2400 --property=StandardOutput=file:"$R/controller.log" --property=StandardError=inherit /bin/bash /home/qnx/edu-integrate-step3.sh
