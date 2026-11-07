#!/bin/sh
echo LEARNER_BIND source=a6b724dbbf066fd7e55ee6bd38745eaa2f35e5b4da9ef7e9b42ddf1c42f77109 binary=22b86e25c442411f79aa14a8849ccbf0ad07a368a12741489cd7842a889db5a8
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
