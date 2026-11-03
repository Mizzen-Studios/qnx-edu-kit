# QNX platform/source gate report — 2026-11-03 UTC

Scope: read plan_v3.md completely; bounded read-only host and upstream investigation. No repository modifications, installs, SDK/image downloads, account creation, spend, public writes, or contact. Only this report is written. GPL emulator source declarations were inspected remotely as hardware-model evidence; no GPL driver code copied or stored.

## Decision summary

- **NO-GO for live x86_64 KVM/QSTI validation on this host as currently configured.** Host is ARM64, /dev/kvm absent, no discovered QEMU system binaries/packages. This is a host prerequisite failure, not proof QNX or SocketCAN lacks x86_64 support.
- **GO for further source/design work, conditional for SocketCAN integration.** Contrary to a possible reading of the missing board directories, upstream explicitly supplies an x86_64 mods-can.so. Do NOT trigger the libcan fallback merely because boards lack x86_64 directories.
- **NO-GO for claiming a reproducible public-source build of mods-can.so.** README explicitly says internal io-sock hooks are required, remaining source is not released, and public module source cannot currently build.
- **NOT TESTED:** binary loading/ABI compatibility, QSTI QEMU devices/properties, all guest traffic/IRQ/DMA, io-sock isolation, SLM/HAM, secpol, QPP. No live success claimed.
- **Licensing hold before copying templates:** repository Apache-2.0 metadata coexists with explicitly proprietary headers in vcan files. Retain file-by-file notices and resolve permissions rather than blanket-relicensing copied glue.

## Host evidence

Commands: uname -a; cat /etc/os-release; ls -l /dev/kvm; id; command -v qemu-system-x86_64 qemu-system-aarch64 qemu-kvm gh; dpkg-query -W '*qemu*'; find /usr/bin /usr/local/bin /home/linuxbrew/.linuxbrew/bin -maxdepth 1 -name '*qemu*'.

- Linux open-claw-vnic 7.0.0-1013-oracle, aarch64.
- Ubuntu 24.04.5 LTS (Noble).
- /dev/kvm: No such file or directory.
- ubuntu uid 1001; groups include sudo but no kvm.
- No QEMU paths found in PATH or those standard binary directories; dpkg-query emitted no QEMU package records. Bounded inspection does not exclude arbitrary custom binaries elsewhere.
- Therefore no installed QEMU version, -device help, -object help, or edu property output available. No claim about this nonexistent binary's device support can be made.
- x86_64 guests cannot use native KVM acceleration on this ARM64 CPU. TCG cross-architecture emulation is a different, untested route requiring QEMU installation and approved SDK/image provisioning; it does not satisfy the plan's x86_64 KVM baseline. No new resources were provisioned.

## Pinned qnx/socketcan evidence

Current main observed via GitHub API: **9db62b4747d84135a500dbfe3a318a4330f31654**. Repository pushed_at 2026-09-29T20:47:47Z; GitHub license metadata Apache-2.0. No releases listed by releases API.

Base URL: https://github.com/qnx/socketcan/tree/9db62b4747d84135a500dbfe3a318a4330f31654

1. README: https://github.com/qnx/socketcan/blob/9db62b4747d84135a500dbfe3a318a4330f31654/README.md
   - Experimental, incomplete, no formal support/testing/certification guarantees; not monitored/scanned under their Cybersecurity Management Standard.
   - Must cross-compile; no self-hosted builds.
   - Exact module-build statement: “The module cannot currently be built due to requiring some internal hooks.” Supplied aarch64 and x86_64 modules; remaining source reference-only until internal dependencies removed.
   - Documents separate io-sock stack with prefix=/can, SOCK=/can ifconfig and vcan0 create. This is documented support, not a performed x86_64 runtime test.
   - CAN_RAW implemented; CAN_BCM explicitly unsupported and not planned. “Linux-identical API” must be qualified.
