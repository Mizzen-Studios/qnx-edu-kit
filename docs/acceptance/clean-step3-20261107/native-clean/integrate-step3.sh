#!/bin/bash
set -eu
source /home/qnx/qnx800/qnxsdp-env.sh
W=/home/qnx/clean-step3-swap-20261107
A="$W/learner-active"
R=/mnt/host/clean-step3-20261107/native-clean
cd "$W"
# Application-only snippets; stock platform, kernel and PCI setup remain untouched.
qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -Wno-unused-variable -o "$A/learner_bin" "$A/correct.c" -lpci
printf '#!/bin/sh\nexit 2\n' > "$A/learner-start.sh"
printf '[perms=0755] /proc/boot/learner_bin=%s/learner_bin\n[perms=0755] /proc/boot/learner-start.sh=%s/learner-start.sh\n' "$A" "$A" > local/snippets/ifs_files.learner
printf '\nwaitfor /dev/pci/server_id_1 60 || exit 2\nsh /proc/boot/learner-start.sh\n' > local/snippets/post_start.learner
timeout --kill-after=15 1800 mkqnximage --build
cp --sparse=always output/disk-qemu "$R/disk.raw"
sha256sum local/snippets/ifs_files.learner local/snippets/post_start.learner output/build/ifs.build output/build/startup.sh output/build/post_startup.sh output/disk-qemu > "$R/integration-hashes.log"
for variant in wrong correct; do
 python3 "$A/learner_lab.py" build --source "$A/$variant.c" --out "$A" --sdp-env /home/qnx/qnx800/qnxsdp-env.sh --buildfile "$W/output/build/ifs.build" --bsp-cwd "$W" > "$R/$variant-build.log" 2>&1
 mkdir "$R/$variant"
 cp "$A/learner-source.c" "$A/learner_bin" "$A/learner.ifs" "$A/learner-start.sh" "$A/manifest.json" "$R/$variant/"
 cp "$A/$variant.c" "$R/$variant/main.c"
done
echo 0 > "$R/build.rc"
