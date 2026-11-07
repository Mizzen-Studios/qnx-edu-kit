#!/bin/bash
set -eu
W=/home/qnx/clean-step3-swap-20261107
A="$W/learner-active"
R=/mnt/host/clean-step3-20261107/native-clean/finish-corrected
python3 "$A/learner_lab_finish.py" build --stage step6 --source "$A/finish.c" --out "$A" --sdp-env /home/qnx/qnx800/qnxsdp-env.sh --buildfile "$W/output/build/ifs.build" --bsp-cwd "$W"
cp "$A/learner-source.c" "$A/learner_bin" "$A/learner.ifs" "$A/learner-start.sh" "$A/manifest.json" "$R/"
cp "$A/finish.c" "$R/main.c"
echo 0 > "$R/build.rc"
