#!/bin/bash
R=/mnt/host/clean-step3-20261107/native-clean
for i in $(seq 1 130); do
 state=$(systemctl show edu-clean-learner-build.service -p ActiveState --value 2>> "$R/monitor-errors.log")
 if test "$state" = inactive || test "$state" = failed; then break; fi
 { date -u +%FT%TZ; free -m; } >> "$R/resources.log"
 sleep 20
done
systemctl show edu-clean-learner-build.service -p MainPID -p Result -p ActiveState -p ExecMainStatus -p ExecMainCode > "$R/service-exit.log"
systemctl show host-queue.service -p Result -p NRestarts -p ActiveState > "$R/queue-after.log"
dmesg > "$R/dmesg.log"
cat "$R/service-exit.log"
