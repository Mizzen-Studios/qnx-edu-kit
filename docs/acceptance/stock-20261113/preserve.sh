#!/bin/bash
set -eo pipefail
B=/mnt/host/edu-stock-control-20261113
R=/home/qnx/edu-clean-stock-20261113
systemctl stop edu-clean-stock-20261113.service
systemctl show edu-clean-stock-20261113.service -p Result -p ExecMainStatus -p ActiveState -p SubState > "$B/unit-after-stop.txt"
cp "$R/output/build/qemu_options" "$B/qemu_options"
cp "$R/local/snippets/qemu_options.edu" "$B/qemu_options.edu"
for f in "$R"/output/ifs.bin "$R"/output/*.part "$R"/output/disk-qemu* "$R"/output/build/ifs.build "$R"/local/options "$R"/local/snippets/qemu_options.edu; do
 if test -f "$f"; then sha256sum "$f"; stat -c '%s %n' "$f"; fi
done > "$B/preserved-partial-hashes.txt"
pgrep -af '[q]cc|[m]kifs|[x]86_64-pc-nto' > "$B/build-processes-after-stop.txt" || true
free -k > "$B/guest-memory-after-stop.txt"
cat "$B/unit-after-stop.txt" "$B/preserved-partial-hashes.txt" "$B/build-processes-after-stop.txt"
