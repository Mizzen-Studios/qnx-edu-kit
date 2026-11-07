#!/bin/bash
# Own explicit receipts: queue wrapper may die with a terminated compiler group.
set -u
export HOME=/home/qnx
R=/mnt/host/clean-step3-20261107/diagnosis900
mkdir -p "$R"
exec >"$R/controller.log" 2>&1
W=/home/qnx/clean-step3-diagnosis900-20261107
if test -e "$W"; then echo fresh_directory_already_exists; echo 2 > "$R/controller.rc"; exit 2; fi
mkdir "$W"
source /home/qnx/qnx800/qnxsdp-env.sh
cd "$W"
start=$(date +%s)
printf '%s
' "$start" > "$R/started"
dmesg | tail -100 > "$R/dmesg-before.log"
# setsid separates builder from queue/controller; wait status is written explicitly.
setsid timeout --kill-after=15 900 mkqnximage --type=qemu --arch=x86_64 --build --ssh-ident=none > "$R/build.log" 2>&1 &
pid=$!
echo "$pid" > "$R/build.pid"
(
 while kill -0 "$pid" 2>/dev/null; do
  date -u +%FT%TZ
  free -m
  ps -eo pid,ppid,pgid,rss,stat,args | grep -E 'mkqnximage|mkqnx6fsimg|mkifs|qcc|ntox86|ld |timeout' | grep -v grep || true
  sleep 20
 done
) > "$R/resources.log" 2>&1 &
monitor=$!
wait "$pid"
rc=$?
printf '%s
' "$rc" > "$R/build.rc.tmp"
mv "$R/build.rc.tmp" "$R/build.rc"
kill "$monitor" 2>/dev/null || true
wait "$monitor" 2>/dev/null || true
dmesg | tail -160 > "$R/dmesg-after.log"
find output -maxdepth 2 -type f -printf '%p %s bytes
' > "$R/output-files.log"
for f in output/build/ifs.build output/build/startup.sh output/build/post_startup.sh output/ifs.bin output/disk.raw; do
 if test -f "$f"; then sha256sum "$f"; stat -c '%n %s bytes' "$f"; fi
done > "$R/output-hashes.log"
end=$(date +%s)
echo "$end" > "$R/finished"
echo "$((end-start))" > "$R/duration-seconds"
sync
echo 0 > "$R/controller.rc"
exit 0
