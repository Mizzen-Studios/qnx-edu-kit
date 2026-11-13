#!/bin/bash
set -euo pipefail
G=/mnt/host/edu-journey-20261113-1300
chown -R qnx:qnx "$G/own"
runuser -u qnx -- env HOME=/home/qnx python3 "$G/repo/scripts/learner_session.py" build --work "$G/own" --stage step3 --stock approved-stock-reuse --sdp-env /home/qnx/qnx800/qnxsdp-env.sh
