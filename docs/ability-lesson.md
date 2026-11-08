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
