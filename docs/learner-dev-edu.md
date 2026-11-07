# Learner-owned /dev/edu finish

This stage is separate from `check-reference-step6` and `native/edu_accept.c`.
It builds an edited step6 starter and assesses actual normal device I/O on a fresh
boot. Reference receipts and step3 manifests cannot satisfy this stage.
Native acceptance is pending until the separately recorded clean-image run.

1. Initialize an external directory with `python3 scripts/learner_lab.py init --stage step6 --work /external/finish`.
2. Edit `main.c` to complete resource-manager registration: dispatch setup, the
   existing bounded read/write handlers, per-open result snapshots and `/dev/edu`
   attachment. The starter includes IRQ/factorial scaffolding; this finish does
   not demonstrate that a human independently implemented every earlier step.
3. Use the licensed clean platform from [clean setup](clean-step3-setup.md).
   Its application-only snippets install the fresh `learner_bin` and
   `learner-start.sh`, and invoke the wrapper after PCI readiness. Build with
   `learner_lab.py build --stage step6` and the same explicit source/out/SDP-env/
   buildfile/BSP-cwd arguments as [step3](learner-lab.md). No reference binary.
4. Stop/reap the SDK guest, then hold the exclusive native lease. Run
   `learner_lab.py run --stage step6` with the actual edited source, fresh bundle,
   matching clean disk and an external receipt prefix. Caps remain100%CPU/1GiB/
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
