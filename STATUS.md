# Status — 7 November 2026

**PASS: fresh native functional acceptance and clean-checkout end-to-end verify.sh.**

- Direct parent-owned acceptance returned0 with all six target markers, IRQ raise/wait/ack,64-byte byte-exact RAM→EDU→RAM DMA (polled; not DMA-IRQ proof), and actual shell echo10/cat3628800 through the IAT IRQ-driven resource manager.
- Receipt validates CPU100000/100000, memory1073741824bytes, nice15. Guest1vCPU/512MiB; no other native guest ran concurrently.
- Clean detached checkout `387ba38ce696c92bb3d8332ea7f01d5a0630cbfc` ran full `verify.sh`, exit0. Host suite55cases:53pass+2explicit optional/live integration skips. Fresh native steps1–6 allPASS; no saved transcript accepted as input. Checkout stayed clean.
- Evidence: [direct receipt](docs/acceptance/native-20261107/receipt.json), [serial](docs/acceptance/native-20261107/serial.txt), [clean-checkout receipt](docs/acceptance/native-20261107/clean-checkout-receipt.json), [complete verify output](docs/acceptance/native-20261107/clean-checkout-verify.txt). Source/image hashes bound in each receipt.

All observations are **observed in this QEMU run · app budget, not a QNX benchmark**.

## Recovery and remaining boundaries

The old worker was killed/stalled, the handoff file absent, and no owned QEMU remained. The coordinator took over directly without file-event waiting. No live processes needed killing to free the stale lease. The cap collector fix includes the exec-replaced QEMU root PID; the failed old null-cap receipt is not promoted to success. The original source-bound image worked; an unfinished dedicated-startup rebuild was not required or represented as completed.

Target is custom licensed SDP8 Generic BSP/QNX8, **not established QSTI provenance**. Functional PASS is not a certification, least-privilege/security-policy, physical-device, graceful-stop, comprehensive fault injection or two-fresh-learner acceptance claim. No licence/SDK/header/library/image/binary/QSC/credential material is committed. Guests stopped/reaped after each owned run, shared native lease free. Repos private; nothing published and no spending or outreach.
