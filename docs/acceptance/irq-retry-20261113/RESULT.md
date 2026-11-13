# One stock IRQ finish retry — PASS, Nov13 11:03 scope

**PASS_ONE_STOCK_FINISH_TRANSACTION. All SDK/native guests reaped; no QEMU; actual lease FREE. Stopped for parent independent review.**

The pre-attempt [justification](../../irq-retry-plan-20261113.md) used HostShare stock evidence API10/config11 and installed QNX8 API declarations. Minimal explicit --pci-line reads existing config line/pin, never rewrites routing. Current EDU keeps real InterruptWait(0), own pending/not-busy checks, acknowledge then one explicit unmask. Unlike Nov8 UNMASK-wait history, no redundant second unmask was introduced. No virtio read-clear ISR workaround is transplanted into EDU.

One serial existing-SDK compile/link (rc0), then SDK stop/reap before ONE native512MiB attempt. No image generation and no repeat of already proved wrong/correct stock MMIO gates. Same IFS68bbe1b49a9b723c09d152773ee323ec6ab576eb29de933bfe3f08fdae21c753 and disk0aee00c281f8eeb5b02c66555ed9517e317bb1503002a19dbf2b0155de336532, verified before/after. External paths/hashes in receipt.json. No proprietary artifacts or executable bytes committed.

Actual native API10/config11/pin1, attached IRQ11. Exact transferred ELF bytes matched host e599c54a0eb2b64dff5114f9ab499867a75ba4336ee1d09cba8a628d42d0a3d4. One write10 returned0; read3628800 returned0. IRQcompletion1/input10/result3628800/ack00000000 and private pulse sent1/received1 observed. Three bounded slog2 records: ready, IRQ/ack, pulse. Service terminated143 deliberately after transaction; that is cleanup, not a claimed normal daemon exit0.

SDK<=1GiB; target512MiB; HOST2GiB CPU100 nice15 smp1 TCG256MiB swap0 reserve64MiB. SDK measured peak965160960B through shutdown, native monitored peak517066752B, no resource breach. Effective caps, events, process RSS series and all source/object/ELF/IFS/disk bindings are in this separate receipt. Earlier OOM/IRQ-timeout/native receipts untouched. Selection fix is proved only for this observed stock x86 configuration, not a universal PCI API diagnosis.

Networking/SSH remains unverified: nic none with serial transfer, boot sshd memoryfault preserved, no platform repair. Optional trace NOT_RUN. This proves one synchronous factorial/IRQ/ack/private-pulse flow, not performance/concurrency/safety/full-platform health or independent human learning. No new broader acceptance pin, recording, public/media/PR, CAN/C6, install/login or spend. Stop review; no more guest attempts under this wave.
