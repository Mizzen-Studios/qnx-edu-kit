#!/bin/bash
set -eu
unit=learner-bootstrap-final-20261107
for n in $(seq 1 930); do
 state=$(systemctl show "$unit" -p ActiveState --value)
 case "$state" in inactive|failed)
  systemctl show "$unit" -p ActiveState -p Result -p ExecMainCode -p ExecMainStatus -p MainPID
  systemctl show host-queue.service -p ActiveState -p NRestarts
  test "$state" = inactive
  test "$(systemctl show "$unit" -p Result --value)" = success
  test "$(systemctl show "$unit" -p ExecMainStatus --value)" = 0
  exit $?;;
 esac
 sleep 2
done
systemctl show "$unit" -p ActiveState -p Result -p ExecMainCode -p ExecMainStatus -p MainPID
exit 2
