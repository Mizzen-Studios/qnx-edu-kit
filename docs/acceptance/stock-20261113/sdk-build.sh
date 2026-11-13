#!/bin/bash
# PLAN ONLY: sole SDK owner dispatch after explicit parent EDU grant.
set -eo pipefail
: "${EDU_STOCK_GRANT:?explicit parent EDU grant required}"
test "$EDU_STOCK_GRANT" = yes
: "${EDU_SDP_ENV:?existing SDK environment}"
: "${EDU_STOCK_ROOT:?fresh guest disk directory}"
: "${EDU_STOCK_EXPORT:?fresh authorized share directory}"
test ! -e "$EDU_STOCK_ROOT"
test ! -e "$EDU_STOCK_EXPORT"
mkdir -p "$EDU_STOCK_ROOT" "$EDU_STOCK_EXPORT"
source "$EDU_SDP_ENV" >/dev/null
probe() { echo "EDU_CLEAN_STOCK phase=$1"; free -k; cat /proc/swaps; ps -eo pid,comm,rss,stat --sort=-rss | sed -n '1,15p'; }
cd "$EDU_STOCK_ROOT"
mkdir -p local/snippets
printf '%s\n' '-device edu' > local/snippets/qemu_options.edu
probe before_stock_build
# Installed defaults1G/2CPU require explicit512M/1. --tcg is TPM, not QEMU accelerator.
mkqnximage --type=qemu --arch=x86_64 --ram=512M --cpu=1 --ssh-ident=none --build
probe after_stock_build
test -s output/ifs.bin
test -s output/disk-qemu
test -f output/build/qemu_options
python3 - <<'CHECK'
from pathlib import Path
import shlex
args=shlex.split(Path('output/build/qemu_options').read_text())
assert sum(args[i:i+2]==['-device','edu'] for i in range(len(args)-1))==1
assert not any('learner' in str(p) for p in Path('local/snippets').iterdir())
print('PASS: generated QEMU_OPTIONS has one EDU device; no lesson IFS snippets')
CHECK
for f in output/ifs.bin output/disk-qemu output/disk-qemu.vmdk output/build/qemu_options local/options local/snippets/qemu_options.edu; do
 if test -f "$f"; then sha256sum "$f"; stat -c '%s %n' "$f"; fi
done > "$EDU_STOCK_EXPORT/stock-hashes-and-sizes.txt"
cp output/ifs.bin "$EDU_STOCK_EXPORT/ifs.bin"
cp output/disk-qemu "$EDU_STOCK_EXPORT/disk-qemu"
if test -e output/disk-qemu.vmdk; then cp -L output/disk-qemu.vmdk "$EDU_STOCK_EXPORT/disk-qemu.vmdk"; fi
cp output/build/qemu_options "$EDU_STOCK_EXPORT/qemu_options"
cp local/options "$EDU_STOCK_EXPORT/options"
cp local/snippets/qemu_options.edu "$EDU_STOCK_EXPORT/qemu_options.edu"
# No --run. STOP/REAP SDK before HOST native. No lesson IFS snippets/startup.
