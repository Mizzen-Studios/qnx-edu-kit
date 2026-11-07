#!/bin/bash
set -eu
export HOME=/home/qnx
echo CLEAN_STEP3_INSTALLED_INVENTORY
test -f /home/qnx/qnx800/qnxsdp-env.sh
find /home/qnx/qnx800 -maxdepth 6 -type f \( -name '*x86*build*' -o -name '*.build' -o -name '*bsp*.zip' -o -iname '*readme*' \) | head -80
find /home/qnx/qnx800 -maxdepth 5 -type d | grep -E 'bsp|src/hardware|mkqnximage' | head -80
find /home/qnx -maxdepth 3 -type d | grep -v -E '/[.]|qnx-work|qnxinstall' | head -60
