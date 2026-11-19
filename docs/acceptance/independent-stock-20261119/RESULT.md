# Independently built stock admission — 19 November 2026

## Result: HOST implemented; actual fresh build BLOCKED

The explicit cooperative own-build admission route is implemented separately from strict historical pinned reuse. Original `learner_stock.PINS` and historical receipts/failure bytes are unchanged. Cooperative provenance is **not cryptographic stock attestation, licence certification or independent-human validation**.

The one actual SDK attempt used source `593b2ccaaa1ff6617371cf99e2ef1308ce472094`, the existing legal SDK and controller, a fresh project and the canonical stock recipe with only the EDU QEMU-options snippet. It reached “Building disk” but the existing monitor stopped it for `MemoryError('reserve')`. Peak cgroup memory **2,095,493,120 bytes + 67,108,864 reserve > 2,147,483,648 limit** (15,118,336 bytes over the reserve threshold). This is a reserve64 breach, not a demonstrated hard-limit OOM: measured OOM events and swap usage remained zero. CPU100%, HOST2GiB, swap0, nice15, smp1, SDK1024MiB and TCG256 were retained. No cap was raised; no retry occurred.

Original queue request `1795113265349792925` has no successful EOF/return code. No final stock manifest, owner admission receipt or admitted image exists. Actual pre-build tool measurements were not durably persisted before this abort; they must not be inferred from later source. Subsequent HOST-only changes persist invocation/tool-version diagnostics before the command and stop the owned controller waiter when its SDK monitor exits. They have **not** been rerun in the SDK.

SDK owner reports `stopped_reaped: true`; its owned child exited0. QMP stop returned1 during connection reset; this is disclosed, not recast as clean command success. Owned HOST waiters were terminated only after SDK reaping was proven. Final observation: zero QEMU, zero queued `*.sh`, exclusive lease **FREE**; historical consumed `.running` requests were preserved.

## Native acceptance: NOT RUN

No new own notebook/source was created, no application or native QNX guest launched, and no wrong FAIL/app0 → corrected PASS → own step6 normal/dev/edu10 → 3628800/IRQack/private-pulse/slog2 chain or new export was obtained. Historical receipts were not used as live evidence. This item cannot be called native accepted, and no fresh-image success or independent-human validation is claimed. Native work stopped at the authorized critical resource blocker.

## HOST verification and evidence

The suite retains the original143 tests and adds19 admission/export/controller negatives (162 total; two existing skips). The fresh route requires the separately trusted owner receipt digest, exact typed schemas, recipe/tool/source/input/output bindings and reaped-owner handoff; arbitrary supplied hashes alone are not admitted. Changed image/disk/options/tools, mixed manifests/owners, unsafe paths/symlinks, custom inputs and incomplete exports fail closed. Learner controller/session/notebook/export and docs distinguish own-build from pinned reuse.

- [Typed source-bound attempt](attempt.json): caps, hashes, missing-completion facts and cleanup.
- [Sanitized monitor receipt](sdk-owner.sanitized.json).
- [Sanitized actual build phases](build-phases.sanitized.txt); no images, SDK tools/libraries/licences/secrets or licensed raw ELF transfers are committed.
- [Clean learner commands and trust boundary](../../independent-stock.md).

Historical T01 proof/claim-copy gates still FAIL for frozen README, codelab and learner-route drift and stale historical reports. No historical dry-pack was repinned and no validator was weakened. Those gates are distinct from HOST tests/CI and native acceptance. Owner Devpost wording remains an external private local draft; nothing was submitted, published or made visible.
