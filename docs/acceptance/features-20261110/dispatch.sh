#!/bin/bash
set -euo pipefail
BASE=/mnt/host/features-edu-20261110
exec > "$BASE/dispatch.log" 2>&1
date -u
free -k
swapon --show
ps -eo pid,ppid,comm,rss,args --sort=-rss | head -20
for u in snapd.socket apport.service udisks2.service; do systemctl show "$u" -p ActiveState -p MainPID; done
id qnx
test -r /home/qnx/qnx800/qnxsdp-env.sh
test ! -e /home/qnx/edu-features-20261110
install -d -o qnx -g qnx /home/qnx/edu-builds/features-edu-20261110
cp "$BASE/build-plan.sh" /home/qnx/edu-builds/features-edu-20261110/build-plan.sh
chown qnx:qnx /home/qnx/edu-builds/features-edu-20261110/build-plan.sh
systemd-run --unit=edu-features-20261110 --uid=qnx --setenv=HOME=/home/qnx --property=WorkingDirectory=/home/qnx --property=StandardOutput=append:/home/qnx/edu-builds/features-edu-20261110/build.log --property=StandardError=append:/home/qnx/edu-builds/features-edu-20261110/build.log -- /bin/bash /home/qnx/edu-builds/features-edu-20261110/build-plan.sh wrong
