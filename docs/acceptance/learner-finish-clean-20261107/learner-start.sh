#!/bin/sh
echo LEARNER_BIND source=73d19b2784559a3115ded0b1a13a17a28f90b3f892b982af520e02084f315435 binary=1315beffa3dcce44d78be20999abc458576305e4ff8e17498ea9beb420276caf
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
