#!/bin/bash
set -e
export EDU_BASE=/home/ubuntu/qnx-host/guest/shared/edu-journey-20261113-1300
export EDU_CONTROLLER=/home/ubuntu/qnx-host/guest/guestctl-capped.py
cd /home/ubuntu/qnx-host/guest/shared/edu-journey-20261113-1300/repo
mkdir "$EDU_BASE/sdk-wrong"
python3 scripts/stock_sdk_owner.py --controller "$EDU_CONTROLLER" --control "$EDU_BASE/sdk-wrong" > "$EDU_BASE/sdk-wrong-owner.log" 2>&1 &
SDK_OWNER=$!
trap 'touch "$EDU_BASE/sdk-wrong/STOP"; wait "$SDK_OWNER"' EXIT
for attempt in $(seq 1 310); do
  test -f "$EDU_BASE/sdk-wrong/SDK_READY" && break
  kill -0 "$SDK_OWNER" || exit 1
  sleep 2
done
test -f "$EDU_BASE/sdk-wrong/SDK_READY"
python3 "$EDU_CONTROLLER" exec "$EDU_BASE/build-wrong.sh" 600
touch "$EDU_BASE/sdk-wrong/STOP"
wait "$SDK_OWNER"
trap - EXIT
python3 -c 'import json,sys;r=json.load(open(sys.argv[1]));assert r["stopped_reaped"] and r["status"]=="REQUESTED_STOP";print(r)' "$EDU_BASE/sdk-wrong/sdk-owner.json"
if pgrep -af '^qemu-system-'; then exit 1; fi # rc1 means absent
flock -n /home/ubuntu/qnx-host/native-test.lock true
