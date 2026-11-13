#!/bin/bash
# PLAN ONLY: requires explicit parent grant to sole SDK owner. No image/QEMU actions.
set -euo pipefail
: "${EDU_PREP_EXECUTION_GRANTED:?explicit parent grant required}"
test "$EDU_PREP_EXECUTION_GRANTED" = yes
: "${EDU_SDP_ENV:?existing licensed SDK environment file}"
: "${EDU_SOURCE_DIR:?source-bound handoff directory}"
: "${EDU_OUTPUT:?fresh external output directory}"
phase="${1:?wrong or finish or correct}"
case "$phase" in
 wrong) name=step3-wrong.c; expected=7868b7dfa3fc1d3f21600bc4231430d5c40f082f63999fd4b57d3485f945a19c;;
 finish) name=step6-own.c; expected=c84e91925d84731b18e1ad11718b692a78e351bf2f633895e9781c7ef8641ef7;;
 correct)
  : "${EDU_WRONG_RECEIPT_REVIEWED:?actual wrong FAIL/app0 must be reviewed first}"
  test "$EDU_WRONG_RECEIPT_REVIEWED" = yes
  : "${EDU_CORRECT_SHA256:?fresh post-observation source hash required}"
  name=step3-correct.c; expected="$EDU_CORRECT_SHA256";;
 *) exit 64;;
esac
printf '%s  %s\n' "$expected" "$EDU_SOURCE_DIR/$name" | sha256sum -c -
test ! -e "$EDU_OUTPUT"
mkdir -p "$EDU_OUTPUT"
cp "$EDU_SOURCE_DIR/$name" "$EDU_OUTPUT/learner-source.c"
set +u # installed SDK environment may reference unset optional shell variables
source "$EDU_SDP_ENV" >/dev/null
set -u
probe() { echo "EDU_STOCK_COMPILE phase=$1"; free -k; cat /proc/swaps; ps -eo pid,comm,rss,stat --sort=-rss | sed -n '1,12p'; }
command -v qcc
probe before_compile
qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g0 -Wall -Wextra -Wno-unused-variable -c "$EDU_OUTPUT/learner-source.c" -o "$EDU_OUTPUT/learner.o"
probe after_compile
qcc -Vgcc_ntox86_64 -o "$EDU_OUTPUT/learner_bin" "$EDU_OUTPUT/learner.o" -lpci -lslog2
probe after_link
(cd "$EDU_OUTPUT"; sha256sum learner-source.c learner.o learner_bin > hashes.txt)
# No mkifs, bootstrap snippets, custom startup or learner_lab.py build/run.
