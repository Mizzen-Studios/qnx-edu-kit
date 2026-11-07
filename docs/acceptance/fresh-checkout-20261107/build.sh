#!/bin/bash
set -eo pipefail
export HOME=/home/qnx
B=/mnt/host/rereview-20261107
W=/home/qnx/rereview-clean-20261107
python3 "$B/learner_clean_preflight.py" --sdp-env /home/qnx/qnx800/qnxsdp-env.sh --fresh-work "$W" > "$B/preflight.json"
mkdir "$W"
cd "$W"
source /home/qnx/qnx800/qnxsdp-env.sh
mkqnximage --type=qemu --arch=x86_64 --build --ssh-ident=none
mkdir learner-active
A="$W/learner-active"
qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -Wno-unused-variable -o "$A/learner_bin" "$B/step3/wrong.c" -lpci
printf '%s
' '#!/bin/sh' 'exit 2' > "$A/learner-start.sh"
sed "s|@OUT@|$A|g" "$B/learner-step3.build.in" > local/snippets/ifs_files.learner
printf '%s
' 'waitfor /dev/pci/server_id_1 30' 'sh /proc/boot/learner-start.sh' > local/snippets/post_start.learner
mkqnximage --build
cp output/disk-qemu "$B/disk.raw"
for v in wrong correct finish; do
 stage=step3; src="$B/step3/$v.c"
 if [ "$v" = finish ]; then stage=step6; src="$B/step6/main.c"; fi
 python3 "$B/learner_lab.py" build --stage "$stage" --source "$src" --out "$A" --sdp-env /home/qnx/qnx800/qnxsdp-env.sh --buildfile "$W/output/build/ifs.build" --bsp-cwd "$W"
 mkdir "$B/$v"
 cp "$A/learner-source.c" "$A/learner_bin" "$A/learner.ifs" "$A/learner-start.sh" "$A/manifest.json" "$B/$v/"
 cp "$src" "$B/$v/main.c"
done
sha256sum output/build/ifs.build output/build/startup.sh local/snippets/*.learner output/disk-qemu > "$B/platform-hashes.txt"
