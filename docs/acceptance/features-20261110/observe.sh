#!/bin/bash
set -euo pipefail
B=/mnt/host/features-edu-20261110
for n in $(seq 1 180); do
 state=$(systemctl show edu-features-20261110.service -p ActiveState --value)
 if test "$state" != active && test "$state" != activating; then break; fi
 sleep 2
done
systemctl show edu-features-20261110.service -p ActiveState -p SubState -p Result -p ExecMainStatus > "$B/build-unit.txt"
cp /home/qnx/edu-builds/features-edu-20261110/build.log "$B/build.log"
free -k > "$B/memory-after.txt"
ps -eo pid,ppid,comm,rss,args --sort=-rss >> "$B/memory-after.txt"
journalctl -k --no-pager | grep -E -i 'oom|killed process|out of memory' > "$B/kernel-oom.txt" || true
find /home/qnx/edu-features-20261110 -maxdepth 3 -type f -printf '%p %s bytes
' > "$B/artifact-inventory.txt"
cat "$B/build-unit.txt"
tail -40 "$B/build.log"
