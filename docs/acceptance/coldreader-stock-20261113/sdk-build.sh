#!/bin/bash
set -euo pipefail
G=/mnt/host/edu-coldreader-20261113-1208
chown -R qnx:qnx "$G/own"
runuser -u qnx -- env HOME=/home/qnx python3 "$G/repo/scripts/learner_session.py" build --work "$G/own" --stage step6 --stock approved-stock-reuse --sdp-env /home/qnx/qnx800/qnxsdp-env.sh
