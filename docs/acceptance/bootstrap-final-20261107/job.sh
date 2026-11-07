#!/bin/bash
set -eo pipefail
export HOME=/home/qnx
export EDU_SHARED_GUEST=/mnt/host/bootstrap-final-20261107
export EDU_SDP_ENV=/home/qnx/qnx800/qnxsdp-env.sh
export EDU_PLATFORM=/home/qnx/bootstrap-final-20261107
export EDU_ACTIVE=/home/qnx/bootstrap-final-active-20261107
export EDU_SOURCE=$EDU_SHARED_GUEST/step3/wrong.c
export EDU_SNIPPET=$EDU_SHARED_GUEST/learner-step3.build.in
python3 "$EDU_SHARED_GUEST/learner_clean_preflight.py" --sdp-env "$EDU_SDP_ENV" --fresh-work "$EDU_PLATFORM" > "$EDU_SHARED_GUEST/preflight.json"
bash "$EDU_SHARED_GUEST/learner_bootstrap.sh"
cp "$EDU_PLATFORM/output/disk-qemu" "$EDU_SHARED_GUEST/disk.raw"
sha256sum "$EDU_PLATFORM/output/build/ifs.build" "$EDU_PLATFORM/output/build/startup.sh" "$EDU_PLATFORM"/local/snippets/*.learner "$EDU_PLATFORM/output/disk-qemu" > "$EDU_SHARED_GUEST/platform-hashes.txt"
for variant in wrong correct finish; do
 stage=step3; src="$EDU_SHARED_GUEST/step3/$variant.c"
 if test "$variant" = finish; then stage=step6; src="$EDU_SHARED_GUEST/finish/main.c"; fi
 python3 "$EDU_SHARED_GUEST/learner_lab.py" build --stage "$stage" --source "$src" --out "$EDU_ACTIVE" --sdp-env "$EDU_SDP_ENV" --buildfile "$EDU_PLATFORM/output/build/ifs.build" --bsp-cwd "$EDU_PLATFORM"
 mkdir "$EDU_SHARED_GUEST/$variant-bundle"
 cp "$EDU_ACTIVE"/{learner-source.c,learner_bin,learner.ifs,learner-start.sh,manifest.json} "$EDU_SHARED_GUEST/$variant-bundle/"
done
