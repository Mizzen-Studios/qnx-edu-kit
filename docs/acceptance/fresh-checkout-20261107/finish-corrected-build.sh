#!/bin/bash
set -e
export HOME=/home/qnx
B=/mnt/host/rereview-20261107
W=/home/qnx/rereview-clean-20261107
A=$W/learner-active
python3 "$B/learner_lab.py" build --stage step6 --source "$B/step6/main.c" --out "$A" --sdp-env /home/qnx/qnx800/qnxsdp-env.sh --buildfile "$W/output/build/ifs.build" --bsp-cwd "$W"
mkdir "$B/finish-corrected"
cp "$A/learner-source.c" "$A/learner_bin" "$A/learner.ifs" "$A/learner-start.sh" "$A/manifest.json" "$B/finish-corrected/"
cp "$B/step6/main.c" "$B/finish-corrected/main.c"
