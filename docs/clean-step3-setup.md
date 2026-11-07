# Clean learner-owned bootstrap — tested narrow configuration

**Companion/reference details: start with the [canonical learner route](learner-route.md), integrating step3 then your own /dev/edu.**

Fresh clean-platform step3 now has **wrong-edit intended FAIL and corrected native
PASS**, with source/binary/image/disk provenance. [Receipts](acceptance/clean-step3-20261107/native-clean/NOTES.md).
This is one automated run on the configuration below, not independent re-review,
two fresh human learners, QSTI acceptance or broad portability. The owner gate has
not been independently reassessed. No SDK/BSP/image/disk/library/licence is distributed.

## Platform and memory actually tested

Licensed Linux x86_64 SDP 8, Generic x86_64 BSP 0.0.1.00050T202311201204L,
mkqnximage 0.5.0.00132T202605281115L; QEMU 8.2.2 x86_64 pc TCG.
Host cgroup CPUQuota 100%, MemoryMax 1 GiB, nice 15; one vCPU, 512 MiB SDK guest.
**512 MiB guest RAM with no swap was insufficient** for the unmodified stock kernel
link. **512 MiB RAM plus 1 GiB disk-backed guest swap completed it.** This is a tested
configuration, not a measured minimum RAM requirement. Existing host swap settings
were unchanged. Target QNX guests remain 1 vCPU / 512 MiB, under the same host caps.

Bring an already installed licensed SDP/BSP. No login, paid download, installation,
activation or licence change is part of this procedure. An ARM host may use its
existing x86_64 SDK VM. Serialize SDK and native QEMU with the same exclusive flock;
never use the historical 200% / 4 GiB launcher. No E1 buildfiles/images, owner bundles,
private stripped kernel or cached image substitution.

## Read-only preflight

Copy original scripts and edited C to the licensed SDK host. Choose a nonexistent
external work directory and run:

    python3 learner_clean_preflight.py --sdp-env /licensed/qnx800/qnxsdp-env.sh --fresh-work /external/clean-platform

Exit 2 is blocked; preserve JSON. Exit 0 permits an attempt, not native success.
The probe installs nothing and launches no QEMU. Trust the supplied environment
script; normal compiler licensing remains authoritative.

## Guest swap and isolated build ownership

Inside the Linux build guest, as root, create a new 1 GiB file on its existing disk,
not tmpfs or the shared 9p filesystem. Refuse to overwrite an existing file. The
recorded commands used dd, chmod 600, mkswap and swapon on /var/tmp/edu-build.swap.
No fstab entry was added. On a later SDK boot, explicitly activate that same file
before linking; shutdown deactivates swap. Check free-m and available disk first.
The original scripts are in [the attempt evidence](acceptance/clean-step3-20261107/swap-attempt/NOTES.md).

Run the compiler/image builder in **its own transient guest systemd service**,
not as a descendant of host-queue.service. The prior guest OOM killed the linker;
OOMPolicy=stop then killed the queue controller too. The successful attempt used
an isolated service, 1800-second command timeout and 1830-second service ceiling.
Queue diagnostics remained outside it; queue restart count stayed 0. Preserve
Result, ExecMainCode, ExecMainStatus, MainPID and terminal ActiveState. A transport
error or active service with default status 0 is not a terminal-success receipt.

Keep the launcher **outside** the fresh image directory: mkqnximage rejects a
nonempty unknown directory. The initial launcher-placement rejection is preserved;
no compiler/linker ran in that invocation. Do not silence it with --force.

## Fresh generic image and application-only integration

These original instructions use the documented [mkqnximage local snippets](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.utilities/topic/m/mkqnximage.html).
All generated platform files remain outside Git.

1. Source the licensed SDP environment in an empty external directory. Run
   `mkqnximage --type=qemu --arch=x86_64 --build --ssh-ident=none`, never --run.
   Keep the stock kernel unmodified. Preserve final IFS and disk hashes and size.
2. Create an external learner-active directory. Its absolute location must match
   the application-only snippet paths. Preseed a freshly compiled learner_bin
   and a wrapper that exits 2 solely to let the platform generator resolve files;
   **this preseed image is not assessed as learner completion**.
3. Add local/snippets/ifs_files.learner containing the two entries from
   scripts/learner-step3.build.in, with @OUT@ replaced by learner-active's path.
   Add local/snippets/post_start.learner with a bounded waitfor for
   /dev/pci/server_id_1 followed by sh /proc/boot/learner-start.sh. This supported
   hook runs after the stock platform startup; no E1 startup is copied.
4. Run mkqnximage --build to generate the integrated platform and matching raw
   output/disk-qemu. Hash the original snippets and generated build/startup files.
   Keep the generated platform implementation outside the repository.
5. Run learner_lab.py build with the actual edited source, out=learner-active,
   the installed SDP environment, buildfile=output/build/ifs.build and
   bsp-cwd=the clean platform directory. It freshly qcc-compiles and mkifs-links,
   replacing the preseed wrapper with actual source/binary binding and target exit.
   Preserve the full resulting bundle outside Git for each variant **before**
   replacing learner-active for another build. Keep the same matching clean disk.

## Wrong edit then corrected edit

Use [the step3 learner loop](learner-lab.md). Wrong write 12345679 must actually
read edcba986 and fail the fixed stage oracle even if the application exits 0.
Correct write 12345678 must read edcba987 and pass in a fresh boot. The oracle was
unchanged. Both runs bind source, binary, image, disk, build/run driver and startup.

Stop/reap the SDK guest before target QEMU. Hold the exclusive lease throughout
each phase, and only set EDU_NATIVE_LEASE=granted while owning it. Actual validation
lock: $EDU_NATIVE_LOCK (your chosen external shared lock). Never interrupt another project.

## Remaining limits and chronology

The original 240-second failure and [diagnosis900 OOM receipts](acceptance/clean-step3-20261107/diagnosis900/NOTES.md)
remain unchanged. The [swap build](acceptance/clean-step3-20261107/swap-attempt/NOTES.md)
completed with nonempty stock IFS and disk; subsequent fresh wrong/correct native
runs reached the intended learner stage. Guest soft-lockup warnings are preserved.

Both target startup logs also contain an **unattributed Memory fault immediately
after Starting sshd**, before the learner. This scope does not establish healthy
SSH or all-platform service health, and that fault is not claimed fixed.
The separate [/dev/edu learner finish](learner-dev-edu.md) is not a reference PASS
transfer. C6 remains STOPPED; no safety, timing or production-driver claims.

Startup diagnosis attributes the observed failure to **sshd** in a separately traced image; internal cause remains UNVERIFIED. [Separate baseline/diagnostic bindings](acceptance/startup-diagnosis-20261107/NOTES.md). No SSH/platform health claim.

[Fresh isolated checkout reproduction and preserved failures](acceptance/fresh-checkout-20261107/NOTES.md): wrong/corrected step3 and corrected learner /dev/edu observed; installed SDK reused, independent human/owner re-review remains not done.
