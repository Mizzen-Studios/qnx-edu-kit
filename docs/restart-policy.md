# Restart-safe re-probe contract

Design specification, NOT a QNX implementation or measured recovery result.
Host model: host/edu_model.py:Reprobe; tests: tests/test_model.py:RestartDesign.

## Invariants

- Publish the endpoint only after all setup succeeds; readiness is not process existence.
- Stop accepting requests before teardown. Resolve or explicitly fail existing clients.
- Process death does not reset device state. Inspect busy and owned IRQ status on re-probe.
- Busy work requires a bounded drain or explicit failure. Do not guess that reset is supported.
- Release endpoint, IST, abilities bookkeeping, BAR mapping and PCI attachment in reverse acquisition order.
- A replacement must acquire fresh handles and mappings; no pointer/handle survives process death.
- Drain only owned stale interrupt causes before readiness. Do not acknowledge unrelated shared IRQs.
- Preserve generation/counters in an external observer if survival is needed; the driver cannot certify its own crash.

## Host design tests

Every acquisition position is fault-injected and reverse unwind is asserted.
Stale status is cleared on re-probe; busy re-probe fails closed, duplicate attach
is rejected, stop is idempotent. These model tests are deterministic and do not
exercise QNX, actual masking, kernel cleanup, client wakeup or PCI server ownership.

## Target acceptance still required

Capture PID, build hash and device identity before and after controlled process
replacement. Test idle, in-flight factorial, IRQ pending, client blocked and each
partial setup failure. Assert bounded client errors, no stale success, no leaked
PCI ownership and no IRQ storm. Use only a verified driver PID, never a broad
process-name kill. Supervisor choice/commands and retry limits remain target
review work; no executable SLM/HAM recipe is fabricated here.
