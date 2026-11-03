# Learning notes — outline, not target instructions

## Concept map (not API equivalence)

| Linux familiarity | QNX learning topic to verify locally |
|---|---|
| PCI probe/remove | QNX 8.0 PCI server ownership and detach |
| mapped BAR | validated device memory mapping and ability scope |
| interrupt handler | interrupt service thread and lifecycle |
| device file operations | resource-manager messages/handlers |
| capabilities/policy | QNX abilities and security policy |

Do not translate Linux signatures or assume compatibility. The discontinued legacy PCI path is not a target for this kit. Consult the actual installed QNX 8.0 documentation before choosing any function declaration.

## Planned asides, all awaiting local documentation and live review

- IAT/InterruptWait is the planned standalone-driver path; IAE in io-sock is contextual, not an interchangeable sample here.
- Ability-related EPERM: verify the process's IO/interrupt abilities and active policy rather than recommending broad root access. No /dev/mem workaround.
- Verify mutex priority-inheritance defaults in the installed SDK; do not assume semaphores inherit priority.
- INTx and MSI have distinct acknowledgement/lifecycle requirements.

## Symptom → investigation → bounded next action

| Symptom | Candidate cause, not diagnosis | Next action |
|---|---|---|
| check-step exits 2 | live implementation absent | expected now; read verification ledger |
| verify fails after green host tests | full acceptance deliberately blocked | do not bypass or rename as PASS |
| guard rejects file | binary/image/archive/SDK marker or symlink | move local artifact outside checkout; review provenance |
| future EPERM | missing ability or policy | capture actual target error and inspect local docs/policy |
| future polling timeout | mapping/state/ownership mismatch | stop; preserve transcript, do not extend wait indefinitely |
| future stuck IRQ | ack/status/lifecycle mismatch | stop driver safely; inspect live evidence before retry |

## Glossary

- SDP: the QNX development platform; separately licensed local tooling, never vendored.
- QSTI: QNX Software Target Image; exact distribution/version and provenance still pending.
- QSC: QNX Software Center; tooling/distribution access is not assumed configured.
- myQNX: account portal; no account creation is performed by this kit.
- BAR: PCI base-address register describing a device resource.
- IST: interrupt service thread.
- claat: codelab authoring/export tool; metadata outline exists, export untested.
