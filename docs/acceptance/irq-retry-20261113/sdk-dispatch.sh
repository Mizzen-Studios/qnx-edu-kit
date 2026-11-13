#!/bin/bash
set -euo pipefail
B=/mnt/host/edu-irq-retry-20261113
chown -R qnx:qnx "$B"
runuser -u qnx -- env HOME=/home/qnx EDU_PREP_EXECUTION_GRANTED=yes EDU_SDP_ENV=/home/qnx/qnx800/qnxsdp-env.sh EDU_SOURCE_DIR="$B" EDU_OUTPUT="$B/output" bash "$B/compile.sh" finish > "$B/build.log" 2>&1
cat "$B/output/hashes.txt"
