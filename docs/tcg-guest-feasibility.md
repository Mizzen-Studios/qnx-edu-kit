# x86_64 Linux under ARM64 TCG: PASS

Observed 2026-11-03 on this existing ARM64 Oracle Ubuntu VM only. QEMU 8.2.2, no KVM, explicit -accel tcg,thread=single; 1 vCPU, 256 MiB RAM. No networking, display, monitor socket, listening port or persistent process. QEMU exited 0 after guest poweroff; 180s enforced timeout was not reached.

## Result

- Measured host wall time (QEMU invocation through poweroff/exit): **7.872045 seconds**. Single smoke-test observation, not a performance benchmark or projection.
- Real guest: Linux 6.12.114-0-virt, x86_64; Alpine 3.22.7.
- Actual guest userspace: uname, cat, sha256sum and shell arithmetic worked. Arithmetic 123*456=56088. hello-x86_64-linux plus newline SHA256 c3d19276efb03d108b5d0ea201f36fb9609e9b2f48f076bb34508015e3c0fa02.
- Serial markers TCG_GUEST_BEGIN, TCG_GUEST_PASS, TCG_GUEST_POWEROFF, then kernel reboot: Power down.
- Guest PCI sysfs enumerated Kvaser PCICAN at 0000:00:03.0, **10e8:8406**; EDU at 0000:00:04.0, **1234:11e8**. EDU instantiated with dma_mask=0xffffffff. This proves enumeration/instantiation only, NOT Linux or QNX driver operation, interrupts, DMA or CAN frame exchange.
- Separate bounded can-host-socketcan instantiation exited 1: "SocketCAN host interface vcan0 not available: No such device". Host vcan0 does not exist. This is missing host interface, not missing QEMU SocketCAN object support. No host interface changes attempted.
- Final pgrep found no qemu-system-x86_64 process.

## Official source and verification

Official HTTPS base: https://dl-cdn.alpinelinux.org/alpine/v3.22/releases/x86_64/

Both artifacts downloaded alongside their official .sha256 sidecars and passed sha256sum -c:

- alpine-minirootfs-3.22.7-x86_64.tar.gz: 57e364a241bab0699cd8a760c0fd7b270e9cbcbd3cee822cb2b07ca6d925c16c
- alpine-virt-3.22.7-x86_64.iso: c345ec65055908734523e03e81137a2e2f82f0094eb2b6e99bc6e07a7d2a0556

Kernel extracted from checksum-verified ISO boot/vmlinuz-virt: SHA256 26f146f664ad057be3b39b211422b03b1f94cb2c3d66522fd4841811a224bfd5.
Custom initramfs assembled from verified minirootfs and included init shell: SHA256 763736dcecf2060e3bab9fb6cd4bf28a3070d205b1890afc4406188bc7788a3b. Generated initramfs hashes can vary on rebuild due metadata/time.

A direct netboot kernel .sha256 URL returned 404 during preparation, so the tested kernel was instead extracted from the official SHA256-verified ISO; the unverified netboot kernel was not downloaded or used. SHA256 sidecars were retrieved over official HTTPS, not separately signature-verified.

## Reproduce and evidence

Run bash run-test.sh in this directory (requires installed QEMU, curl, 7z, tar, cpio, gzip, python3). It verifies source checksums, extracts kernel, builds tiny ~3.8MiB initramfs and runs bounded boot. Full QEMU argv and wall time are in result.json. Logs: serial.log, run.log, host-evidence.log, verification.log, extraction.log, cpio.log, derived-artifacts.sha256, socketcan-probe.log. Original source sidecars retained.

SocketCAN reproduction (no host mutations):

    timeout 5 qemu-system-x86_64 -accel tcg,thread=single -machine pc -smp 1 -m 128 -display none -monitor none -serial none -nic none -S -object can-bus,id=canbus0 -object can-host-socketcan,id=hostcan0,if=vcan0,canbus=canbus0

## Scope limitations

This proves a free Linux x86_64 full-system boot and basic userspace under TCG on THIS ARM64 VM. **QNX, SDK, qcc compilation speed, QNX boot, mods-can.so, SDK license/access, driver integration and QNX application performance were not tested.** No SDK/accounts/QNX images installed. No paid resources, repository changes or host package changes made by this lane. All task writes are confined to this guest directory.
