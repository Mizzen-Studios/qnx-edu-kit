# Clean learner-owned step3 bootstrap

**Portability UNVERIFIED** until independent clean source/binary/image-bound negative and corrected fresh boots both exist. Earlier E1 receipts do not validate this path. No SDK/BSP/image/disk/library/licence is distributed.

## Narrow platform and prerequisites

Licensed Linux x86_64 SDP 8 and Generic x86_64 components; QEMU x86_64 pc TCG. Scope: PCI attachment, BAR0 ID and complement only. Not QSTI, IRQ, DMA, security policy, resource managers or C6 (STOPPED).

Bring an already installed licensed SDP/BSP. No login, paid downloads, installation, activation or licence changes. An ARM host can use an existing x86_64 SDK VM. Serialize all SDK/native QEMU under the same flock: CPUQuota=100%, MemoryMax=1G, nice 15, one vCPU, 512 MiB guest. Never use the older 200%/4G launcher or increase caps.

These original instructions use the public [QNX 8 mkqnximage reference](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.utilities/topic/m/mkqnximage.html) empty-directory and local-snippet interfaces. Keep licensed implementation external. No E1 buildfiles/images, owner bundles, can-gate/edu-followup outputs or private stripped kernels.

## Read-only preflight

Copy original scripts and edited C to the licensed SDK host. Choose a nonexistent external work directory:

    python3 learner_clean_preflight.py --sdp-env /licensed/qnx800/qnxsdp-env.sh --fresh-work /external/clean-step3

Exit 2 means blocked; preserve JSON. Exit 0 permits an attempt, not native success or complete BSP readiness. Probe executes no compiler/image builder, creates no workspace and launches no QEMU. Environment script must be trusted. Normal compiler licensing checks remain authoritative.

## Fresh generic platform

1. Source the SDP environment. Make the fresh external directory. Inspect and preserve mkqnximage --help=brief. Generate with mkqnximage --type=qemu --arch=x86_64 --build, never --run. Preserve failure output. Default services do not expand assessment scope.
2. Use documented local/snippets/ifs_files.custom to install fresh learner_bin and learner-start.sh at /proc/boot, mode 0755. scripts/learner-step3.build.in supplies only those two application entries, not a BSP.
3. Use local/snippets/post_start.custom to invoke sh /proc/boot/learner-start.sh after platform startup/PCI readiness. Licensed platform must provide pci-server, libpci and x86 hardware modules. Inspect its documented startup rather than invent configuration or copy E1.
4. Generate the disk/buildfile from these clean inputs. Invoke learner_lab.py build with the external generated buildfile/cwd referring to the variant-specific new output directory. It qcc-compiles the source snapshot and invokes mkifs. Use only a disk from the fresh platform. Keep options/buildfile/startup hashes externally, never proprietary files in Git.

If unmodified linking exceeds the capped SDK VM, preserve OOM/link failure and stop. Private stripped kernels/cached images cannot establish portability; no silent substitutes.

## Negative then corrected

Initialize using learner_lab.py init and complete step3 per [learner-lab.md](learner-lab.md). Require memory BAR0 extent >=0x1000, map uncached, print actual volatile observations. Keep artifacts external.

First wrong write 0x12345679 should observe complement 0xedcba986; deliberately print application PASS/exit 0. Fresh stage must FAIL/1 despite app PASS/0. Correct write to 0x12345678 and require 0xedcba987, rebuild/fresh boot: stage must PASS/0. Both need source/binary/image/disk/driver bindings, target exit, caps, locked lease and stopped/reaped QEMU. Existing runner/oracle unchanged. Host tests/compilation/saved logs cannot replace boots.

Stop/reap SDK before target QEMU. Hold the same flock across phases, clean up every owned guest, release at end. Validation lock: /home/ubuntu/qnx-host/native-test.lock. Never interrupt another project. Missing prerequisites mean BLOCKED and portability UNVERIFIED, not inferred PASS or learner failure.

## Actual bounded attempt

See [receipts](acceptance/clean-step3-20261107/NOTES.md): both edited sources compiled, but clean generic image generation reached IFS then its bounded termination (zero-byte IFS). No native runs. This is not a proven OOM, missing SDK or portable bootstrap PASS.
