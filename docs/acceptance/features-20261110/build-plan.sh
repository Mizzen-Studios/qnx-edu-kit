#!/bin/bash
# PLAN ONLY: no dispatch before parent EDU lease grant. Existing licensed qnx user.
set -eo pipefail
phase="$1"
export HOME=/home/qnx
export EDU_SDP_ENV=/home/qnx/qnx800/qnxsdp-env.sh
export EDU_SHARED=/mnt/host/features-edu-20261110
export EDU_REPO="$EDU_SHARED/repo-lowmemory"
export EDU_ROOT=/home/qnx/edu-features-20261110
export EDU_PLATFORM="$EDU_ROOT/platform"
export EDU_ACTIVE="$EDU_ROOT/active"
export EDU_SNIPPET="$EDU_REPO/scripts/learner-step3.build.in"
test -r "$EDU_SDP_ENV"
source "$EDU_SDP_ENV"
command -v qcc; command -v mkifs; command -v mkqnximage
df -h /home/qnx
free -m
swapon --show
ps -eo pid,comm,rss,stat --sort=-rss | sed -n '1,12p'
case "$phase" in
 wrong)
  test ! -e "$EDU_ROOT"
  mkdir "$EDU_ROOT"
  cp "$EDU_SHARED/source/step3-wrong.c" "$EDU_ROOT/own-step3-wrong.c"
  export EDU_SOURCE="$EDU_ROOT/own-step3-wrong.c"
  bash "$EDU_REPO/scripts/learner_bootstrap.sh"
  stage=step3;;
 correct)
  # This correction is created ONLY after actual wrong FAIL/app0.
  cp "$EDU_SHARED/source/step3-correct.c" "$EDU_ROOT/own-step3-correct.c"
  export EDU_SOURCE="$EDU_ROOT/own-step3-correct.c"
  stage=step3;;
 finish)
  cp "$EDU_SHARED/source/step6-own.c" "$EDU_ROOT/own-step6.c"
  export EDU_SOURCE="$EDU_ROOT/own-step6.c"
  stage=step6;;
 *) exit 2;;
esac
sha256sum "$EDU_SOURCE" "$EDU_REPO/scripts/learner_lab.py"
python3 "$EDU_REPO/scripts/learner_lab.py" build --stage "$stage" --source "$EDU_SOURCE" --out "$EDU_ACTIVE" --sdp-env "$EDU_SDP_ENV" --buildfile "$EDU_PLATFORM/output/build/ifs.build" --bsp-cwd "$EDU_PLATFORM"
test ! -e "$EDU_SHARED/output-$phase"
cp -a "$EDU_ACTIVE" "$EDU_SHARED/output-$phase"
cp "$EDU_PLATFORM/output/disk-qemu" "$EDU_SHARED/disk-$phase.raw"
(cd "$EDU_SHARED"; sha256sum "output-$phase/"* "disk-$phase.raw") > "$EDU_SHARED/hashes-$phase.txt"
