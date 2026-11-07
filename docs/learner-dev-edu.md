# Learner-owned /dev/edu finish

This stage is separate from `check-reference-step6` and `native/edu_accept.c`.
It builds an edited step6 starter and assesses actual normal device I/O on a fresh
boot. Reference receipts and step3 manifests cannot satisfy this stage.
The [clean-image learner run](acceptance/learner-finish-clean-20261107/NOTES.md) passed real write/read10→3628800 and IRQ completion/ack, with source/binary/image/disk provenance. This is not independent human validation.

1. Initialize an external directory with `python3 scripts/learner_lab.py init --stage step6 --work /external/finish`.
2. Edit `main.c` to complete resource-manager registration: dispatch setup, the
   existing bounded read/write handlers, per-open result snapshots and `/dev/edu`
   attachment. Keep IAT ownership transaction-scoped: attach normally (unmask before triggering the device),
   wait with the UNMASK flag, acknowledge and detach before returning to message
   dispatch. The initial clean run exposed the scaffold's persistent-IST
   lifetime across dispatch (normal write timed out; exact causality not isolated); its failure receipt is preserved. QNX
   [documents that an IST may block only in InterruptWait](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.prog/topic/inthandler_Thread_or_Event.html).
   The starter includes IRQ/factorial scaffolding; this finish does
   not demonstrate that a human independently implemented every earlier step.
3. Use the licensed clean platform from [clean setup](clean-step3-setup.md).
   Its application-only snippets install the fresh `learner_bin` and
   `learner-start.sh`, and invoke the wrapper after PCI readiness. Build with
   `learner_lab.py build --stage step6` and the same explicit source/out/SDP-env/
   buildfile/BSP-cwd arguments as [step3](learner-lab.md). No reference binary.
4. Stop/reap the SDK guest, then hold the exclusive native lease. Run
   `learner_lab.py run --stage step6` with the actual edited source, fresh bundle,
   matching clean disk and an external receipt prefix. The runner pins EDU to PCI slot5 (observed PIRQ0→IRQ10); no host routing adapter is used. Caps remain100%CPU/1GiB/
   nice15, target1vCPU/512MiB.
5. The generated wrapper starts the edited daemon, waits for `/dev/edu`, writes
   `10` using normal shell redirection, reads with `cat`, and captures both exit
   codes and the actual returned text. Acceptance requires3628800, a matching
   IRQ completion/ack observation, QNX identification, source/binary binding,
   bounded completion and stopped/reaped QEMU. Merely printing PASS fails.

The wrapper terminates its daemon after this one normal-I/O transaction; no
lifecycle, least-privilege, timing, robustness or safety acceptance follows.
Hashes are cooperative build provenance, not malicious-learner attestation.
No C6 work, publication or deployment is performed.

The clean target still logs an unattributed Memory fault after Starting sshd. No healthy-SSH/full-platform claim. The earlier NO_UNMASK and routing hypotheses failed and remain in the receipt history.

Startup diagnosis attributes the observed failure to **sshd** in a separately traced image; internal cause remains UNVERIFIED. [Separate baseline/diagnostic bindings](acceptance/startup-diagnosis-20261107/NOTES.md). No SSH/platform health claim.

## Fresh-checkout correction

When adapting the starter, remove its explicit InterruptUnmask after InterruptWait
when using _NTO_INTR_WAIT_FLAGS_UNMASK: do not unmask a second time. Detach the
transaction IAT before stdio or dispatch (and on every error exit); printing while
still an IST can fail the transaction. Attach in the write's factorial transaction,
not at daemon startup. This is an implementation requirement, not a safety claim.
