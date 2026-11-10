# Nov10 bounded EDU feature gate — BLOCKED_STOCK_MKIFS_OOM

Existing licensed SDK only; one capped SDK build attempt, no native QNX run. Own wrong-step3 source compiled and linked serially (-O0 -g0); QNX ELF retained privately. Bootstrap then reached stock mkqnximage / Generating ifs. Guest kernel killed PID1617 x86_64-pc-nto-q (anon RSS328616KiB); build service Result=oom-kill, main status15. ifs.bin is zero bytes, not an image. Exact internal relink input was not captured: UNVERIFIED, not inferred from CAN.

No wrong FAIL/app0 observation, corrected source, corrected PASS, step6 pulse/slog2 or trace run. Stop on this gate; no retries, swap/cap/package/platform changes. The new implementation is not native-accepted. Nov8 historical receipts remain unchanged and do not prove added features.

Original own source/object/ELF and partial partitions stay on the existing SDK disk; source/object/ELF copied privately to the authorized host share. Hashes only, no binaries/images/SDK contents in git. Bootable disk-qemu was not produced. SDK service stopped, all QEMU reaped and owner result collected exit0; lease independently tested free. CAN transient units were observed active after boot; EDU changed no units.

See receipt.json for evidence hashes, exact source SHA, resources and NOT_RUN stages. Dispatch/observer/preservation scripts record the actual commands. Prior short boot-readiness waits expired without any dispatch; the same single boot subsequently became ready. The build was dispatched exactly once as the existing licensed qnx user in an isolated system service.

Redistribution guard review: four SDK environment-export banner lines are omitted from committed build.log; original log stays private with raw hash in receipt.json. Commands, phase/resource rows and OOM evidence are unchanged. Guard itself is unchanged.
