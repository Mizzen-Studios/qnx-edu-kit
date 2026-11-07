# Clean-image learner /dev/edu investigation

Acceptance is **not yet passed**. This is edited step6 starter code, not the reference checker. The actual normal write timed out, cat returned EIO, and the stage correctly failed. All failures are preserved.

- `initial-failure`: persistent IAT lifetime across resource-manager dispatch.
- `irq-routing-failure`: transaction-scoped IAT with NO_UNMASK and InterruptWait UNMASK; device computes3628800, pending1, no observed completion.
- `slot5-failure`: explicit EDU PCI slot5 alone did not resolve it.
- `route-inspection-failure`: read-only PIIX inspection found EDU1234:11e8, PCI IRQ10, PIRQ0 already routed10.
- `route-noop-failure`: wrote the identical PIIX route value; no change/no pass. No EDU MMIO, result or IRQ injection.
- `controller-inspection-failure`: PIC masksff/ff, ELCR00/0c, IOAPIC IRQ10 low entry40 (edge-triggered). Read-only controller inspection except IOAPIC register selector. Not native acceptance.

`diagnostic-run-driver.py` preserves the temporary diagnostic harness. Production learner runner remains unchanged; no qtest dependency or routing mutation was adopted. The source-bound native logs preserve the unattributed startup Memory fault after Starting sshd; no healthy-SSH/platform claim.

Next narrowly scoped source check removes NO_UNMASK so attachment unmasks before starting the device operation. No timeout/oracle change, reference priming or polling fallback. Result pending.
