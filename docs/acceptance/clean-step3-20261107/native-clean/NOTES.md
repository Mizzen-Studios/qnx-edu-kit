# Fresh clean-platform learner step3

**Wrong edit: intended stage FAIL/1, application exit0. Correct edit: native PASS/0.** Only wrong device_readback failed; source/binary binding, QNX identification, ordering, target exit0, disk immutability, bounded completion and stopped/reaped QEMU passed for both. No reference checker was invoked.

Both edited sources were freshly qcc-compiled and mkifs-linked against the fresh stock generic platform built with guest swap. Original local ifs_files.learner and post_start.learner snippets install only the application/wrapper and invoke after PCI readiness. No E1/private cache or stripped kernel. Same fresh disk SHA64db806fb1307b5cb4b3b8451c35427e39c65ff55c0db63f284b2398db82bb03 for both target boots.

The SDK guest stopped/reaped exit0 before native execution. Actual native caps100000/100000 CPU,1073741824 memory,nice15,1vCPU/512MiB; exclusive caller-held flock observed. Source/build/run-driver/image/disk hashes are in receipts. Step3 oracle exact source remained unchanged from97fabc1 (SHA2564fc3e2a966d186f8e1020ee705a3e364723066e75074ed6982b065c99dc93b1e).

## Important limit

Both raw target logs retain **Memory fault (core dumped)** immediately after the startup message **Starting sshd**, before the learner wrapper. The faulting process was not identified. The learner process itself completed with the expected observed device values and exit0. This is a scoped BAR/bootstrap journey result, **not a healthy-all-services image, SSH acceptance, independent re-review, broad portability, or complete learner-course acceptance**. No claim that this unrelated startup fault is fixed.

Original failure/diagnosis900 receipts remain unchanged. The owner gate has not been independently reassessed. /dev/edu learner completion is a separate authorized next result.
