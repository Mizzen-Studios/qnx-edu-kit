#!/bin/bash
set -eu
export HOME=/home/qnx
cd /mnt/host/clean-step3-20261107
python3 learner_clean_preflight.py --sdp-env /home/qnx/qnx800/qnxsdp-env.sh --fresh-work /home/qnx/clean-step3-20261107 > preflight.json || { cat preflight.json; exit 2; }
cat preflight.json
source /home/qnx/qnx800/qnxsdp-env.sh
for variant in wrong correct; do
 qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -Wno-unused-variable -o "$variant.bin" "$variant.c" -lpci
 sha256sum "$variant.c" "$variant.bin"
done
mkdir /home/qnx/clean-step3-20261107
cd /home/qnx/clean-step3-20261107
mkqnximage --help=brief > /mnt/host/clean-step3-20261107/mkqnximage-options.log
# Strictly bounded generation; no --run, no stripped kernel or cached build.
timeout --kill-after=10 240 mkqnximage --type=qemu --arch=x86_64 --build
