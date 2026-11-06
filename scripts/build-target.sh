#!/bin/bash
# Run INSIDE the owner's existing SDK guest. Sources and outputs stay external.
set -eo pipefail
export HOME=/home/qnx
source /home/qnx/qnx800/qnxsdp-env.sh
src=/mnt/host/edu-followup10
out=/home/qnx/qnx-work/edu-followup10
mkdir -p "$out"
cd "$out"
qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -Werror -o edu_resmgr "$src/edu_resmgr.c" -lpci
qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -Werror -o edu_accept "$src/edu_accept.c"
qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -Werror -o edu_probe "$src/edu_probe.c" -lpci
printf 'EDU_FOLLOWUP10_QCC_PASS\n'
python3 - <<'PY'
from pathlib import Path
s=Path('/home/qnx/qnx-work/can-gate/output/build/ifs.resmgr-followup9.build').read_text()
s=s.replace('/home/qnx/qnx-work/edu_accept','/home/qnx/qnx-work/edu-followup10/edu_accept').replace('/home/qnx/qnx-work/edu_resmgr','/home/qnx/qnx-work/edu-followup10/edu_resmgr').replace('/home/qnx/qnx-work/edu_probe','/home/qnx/qnx-work/edu-followup10/edu_probe')
Path('ifs.build').write_text(s)
PY
cd /home/qnx/qnx-work/can-gate
mkifs -v "$out/ifs.build" "$src/ifs-edu-followup10.bin" > "$out/mkifs.log" 2>&1
sha256sum "$src/ifs-edu-followup10.bin"
printf 'EDU_FOLLOWUP10_IFS_PASS\n'
