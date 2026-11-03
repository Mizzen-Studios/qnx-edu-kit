author: Mizzen Studios
summary: Unverified outline for a first PCI driver for QNX 8.0
id: qnx-edu-kit
categories: QNX, PCI
environments: Web
status: Draft
feedback link: https://github.com/Mizzen-Studios/qnx-edu-kit/issues

# A first PCI driver for QNX® 8.0 — blocked draft

> Last live verified: NEVER. SDP build: PENDING. QSTI: PENDING. QEMU: PENDING.
> This is an outline, not an executable tutorial. Estimated durations are planning targets, not measured learner times. Do not publish until all live verification gates pass.

## 1. Setup
Duration: 8

Intended build: a QEMU edu PCI teaching driver. Learn PCI discovery, mapped I/O, polling, an interrupt service thread and a resource manager. Intended finish line: writing 10 and reading 3628800 via /dev/edu on QNX; NOT achieved. Need an authorized local SDP 8.0, pinned QSTI/QEMU image and a verified target. No hardware required in the proposed path.

Record SDP build, QSTI and QEMU versions, image provenance, target architecture and permissions; validate a clean boot.

Host (repository root):

```sh
make check-step1
```

<details><summary>Current expected output</summary>

BLOCKED: step 1 live QNX check not implemented or verified. Nonzero exit; no target command is available.

</details>

Starter: [task](../steps/step1/starter/README.md). Solution: [acceptance specification only](../steps/step1/solution/README.md).

## 2. PCI server attach
Duration: 8

Use locally reviewed QNX 8.0 PCI server declarations to enumerate and attach edu, inspect BAR metadata and detach cleanly.

Host (repository root):

```sh
make check-step2
```

<details><summary>Current expected output</summary>

BLOCKED: step 2 live QNX check not implemented or verified. Nonzero exit; no target command is available.

</details>

Starter: [task](../steps/step2/starter/README.md). Solution: [acceptance specification only](../steps/step2/solution/README.md).

## 3. ID and liveness
Duration: 4

After every relevant checklist row has live evidence, map the validated BAR range and perform bounded ID/liveness checks.

Host (repository root):

```sh
make check-step3
```

<details><summary>Current expected output</summary>

BLOCKED: step 3 live QNX check not implemented or verified. Nonzero exit; no target command is available.

</details>

Starter: [task](../steps/step3/starter/README.md). Solution: [acceptance specification only](../steps/step3/solution/README.md).

## 4. Factorial polling
Duration: 4

Implement a bounded wait, reject unsupported inputs, and observe the factorial finish line on the actual target.

Host (repository root):

```sh
make check-step4
```

<details><summary>Current expected output</summary>

BLOCKED: step 4 live QNX check not implemented or verified. Nonzero exit; no target command is available.

</details>

Starter: [task](../steps/step4/starter/README.md). Solution: [acceptance specification only](../steps/step4/solution/README.md).

## 5. Interrupt service thread
Duration: 10

Review current InterruptAttachThread and InterruptWait declarations locally; verify ability failures, INTx status, acknowledgement, unmasking and clean detach.

Host (repository root):

```sh
make check-step5
```

<details><summary>Current expected output</summary>

BLOCKED: step 5 live QNX check not implemented or verified. Nonzero exit; no target command is available.

</details>

Starter: [task](../steps/step5/starter/README.md). Solution: [acceptance specification only](../steps/step5/solution/README.md).

## 6. Resource manager
Duration: 10

Review resource-manager handlers locally; implement bounded input, concurrency, partial reads and error handling; observe the finish line and safe re-probe.

Host (repository root):

```sh
make check-step6
```

<details><summary>Current expected output</summary>

BLOCKED: step 6 live QNX check not implemented or verified. Nonzero exit; no target command is available.

</details>

Starter: [task](../steps/step6/starter/README.md). Solution: [acceptance specification only](../steps/step6/solution/README.md).

## Congratulations — future acceptance only
Duration: 0

You are not finished until a real target transcript proves every core step and two fresh agents reproduce the codelab from clean clones. No congratulations or 44-minute completion claim is earned by host CI.

## Extra credit — not implemented
Duration: 0

DMA (estimated 10 minutes), restart/re-probe (4), tracing (5) are blocked. Validate the pinned QEMU DMA property, register semantics, physical-address handling and cache ownership before writing a DMA tutorial. Do not supply guessed commands or APIs.

## Navigation and support
Duration: 0

Mini-map: setup → PCI → ID/liveness → polling → IST → resmgr.

The [verification checklist](../docs/verification-checklist.md) holds candidate register work separately; no offsets or values are taught here. Eight final diagrams (environment, PCI ownership, BAR lifetime, polling, IST, abilities, resmgr, DMA) are pending verified flows and claat export. claat export/render has not been tested.

See [troubleshooting and glossary](../docs/learning-notes.md).
