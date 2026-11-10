#!/bin/bash
set -euo pipefail
B=/mnt/host/features-edu-20261110
systemctl show edu-features-20261110.service -p ActiveState -p SubState -p Result -p ExecMainStatus > "$B/build-unit-final.txt"
mkdir "$B/preserved"
cp -a /home/qnx/edu-features-20261110/active "$B/preserved/active"
cp /home/qnx/edu-features-20261110/own-step3-wrong.c "$B/preserved/"
file /home/qnx/edu-features-20261110/active/learner_bin > "$B/elf-type.txt"
(cd /home/qnx/edu-features-20261110; sha256sum own-step3-wrong.c active/* platform/output/*.part platform/output/ifs.bin) > "$B/artifact-hashes.txt"
find /home/qnx/edu-features-20261110/platform/output/build -name '*procnto*' -printf '%p %s bytes
' > "$B/procnto-artifacts.txt"
journalctl -k --no-pager | tail -180 > "$B/kernel-tail.txt"
cp /home/qnx/edu-builds/features-edu-20261110/build.log "$B/build.log"
systemctl stop edu-features-20261110.service
pgrep -af '/home/qnx/edu-features-20261110|[m]kifs|[q]cc|[p]c-nto' > "$B/build-processes-after-stop.txt" || true
cat "$B/elf-type.txt" "$B/artifact-hashes.txt" "$B/procnto-artifacts.txt"
