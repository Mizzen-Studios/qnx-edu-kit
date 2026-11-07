#!/bin/bash
set -eo pipefail
export HOME=/home/qnx
cd /mnt/host/learner-step3
python3 - <<'PY'
from pathlib import Path
import shutil
cache=Path('/home/qnx/qnx-work/learner-kernel'); cache.mkdir(exist_ok=True)
import subprocess
subprocess.run(['/home/qnx/qnx800/host/linux/x86_64/usr/bin/x86_64-pc-nto-qnx8.0.0-objcopy','--strip-debug','/home/qnx/qnx800/target/qnx/x86_64/boot/sys/procnto-smp-instr',str(cache/'procnto-smp-instr')],check=True)
base=Path('/home/qnx/qnx-work/edu-followup10/ifs.build').read_text()
startup=Path('/home/qnx/qnx-work/can-gate/output/build/startup.sh').read_text().split('# Execute the post startup script.')[0]
for variant in ['wrong','correct']:
 out=Path('/mnt/host/learner-step3')/variant;out.mkdir(exist_ok=True)
 (out/'startup.sh').write_text(startup+'\nsh /proc/boot/learner-start.sh\n')
 s=base.replace('+keeplinked ', '').replace('search=', 'search=/home/qnx/qnx-work/learner-kernel:').replace('[virtual=x86_64,multiboot ]', '[virtual=x86_64,multiboot linker="qcc -bootstrap -nostdlib -Wl,--no-keep-memory -Wl,--reduce-memory-overheads -Vgcc_ntox86_64 -Wl,-z -Wl,max-page-size=4096 %(h!=0, -Wl,--section-start -Wl,.text=0x%t%)%(d!=0, -Wl,--section-start -Wl,.data=0x%d%) -Wl,--no-relax -o%o %i" ]').replace('procnto-smp-instr -mr', 'procnto-smp-instr -mr').replace('startup.sh=output/build/startup.sh','startup.sh='+str(out/'startup.sh'))
 s='\n'.join(line for line in s.splitlines() if not any(x in line for x in ['edu_probe=','edu_probe_native=','edu_resmgr=']))+'\n'
 s+='[perms=0755] learner_bin='+str(out/'learner_bin')+'\n[perms=0755] learner-start.sh='+str(out/'learner-start.sh')+'\n'
 (out/'learner.build').write_text(s)
PY
for variant in wrong correct; do
 python3 learner_lab.py build --source /mnt/host/learner-step3/$variant.c --out /mnt/host/learner-step3/$variant --sdp-env /home/qnx/qnx800/qnxsdp-env.sh --buildfile /mnt/host/learner-step3/$variant/learner.build --bsp-cwd /home/qnx/qnx-work/can-gate
done
