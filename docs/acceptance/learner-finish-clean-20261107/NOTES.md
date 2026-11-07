# Clean-image learner /dev/edu investigation

Final scoped acceptance is **PASS**; see [fresh source-bound receipt](unmasked/native.json) and [raw serial](unmasked/native.txt). Earlier failures below are retained. This is edited step6 starter code, not the reference checker. The actual normal write timed out, cat returned EIO, and the stage correctly failed. All failures are preserved.

- `initial-failure`: persistent IAT lifetime across resource-manager dispatch.
- `irq-routing-failure`: transaction-scoped IAT with NO_UNMASK and InterruptWait UNMASK; device computes3628800, pending1, no observed completion.
- `slot5-failure`: explicit EDU PCI slot5 alone did not resolve it.
- `route-inspection-failure`: read-only PIIX inspection found EDU1234:11e8, PCI IRQ10, PIRQ0 already routed10.
- `route-noop-failure`: wrote the identical PIIX route value; no change/no pass. No EDU MMIO, result or IRQ injection.
- `controller-inspection-failure`: PIC masksff/ff, ELCR00/0c, IOAPIC IRQ10 low entry40 (edge-triggered). Read-only controller inspection except IOAPIC register selector. Not native acceptance.

`diagnostic-run-driver.py` preserves the temporary diagnostic harness. Production learner runner remains unchanged; no qtest dependency or routing mutation was adopted. The source-bound native logs preserve the unattributed startup Memory fault after Starting sshd; no healthy-SSH/platform claim.

Final edited source removes NO_UNMASK: attachment unmasks before starting the device operation, and the transaction-scoped IST detaches before message dispatch resumes. On fixed PCI slot5 this fresh image passes actual write10/read3628800, completion IRQ and ack0. Both client exits0, target wrapper0, independent stage0; all provenance/cap/reaping checks pass. No timeout/oracle change, reference priming, qtest adapter or polling fallback. This is one edited starter finish, not independent human/all-six-stage qualification. The source change was isolated relative to the prior fixed-slot failure; broader causal claims are not established.

Root-level source/manifest/build artifacts describe the earlier NO_UNMASK build, not the successful final source. The authoritative final build and native evidence are exclusively under `unmasked/`. Local upstream claat export validated6 core steps,12 source snapshots and8 SVGs; no publication/browser delivery is implied.
