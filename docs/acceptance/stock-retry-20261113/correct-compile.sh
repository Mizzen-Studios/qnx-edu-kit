#!/bin/bash
set -euo pipefail
B=/mnt/host/edu-stock-correct-20261113
chown -R qnx:qnx "$B"
runuser -u qnx -- env HOME=/home/qnx EDU_PREP_EXECUTION_GRANTED=yes EDU_WRONG_RECEIPT_REVIEWED=yes EDU_CORRECT_SHA256=2e3f68d281f9011024359584a053fa46f52a71f2824abece5c6410888b68aebc EDU_SDP_ENV=/home/qnx/qnx800/qnxsdp-env.sh EDU_SOURCE_DIR="$B" EDU_OUTPUT="$B/output" bash "$B/compile-lesson-PLAN.sh" correct > "$B/build.log" 2>&1
cat "$B/output/hashes.txt"