2. **x86_64 binary exists** at lib/can/nto/x86_64/dll/mods-can.so, size **22448 bytes**, Git blob SHA **b3f0a748aedb981e9a20df9443917c4463b1dda5**.
   - API metadata: https://api.github.com/repos/qnx/socketcan/contents/lib/can/nto/x86_64/dll/mods-can.so?ref=9db62b4747d84135a500dbfe3a318a4330f31654
   - Pinned raw URL: https://raw.githubusercontent.com/qnx/socketcan/9db62b4747d84135a500dbfe3a318a4330f31654/lib/can/nto/x86_64/dll/mods-can.so
   - Binary was NOT downloaded. Blob SHA is Git object identity, **not SHA-256 of file bytes**. ELF architecture/content, SHA-256 and loader compatibility remain unverified.
3. Recursive tree at pinned commit: lib/can has nto/x86_64/dll makefiles and binary; sample readers/writers have x86_64 directories; can-utils has x86_64-qnx.cmake. Four boards (dummy/libcan/mcp25xxfd/vcan) have only nto/aarch64 variants. **No x86_64 board build directory or SJA1000 board exists in that tree.** This is missing build scaffolding/implementation, not an upstream declaration that x86_64 driver builds are unsupported.
4. Build prerequisites observed:
   - Top Makefile includes recurse.mk; board common.mk includes qconfig.mk and devs/devs.mk; module common.mk includes devs/mods.mk. Need licensed compatible QNX SDP environment plus io-sock driver development headers/build rules, not just a generic C compiler.
   - Public libsockcan.h includes io-sock/FreeBSD-style sys/mbuf.h, sys/module.h etc. Verify SDK-installed Network/io-sock DDK components expose the required interfaces and compatible IOSOCK_VERSION_CUR/ABI. No exact package entitlement/version was established here.
   - can-utils README instructs sourcing qnxsdp-env.sh, initializing its linux-can/can-utils submodule, CMake configure.sh x86_64 then make. Toolchain sets QNX version 800, qcc target gcc_ntox86_64, QNX_HOST/QNX_TARGET, libsocket and static libepoll.
   - Public board builds and supplied binary consumption are separate from impossible public-source rebuild of mods-can.
5. API compatibility caveat: mcp25xxfd README explicitly says Linux PF_CAN=29 versus QNX PF_CAN=44, requiring supplied headers. Only cangen/candump stated used; other can-utils functionality not comprehensively verified.

## Licensing evidence / limitations

- LICENSE.md is Apache-2.0: https://github.com/qnx/socketcan/blob/9db62b4747d84135a500dbfe3a318a4330f31654/LICENSE.md
- boards/can-dummy/dummy.c, lib/can/public/hw/libsockcan.h and lib/can/sockcan.c have Apache-2.0 headers.
- **boards/can-vcan/vcan_module.c and vcan.h have BlackBerry proprietary notices**, saying use/reproduction/disclosure/distribution without an express license agreement is prohibited, despite the repo-wide license metadata. URLs: append those paths to the pinned blob base. Do not assume metadata removes these notices. This report is not a legal determination of effective terms.
- README refers to QDL for Experimental Software. SDK/toolchain/image use and any unpublished binary rights are not established by GitHub's license classifier alone. Need owner-reviewed applicable QDL/noncommercial terms and file/binary provenance before redistribution.
- No GPL CAN driver source was inspected/copied. Implement from public interfaces and hardware-model/spec facts; preserve Apache and other notices for any lawful reuse. can-utils dependency licensing needs separate review before shipping its artifacts.
- Plan's QDL 4.6(i) label workaround was not legally validated: labeling an evaluation “app budget, not a benchmark” is not proof publication is permitted. Review actual applicable terms before publishing functional/performance evaluation results.

## QEMU upstream source reference — NOT host or QSTI validation

Pinned references inspected through GitHub contents API:
- QEMU **v6.2.0 commit 44f28df24767cf9dca1ddc9b23157737c4cbb645**.
- QEMU **v10.1.0 commit f8b2f64e2336a28bf0d50b6ef8a7d8c013e9bcf3**.
- At both commits, hw/misc/edu.c exposes writable object property dma_mask initialized to (1UL << 28) - 1; hw/net/can/can_kvaser_pci.c declares kvaser_pci; net/can/can_socketcan.c declares can-host-socketcan.
- v10.1 Kvaser model: vendor 10e8/device 8406, S5920 BAR0, SJA1000 BAR1, Xilinx BAR2, I/O BARs; INTCSR offset 0x38/add-on interrupt-enable 0x2000. Supports design assumptions at source level, not actual compiled-binary inclusion.
- v10.1 net/can/meson.build conditionally includes SocketCAN backend when host OS is Linux; CAN_BUS build gating applies. Version string alone is insufficient: inspect actual QSTI-provided binary.
- An attempted hw/net/can/Kconfig path returned 404; no inference from that missing path.

