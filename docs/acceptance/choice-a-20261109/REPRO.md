# Reproduction on this existing licensed host only

Boot the capped existing SDK host under sole outer flock. Before package/native
work require `systemctl is-system-running` =running and actual `findmnt --mountpoint
/boot` and `/boot/efi`; this wave needed no repair. No SDK changes.

Authorized administrator ran `dpkg --configure -a`, `dpkg --audit`, then
`apt-get install -y --no-install-recommends qemu-system-x86 dbus-user-session libpam-systemd`.
Exact versions/dependencies are in package-session.log. Started packaged
`user-runtime-dir@1001.service user@1001.service`. As qnx set HOME=/home/qnx,
XDG_RUNTIME_DIR=/run/user/1001 and real DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1001/bus;
verify `systemctl --user show-environment`. See ../../singlehost-prerequisites.md.

Fresh original source archivec20c8c7, no historical solution. Notebook init,
import own prediction, independently implement BAR0map/ID/complement in step3
starter writing12345679 and checking its complement. Actual source/ELF/IFS
hashes in first-timeout/build-manifest.json. Pre-existing inspected1GiB swap
reactivated; no new swap. Build local guest disk, not9p. `learner_bootstrap.sh`
with fresh EDU_PLATFORM and own EDU_ACTIVE/EDU_SOURCE, then notebook `build` using
platform/output/build/ifs.build and local BSPcwd. Full commands in final-session.json.

`flock /home/qnx/choice-a-native.lock env EDU_NATIVE_LOCK=/home/qnx/choice-a-native.lock
EDU_NATIVE_LEASE=granted python3 scripts/learner_session.py run --work OWN --stage
step3 --disk OWN/platform/output/disk-qemu` yielded180s timeout. One minimum
parameter correction allowed `--timeout 900` without cap/oracle changes; that
also timed out. Both preserved; no further native attempt or claimed app0.

Notebook notes diagnosis/explanation imported, then `learner_session.py export
--work OWN --out /home/qnx/choice-a-failure-export-20261109`; verified all22file
hashes from pack.json. Export is failure evidence, NOT validated learner work.
Stop/reap outer after inner; verify no QEMU, controller/owner exit and free flock.
No public artifacts. For a usable native demonstration retain the supported
split-host route; this wave does not close the single-host native gate.
