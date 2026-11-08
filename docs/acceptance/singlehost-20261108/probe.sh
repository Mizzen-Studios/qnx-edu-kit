#!/bin/bash
set -u
printf 'EXISTING_HOST\n'
uname -sm
printf 'QUEUE_STATUS\n'
systemctl show host-queue.service -p ActiveState -p NRestarts
printf 'EXISTING_QEMU_CAPABILITY\n'
command -v qemu-system-x86_64 || true
for p in /usr/bin/qemu-system-x86_64 /usr/local/bin/qemu-system-x86_64 /home/qnx/qnx800/host/linux/x86_64/usr/bin/qemu-system-x86_64; do if test -e "$p"; then ls -l "$p"; fi; done
printf 'USER_SCOPE_CAPABILITY\n'
runuser -u qnx -- env HOME=/home/qnx XDG_RUNTIME_DIR=/run/user/1001 systemctl --user show-environment 2>&1
printf 'PLANNER_BEGIN\n'
runuser -u qnx -- env HOME=/home/qnx XDG_RUNTIME_DIR=/run/user/1001 python3 /mnt/host/wrapper-20261108/repo/scripts/learner_setup.py --sdp-env /home/qnx/qnx800/qnxsdp-env.sh --bsp /home/qnx/qnx800 --qemu /usr/bin/qemu-system-x86_64 --work /home/qnx/edu-singlehost-probe-20261108 --probe-sdk
rc=$?
printf 'PLANNER_RC=%s\n' "$rc"
exit "$rc"
