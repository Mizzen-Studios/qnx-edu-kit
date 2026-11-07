#!/bin/bash
set -u
R=/mnt/host/clean-step3-20261107/swap-attempt
W=/home/qnx/clean-step3-swap-20261107
while systemctl is-active --quiet edu-clean-swap-build.service; do
 { date -u +%FT%TZ; free -m; ps -eo pid,ppid,rss,stat,comm | grep -E 'ld|mkifs|mkqnx|qcc'; } >> "$R/resources.log"
 sleep 20
done
systemctl show edu-clean-swap-build.service -p Result -p ExecMainCode -p ExecMainStatus -p ActiveState -p ControlGroup -p OOMPolicy > "$R/service-exit.log"
systemctl show host-queue.service -p Result -p NRestarts -p ActiveState -p MainPID > "$R/queue-after.log"
dmesg > "$R/dmesg-after.log"
find "$W/output" -maxdepth 2 -type f -printf '%P %s bytes\n' > "$R/output-files.log"
for f in "$W/output/ifs.bin" "$W/output/disk.raw"; do
 if test -f "$f"; then sha256sum "$f"; stat -c '%n %s bytes' "$f"; fi
done > "$R/output-hashes.log"
date -u +%FT%TZ > "$R/finished"
sync
