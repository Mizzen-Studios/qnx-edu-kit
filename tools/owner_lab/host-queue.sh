#!/bin/bash
# Existing SDK guest only; root, preconfigured hostshare 9p mount.
set -u
mkdir -p /mnt/host
mountpoint -q /mnt/host || mount -t 9p -o trans=virtio,version=9p2000.L,msize=262144 hostshare /mnt/host || exit 1
mkdir -p /mnt/host/queue /mnt/host/results
printf 'ready\n' > /mnt/host/ready
while :; do
 for cmd in /mnt/host/queue/*.sh; do
  [ -f "$cmd" ] || continue
  id=$(basename "$cmd" .sh)
  mv "$cmd" "$cmd.running" || exit 1
  bash "$cmd.running" > "/mnt/host/results/$id.log" 2>&1
  rc=$?
  printf '%s\n' "$rc" > "/mnt/host/results/$id.rc.tmp"
  mv "/mnt/host/results/$id.rc.tmp" "/mnt/host/results/$id.rc"
  mv "$cmd.running" "$cmd.done"
 done
 sleep 1
done
