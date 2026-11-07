# Focused follow-up: stock kernel linker killed by guest OOM

This supersedes the initial 240-second attempt's provisional blocker conclusion,
not its immutable receipts. A self-imposed timeout alone was not an external
prerequisite failure. Parent authorized one fresh-directory 900-second diagnosis.

Actual command: driver.sh. Fresh work /home/qnx/clean-step3-diagnosis900-20261107,
stock installed mkqnximage, no E1 inputs, no stripped kernel. Only additional
platform option --ssh-ident=none avoids irrelevant root-SSH identity advice.
No installation/licensing/config/cap/swap changes. sdk-caps.json records PID148248,
100000/100000 CPU, 1073741824 memory, nice15, 1vCPU/512MiB, actual shared flock.

Builder began 12:30:49 UTC. At 12:36:30 (about341s, well BEFORE 900-second timeout),
guest global OOM killed linker PID1515. dmesg-after.log records victim virtual
588920KiB, anonymous RSS321704KiB plus file1732KiB. resources.log records exact
mkifs→qcc→stock-kernel ld command and memory samples: 457MiB Linux usable guest
RAM, no swap. This is a guest-memory OOM, not a measured host-cgroup OOM.

service-exit.log proves host-queue.service failed result oom-kill and restarted.
Its pre-existing OOMPolicy=stop stopped the entire unit including our setsid
controller/waiter; setsid separates process groups, NOT systemd unit membership.
Therefore explicit build.rc/controller.rc and normal queue rc could not survive.
No exit code is fabricated. Recovered kernel OOM and service result are actual
termination evidence; current restarted service Result=success is NOT the build
result. recovery.log confirms no builder/controller left and zero-byte IFS.
Only generated proprietary file hashes/sizes are saved, no buildfile contents.

**BLOCKED / portability UNVERIFIED.** Exact missing condition: unmodified stock
kernel link must finish under authorized guest memory, allowing a fresh generic
IFS/matching disk. No target image means no source/binary/image-bound fresh
negative/corrected native test. Earlier two actual qcc source compilations remain
compile-only. No private strip/cache substitution, cap increase or automatic retry.

Stop/reap and free-flock proof: sdk-stop.json. C6 remains STOPPED. Parent owns
site rendering and final full-suite integration; worker does not modify those files.
