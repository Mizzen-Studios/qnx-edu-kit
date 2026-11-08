# Ability-only permission experiment

Not pathname security policy. No /dev path attach/connect identities are enforced
by this lesson. Path-policy support remains BLOCKED, separately from installed tools.

Predict whether the same executable can request this thread's IO_LEVEL_1 after
its process ability configuration changes. Build once in your existing licensed
SDP environment, to a new external directory:

    qcc -Vgcc_ntox86_64 -std=gnu11 -Wall -Wextra -o "$EDU_ABILITY" native/ability_lesson.c

Install that ELF into your own working image buildfile and rebuild normally.
On separate fresh QNX processes (never try to undo a locked deny), run:

    /proc/boot/ability_lesson deny
    /proc/boot/ability_lesson allow

The deny process denies/locks all unlocked abilities in both root/nonroot domains.
The allow process enables/locks only IO subrange0..0, denying/locking all other
unlisted unlocked abilities. QNX8 documents ability IO parameter0 as sufficient
for thread IO_LEVEL_1; parameter1/IO_LEVEL_2 and inheritance are not requested.
The thread relinquishes IO immediately and performs no actual port access.
This is the least supported IO level for this operation, not a proof that every
privilege in the platform is minimal: inherited locked capabilities and image
startup configuration are outside this narrow lesson. Default root is NOT the
least-privilege allow configuration.

Preserve both transcripts, errno, exit status, identical ELF SHA256, original
source revision/hash, build/image/disk/run lineage. Expected deny rc-1 errno1
(EPERM), allow rc0 errno0. A setup failure is BLOCKED, never an expected denial.
Keep failed attempts. Add prediction/diagnosis/explanation to your notebook before
export; permission observations are supplemental, not step3 or /dev/edu completion.
No native safety, adversarial isolation, path policy or availability claim.

API reference: QNX8 procmgr_ability() and ThreadCtl() library reference, specifically
IO subrange0 for IO_LEVEL_1; library libc. SDK headers/implementation are not shipped.

Implementation status: original source and notebook notes are available. The earlier
prerequisite demonstrated deny versus default root only. The new narrowed allow
configuration now has its own [fresh native receipt](acceptance/ability-20261108/receipt.json): deny rc-1/EPERM, allow IO0..0 rc0, both exit0, same ELF separate processes. Do not substitute the older default-root proof.

### Shared-run provenance (offline inspection)

The archived run.json is byte-identical shared CAN incident-run metadata, not an
ability acceptance receipt. Its success field means CAN restart/traffic only.
native-transcript.txt is the original mixed containment/ability/CAN slog2 capture,
not a full boot log; no transcript has been reconstructed. provenance.json types
and hashes both files. The original receipt records the same ELF digest and
separate-process results; shared run metadata does not independently bind that ELF.

Run python3 scripts/ability_provenance.py to recompute the ability observations.
Both capability-ledger and review-packet consumers fail closed on wrong evidence
type, altered shared bytes, run/image/disk mismatch or wrong-typed results. They
never use shared CAN success to grant ability PASS. This is offline validation,
not new execution or a new acceptance award.

The literal shared CAN run.json substituted as receipt.json is a negative fixture:
CLI validation, capability catalog and review appendix all reject it. Notebook
export does not import these ability receipts as native stage attempts: permission
notes and optional supplemental files are unqualified supporting material, never
step3/step6 PASS. Their inclusion cannot grant current-source validation.
