# Security policy specification — NOT validated secpol

No policy syntax or fake configuration is provided. The actual compiler, policy
installation and effective grants must be reviewed in the authorized QSTI image.
IO and INTERRUPT are planned ability areas, not an exhaustive grant set.

| Phase | Intended authority | Required target evidence |
|---|---|---|
| Discover/attach | PCI server access for only the selected edu instance | deny unrelated instance; record attach result |
| Map/setup | permitted device mapping and interrupt attachment | deny without each required grant; capture actual error |
| Serve | only rights needed for requests, IRQ wait/ack and endpoint | demonstrate requests after setup-only authority is reduced |
| Teardown | owned IRQ/map/PCI release, no unrelated device access | no leaked attachment; repeated lifecycle transcript |

Endpoint ownership and permissions must constrain callers; validate input before
hardware access. Do not grant global unrestricted abilities, use /dev/mem as a
QNX workaround, or claim a policy is least privilege merely because it compiles.

Acceptance matrix: correct policy succeeds; missing IO fails at the expected
operation; missing interrupt grant fails attachment; unauthorized client fails
endpoint access; unrelated PCI device is inaccessible. Each test needs the exact
binary hash, policy revision, effective identity, operation, error and transcript.
Host tests cannot establish these outcomes. No validated security claim exists.
