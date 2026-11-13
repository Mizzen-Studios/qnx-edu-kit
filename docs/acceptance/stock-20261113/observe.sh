#!/bin/bash
set -eo pipefail
B=/mnt/host/edu-stock-control-20261113
for n in $(seq 1 230); do
 systemctl show edu-clean-stock-20261113.service -p ActiveState -p SubState -p Result -p ExecMainStatus > "$B/build-unit.txt"
 cp /home/qnx/edu-stock-build-20261113.log "$B/build.log"
 free -k > "$B/guest-memory-last.txt"
 state=$(systemctl show edu-clean-stock-20261113.service -p ActiveState --value)
 if test "$state" != active && test "$state" != activating; then break; fi
 sleep 4
done
systemctl show edu-clean-stock-20261113.service -p ActiveState -p SubState -p Result -p ExecMainStatus > "$B/build-unit-final.txt"
cp /home/qnx/edu-stock-build-20261113.log "$B/build.log"
ps -eo pid,ppid,comm,rss,args --sort=-rss > "$B/guest-processes-final.txt"
journalctl -k --no-pager | grep -E -i 'oom|killed process|out of memory' > "$B/kernel-oom.txt" || true
find /home/qnx/edu-clean-stock-20261113 -maxdepth 4 -type f -printf '%p %s bytes
' > "$B/artifact-inventory.txt"
for f in /home/qnx/edu-clean-stock-20261113/output/ifs.bin /home/qnx/edu-clean-stock-20261113/output/disk-qemu /home/qnx/edu-clean-stock-20261113/output/disk-qemu.vmdk /home/qnx/edu-clean-stock-20261113/output/build/qemu_options; do if test -f "$f"; then sha256sum "$f"; stat -c '%s %n' "$f"; fi; done > "$B/all-partial-hashes.txt"
cat "$B/build-unit-final.txt"
tail -25 "$B/build.log"
