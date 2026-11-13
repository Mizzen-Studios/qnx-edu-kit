# Fresh stock retry — 13 November 2026

**BLOCKED_STOCK_NATIVE_IRQ_TIMEOUT. Wave stopped; guests reaped; lease FREE.**

The one authorized clean stock-generation retry with SDK guest1024MiB succeeded, and its fresh stock image booted twice with target512MiB. Earlier guest512 OOM receipt in `../stock-20261113` is unchanged. No second image-generation retry; only a separate correction compile/link boot. Stock QEMU_OPTIONS adds only `-device edu`; lessons are copied after boot, never injected into IFS. See `stock-artifact-handoff.json` for external paths and hashes for parent-coordinated HostShare N7.

## Native results

- Wrong edit: actual `id=010000ed write=12345679 read=edcba986`, app0. Fixed-value oracle FAIL as intended; matching slog2 event. Exact guest ELF bytes verified before execution.
- Only after observing wrong: corrected source created, serially compiled/linked in existing SDK, source/object/ELF hashes verified; SDK stopped/reaped before native.
- Correction: actual `id=010000ed write=12345678 read=edcba987`, app0, matching slog2 event: PASS.
- Finish: exact guest ELF verified; `/dev/edu` appeared; IAT attached IRQ10; bounded slog2 ready event. Writing10 returned Connection timed out (rc1); read returned EIO (rc1). No3628800, IRQ completion/ack, or private pulse observed. Process terminated explicitly (143). Cause UNVERIFIED. No qtest/PIRQ writes, routing repair, retry or cap change.

## Bounds and limitations

HOST2GiB, CPU100%, nice15, smp1, TCG256MiB, swap0, reserve64MiB throughout; SDK1024MiB only, native512MiB. Stock-build peak2027380736B, correction-SDK peak991621120B; shutdown monitoring included. Effective caps, memory.events and process memory series retained. Native final peaks and all hashes in receipt.json. All guests stopped/reaped; actual no-QEMU and free-flock check recorded in cleanup.json.

Stock networking/SSH is NOT verified: native uses no NIC, serial transfer, and boot logged sshd memory fault. This is not proof of SSH/SCP usability. No platform repairs. Proprietary stock artifacts and raw executable transfer/readback remain outside Git; only text/hashes committed. No media/publication/spend/CAN/C6 changes. Historical acceptance receipts and product acceptance pins remain unchanged; this is not full EDU acceptance.
