# Native recovery checkpoint — 4 November 2026

Private target development evidence, not completed tutorial acceptance.

- Licensed SDK and images remain outside the repository. No SDK code/headers/binaries are redistributed.
- Original native/edu_probe.c compiled with installed SDP8 qcc -Vgcc_ntox86_64 -Wall -Wextra -Werror and -lpci into an external QNX x86_64 ELF. APIs were checked against installed headers, not invented declarations.
- Probe attempts exclusive PCI attach, BAR0 mapping, ID/liveness, factorial10 and bounded interrupt raise/wait/ack; cleanup detaches and unmaps. No resource manager or DMA implementation is claimed.
- Three native executions exited139 (Memory fault). Final source initializes the PCI error output and checks the returned handle rather than treating the error output as a success result. Unbuffered target evidence reaches EDU PROBE BEGIN and EDU PCI attached, then faults before any BAR evidence. Compiled ELF/PCI attach is NOT MMIO/factorial/IRQ acceptance. Keep native tutorial checks BLOCKED; inspect the private core and BAR/library ABI path before implementing DMA/resmgr on it.
- Shared CAN investigation found a legacy interrupt-routing discrepancy (QNX IRQ10 vs QEMU PIRQ routing/PCI IRQ11). Explicit experimental host PIRQ correction enables paced100/100 byte-exact CAN RX/TX. It is not yet an image/BSP routing fix.
- SSH configuration test exits139 normally but0 with OPENSSL_ia32cap=0. Starting the daemon with that workaround then exits255: /usr/libexec/sshd-auth does not exist or is not executable. Both sshd-auth and sshd-session exist in the external installed SDK; adding them to system_files.custom did NOT make them appear at the expected runtime paths. Helper packaging and boot-time environment still need repair. No working SSH connection is claimed.

Compile source only inside the licensed x86 SDK guest. Direct the executable to an external directory, for example /home/qnx/qnx-work/edu_probe, never this checkout. Host-only tests cannot validate native code or substitute for target evidence.
