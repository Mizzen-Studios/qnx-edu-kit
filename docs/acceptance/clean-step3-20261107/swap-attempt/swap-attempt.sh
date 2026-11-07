#!/bin/bash
set -eu
R=/mnt/host/clean-step3-20261107/swap-attempt
W=/home/qnx/clean-step3-swap-20261107
mkdir -p "$R"
test ! -e "$W"
mkdir "$W"
free -m > "$R/memory-before.log"
df -h /home/qnx > "$R/disk-before.log"
test ! -e /var/tmp/edu-build.swap
dd if=/dev/zero of=/var/tmp/edu-build.swap bs=1M count=1024 status=none
chmod 600 /var/tmp/edu-build.swap
mkswap /var/tmp/edu-build.swap > "$R/swap-setup.log"
swapon /var/tmp/edu-build.swap
free -m > "$R/memory-swap.log"
cat > "$W/build.sh" <<'BUILD'
#!/bin/bash
source /home/qnx/qnx800/qnxsdp-env.sh
cd /home/qnx/clean-step3-swap-20261107
exec timeout --kill-after=15 1800 mkqnximage --type=qemu --arch=x86_64 --build --ssh-ident=none
BUILD
chmod 700 "$W/build.sh"
chown -R qnx:qnx "$W"
dmesg > "$R/dmesg-before.log"
date -u +%FT%TZ > "$R/started"
systemd-run --unit=edu-clean-swap-build --property=User=qnx --property=OOMPolicy=stop --property=RuntimeMaxSec=1830 --property=StandardOutput=file:"$R/build.log" --property=StandardError=inherit /bin/bash "$W/build.sh"
systemctl show host-queue.service edu-clean-swap-build.service -p Id -p ControlGroup -p OOMPolicy -p MainPID > "$R/isolation.log"