URLs:
https://github.com/qemu/qemu/blob/44f28df24767cf9dca1ddc9b23157737c4cbb645/hw/misc/edu.c
https://github.com/qemu/qemu/blob/44f28df24767cf9dca1ddc9b23157737c4cbb645/hw/net/can/can_kvaser_pci.c
https://github.com/qemu/qemu/blob/44f28df24767cf9dca1ddc9b23157737c4cbb645/net/can/can_socketcan.c
https://github.com/qemu/qemu/blob/f8b2f64e2336a28bf0d50b6ef8a7d8c013e9bcf3/net/can/meson.build

Official EDU documentation fetched HTTP 200: https://www.qemu.org/docs/master/specs/edu.html (page reports QEMU 11.1.50; mutable master, not target version). It documents -device edu[,dma_mask=mask], 28-bit default, 1234:11e8, 1MiB BAR0 MMIO, DMA direction bit 0x02 (0 RAM→EDU; 1 EDU→RAM), IRQ request 0x04 leading to status 0x100, 4096-byte device buffer at 0x40000, INTx default/MSI possible. These resolve documentation-level uncertainty only; live guest register/IRQ/DMA tests remain required. Do not claim a live DMA property test.

## Official hackathon verification and discrepancies

https://qnx.devpost.com/rules and https://qnx.devpost.com/ both returned **403 Cloudflare “Just a moment...”** through web_fetch. Search tool unavailable (disabled/no provider). No browser session was used or altered. Hence official deadline, categories, eligibility, judging, prize caps and tutorial treatment **could not independently be reverified**. No verified deadline discrepancy found; **15 December 2026 19:00 UK remains plan-provided, not independently confirmed**. No organizer contact made. Do not translate access failure into changed rules.

Actual evidence discrepancies/qualifications from plan:
- Lack of x86_64 board directories must not be confused with lack of x86_64 mods-can.so: binary is explicitly supplied.
- Supplied module is NOT publicly source-buildable; root make does not fix missing internal hooks.
- Blanket Apache/template-copy assumptions require file-level review because vcan glue/header notices conflict with metadata.
- “Linux-identical” needs RAW-only/header-value caveats; unsupported BCM is explicit.
- Current VM is not the plan's Ubuntu x86_64 KVM host. Upstream device existence does not clear QSTI binary gate.

## Concrete unblock requirements (no actions taken)

1. Owner designate an existing zero-spend **x86_64 Linux host with usable /dev/kvm** and approved access; or explicitly revise architecture to unproven ARM64→x86_64 TCG and accept its limitations. No paid VM provisioned.
2. Owner-provided, lawfully licensed SDP 8.0/QSTI environment/image and applicable license acceptance/provisioning authorization. Record SDP build, io-sock version and DDK components. No account/download authorization presumed.
3. Obtain actual QSTI QEMU path/version; run read-only --version, -device help, -object help, -device edu,help (or QOM property inspection). Require kvaser_pci, can-host-socketcan and edu/dma_mask, plus working host SocketCAN/vcan and any needed administrative network permission.
4. After download permission, fetch only pinned x86_64 module into SDK-excluded external artifact storage, compute SHA-256, inspect ELF, then test loading against chosen io-sock. Run x86_64 vcan source-build spike with compatible board build scaffolding before committing to new SJA1000 implementation. No unverified SDK material in repos.
5. Resolve proprietary-notice/template/binary license questions and QDL publication restrictions from applicable terms. Escalate to owner; do not contact QNX/Devpost without permission.
6. Only then live gates: /can separate instance, create/up interface, RAW RX/TX byte exact, untouched main-stack PID/SSH, repeated restart; edu register/IRQ/DMA verification. Record failures as failures, unperformed checks as not tested.
7. Official rules need an accessible official page or owner-provided dated full rules copy. Tutorial bonus attribution remains unresolved unless clear text settles it; no contact implied.
