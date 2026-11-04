# SDP 8 installation and native gates — 4 November 2026

Private internal evidence only; no public QNX benchmark or functional evaluation.

## Installed and verified

- Persistent Ubuntu24 x86_64 full-system TCG guest, not unreliable qemu-user Docker. Host disk: /home/ubuntu/qnx-host/guest/guest.qcow2. Ordinary guest user qnx, uid1001.
- QSC2.0.4:v202501021438 under /home/qnx/qnxinstall/qnxsoftwarecenter. Official installer length104701288 and vendor MD5bca161a97ab3e14189cf8e7c8227fb7d matched.
- Authenticated using only owner-provided credential files. Password never in argv or repositories. QSC used mode600 @options; transient shared/guest authentication copies removed. Original files preserved.
- Account serial was NOT the activation key: it failed Invalid License Key. The QSC baseline entitlement error identified the corresponding actual key; that single key was successfully activated through a private options file. No activateAll or second-host activation.
- SDP baseline com.qnx.qnx800/8.0.0.00141T202311271501L installed in /home/qnx/qnx800 (~/qnx800 INSIDE the x86 guest). Baseline resolved current entitled components, not exclusively2023 GA components.
- Generic x86_64 GA BSP com.qnx.qnx800.bsp.hw.x86_64/0.0.1.00050T202311201204L installed; no silent experimental opt-in.
- QSC -verifyInstallation returned0.
- qcc -Vgcc_ntox86_64 compiled hello.c into QNX x86_64 ELF with interpreter /usr/lib/ldqnx-64.so.2. Actual QNX8 TCG boot executed it and printed Hello QNX 8.0.
- mkqnximage built licensed x86_64 image. Native pci-tool identified Kvaser10e8:8406 and EDU1234:11e8. SDK contains target usr/sbin/slm; not yet exercised.

## Primary CAN module gate FAILS live loading

External pinned mods-can.so SHA25645cb8b57889b0827b70385692c44ba76d8d49b618e6ae009ee37d0e3e11adea2 was really loaded using:

    io-sock -m /proc/boot/mods-can.so -o prefix=/can

Daemon launch returned0 and /can existed, but neither means module success. Real slog2 diagnostics:

    unknown symbol: sockcan_protosw referenced from mods-can.so
    link_elf_load_file: /proc/boot/mods-can.so load fail cause:Unresolved symbols
    mods-can.so: module not loaded, error 8
    /proc/boot/mods-can.so: failed to mount (8) Exec format error

io-sock BuildID2c37e223468d52cec678a9d50f7978df. QNX8.0.0 kernel build2026/06/05-16:26:03EDT. Primary SocketCAN ABI/module gate RED. Public sources still lack internal dependencies; SDP installation alone does not enable rebuilding module. No primary board/RX/TX acceptance passed.

## Authorized fallback investigated, not completed

Separate GPL dev-can-linux v1.12.0 ran on QNX, detected Kvaser and created /dev/can0/rx0 and tx0. No GPL code copied into Apache application sources.

Two bounded real traffic probes used QEMU can-host-socketcan on vcan1, leaving active vcan0 simulation alone. Each sent100 host frames but captured zero QNX candump rows. Each invoked native cansend100 times, but host observed only one ID321 frame with expected8-byte payload. Second probe drained receive socket before exiting. NOT byte-exact100-frame success or completed fallback selection. Investigate mailbox/filter/IRQ/ACK behaviour and capture logic before adopting fallback.

Image also printed Memory fault (core dumped) immediately after Starting sshd. Main io-sock and DHCP remained alive, but SSH reliability/isolation is NOT established.

## State and remaining core

Persistent Linux SDK guest cleanly ACPI-stopped after verification; QEMU supervisor exited0. Restart with /home/ubuntu/qnx-host/guest/guestctl.py start. SDK resides inside persistent guest disk, NOT directly on ARM host. Credentials are no longer the SDK gate. No SDK/binaries/images/licences/caches/secrets in repositories.

Private evidence outside repositories: /home/ubuntu/qnx-host/guest/shared/results; shared/qnx-native/native-gate.log, fallback-gate.log, traffic-gate.log, traffic-gate-recheck.log, traffic-results.json; guest-home private QSC/build logs. Internal artifacts only, not public evaluation results.

Remaining target core: resolve module ABI or reliable fallback RX/TX; native application/EDU implementation and compilation; IRQ/DMA/resmgr; supervision/secpol; QPP; SSH crash; target continuity/restart/fault acceptance and truthful captures. Host tests do not satisfy these. No publication, Pages, PRs, videos, submission or spending.

Watchdog still NOT installed. qnx-watchdog.timer list showed zero timers. No exposed supported scheduled-agent creation/wake route; shell POST/CLI/direct-RPC messaging prohibited. No Gateway token read or shell bypass installed. Requested2h schedule inactive; no actual stop command.
