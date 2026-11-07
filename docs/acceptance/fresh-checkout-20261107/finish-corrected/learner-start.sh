#!/bin/sh
echo LEARNER_BIND source=64647c88597eff57f0723ffb2e479f90501f717065edd5a008827866fd8b76fe binary=2e9735a6987181630018ce2d09e64ab9d6f4920b5be36ed842b082f85f5b2042
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
