#!/bin/sh
echo LEARNER_BIND source=82f3c03a508157d5c217dd0d22b9da0bee15fabd58db06153770e57fd9c9a109 binary=fa8f6b1d2b19e5a531af349f9ec6e84f3da861f48199478b9dfafaa02357f5ba
echo "EDU TARGET $(uname -s) $(uname -r) $(uname -m)"
/proc/boot/learner_bin &
learner_pid=$!
if ! waitfor /dev/edu 30; then kill "$learner_pid"; wait "$learner_pid"; echo LEARNER_RC=2; exit 2; fi
printf "10\n" > /dev/edu
write_rc=$?
observed=$(cat /dev/edu)
read_rc=$?
echo "LEARNER_DEV_EDU write_rc=$write_rc read_rc=$read_rc result=$observed"
result_rc=1
if test "$write_rc" = 0 && test "$read_rc" = 0 && test "$observed" = 3628800; then result_rc=0; fi
kill "$learner_pid"
wait "$learner_pid"
echo LEARNER_DAEMON_EXIT=$?
echo LEARNER_RC=$result_rc
