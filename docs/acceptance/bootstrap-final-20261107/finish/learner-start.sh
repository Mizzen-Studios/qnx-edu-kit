#!/bin/sh
echo LEARNER_BIND source=29c2e2a834fa1198f21bb5b7717e4d47f3fae9fe8d72258d3b873c137c9e1a52 binary=6d3c97f9ccc514cdbaf942640a1bc706eb08822473181a27f121dfad6bf541e5
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
