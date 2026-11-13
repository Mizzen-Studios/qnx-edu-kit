# Nov13 clean stock EDU gate — BLOCKED_CLEAN_STOCK_IFS_OOM

One newly generated stock project, not CAN-gate, incident.ifs or the advanced custom learner image. Existing licensed SDP only; mkqnximage --type=qemu --arch=x86_64 --ram=512M --cpu=1 --ssh-ident=none --build. The only authored snippet was qemu_options.edu containing -device edu. No lesson binaries, filesystem/startup snippets or custom BSP/IFS integration. Generated QEMU_OPTIONS matched the12-byte snippet; installed launcher option flow was verified separately.

The build reached Generating ifs and guest kernel killed PID1620 x86_64-pc-nto-q at09:03:44UTC, anonRSS329384KiB. Service Result=oom-kill, main status15. The512MiB SDK guest reported295232KiB available immediately before generator invocation; minimum availability during mkifs was not captured. The exact internal relink input is UNVERIFIED, not borrowed from CAN or Nov10.

This was a guest OOM, not a demonstrated HOST2GiB limit breach. HOST monitored peak1105190912bytes, swap0 and sampled hostOOM events0; enforced caps2GiB/CPU100%/nice15/TCG256/guest512/smp1/reserve64. Sampling ended at the stop request; hard cgroup caps remained in force through shutdown. No memory increase, swap/platform/package/SDK login/install or repairs/retries.

ifs.bin is zero bytes (empty-file hash), not a valid image. No disk-qemu or VMDK was produced; disk hashes are absent, not substituted from old images. Partial data/system partitions remain on original SDK disk and are hashed. Source-bound already-compiled wrong/finish artifacts were verified against HostShare records; they were NOT transferred/executed on stock. Corrected source was NOT created. No HOST stock boot or new lesson/native/pulse/slog2/trace proof. Do not promote the stock-first draft.

Failed build service stopped, build process list empty; SDK ACPI stop succeeded, owner child reaped exit0. Independent no-QEMU and free-lock check recorded in cleanup.json. Stop EDU lane for review. No more builds/native attempts. Original advanced tutorial and historical receipts are untouched. Raw diagnostic log remains private; sanitized tool/resource output only, no SDK implementation or binary contents in git.
