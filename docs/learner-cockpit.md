# Your local EDU notebook

A host-operable companion to the [canonical learner route](learner-route.md),
not a reference checker or a simulated terminal. Python standard library only.
No daemon, new port, account or browser-to-shell execution.

## Start a new own session

From your checkout, choose an external, previously nonexistent directory:

~~~sh
export EDU_WORK="$HOME/edu-own-session"
python3 scripts/learner_session.py init --work "$EDU_WORK"
~~~

Open the printed cockpit.html file directly in your local browser. Both starters
are copied to your own step3/main.c and step6/main.c; no solution is copied.
Write your prediction, save a local browser draft, download the notes JSON and
use the displayed fixed notes import command. Notes are session-bound; a draft
alone is not in the evidence pack. CLI import is the durable notebook authority.
Browser storage is convenience only and may vary with file URL/browser settings.

Edit your main.c in your editor. Follow canonical setup and the notebook's exact
source-bound build/run commands, under the same shared native lock. Replace the
notes file placeholder with your actual download. Building requires a saved
prediction, not a supplied answer. Read the raw log and individual checks; record
your diagnosis; edit, rebuild, run again and explain. Refresh the notebook after
CLI actions. Blank diagnosis/explanation are allowed while you are still working;
no overall completion badge is fabricated from notes.

- Step3 wrong write12345679 must fail the existing fixed oracle even if app exit0.
  Correct write12345678 must observe edcba987; printing PASS does not suffice.
- Your own /dev/edu must return3628800 after normal write10. IRQ completion1,
  input10/result3628800/ack00000000 are separate required checks, not node existence.
- HOST identifies setup/build/blocked commands. nativefresh identifies an actual
  driver invocation in this own session with a matching build and recomputed
  oracle. It is local provenance, not tamper-proof independent attestation.
- Historical/recorded references remain comparison material and cannot be imported
  as learner observations. This tool has no receipt import or saved-log run mode.

Every command attempt has an append-only numbered directory, source snapshot and
command output. Successful builds retain their bundle before later builds replace
the active one. Intended failures, setup blocks and interrupted attempts remain.
The existing learner_lab.py CLI, native mechanisms and stage oracles are unchanged.
A supplemental [ability-only lesson](ability-lesson.md) now has permission prediction/diagnosis/explanation notes in the notebook/export. It is not pathname policy, and notes do not create a native acceptance badge. Actual native permission transcripts remain separately bound evidence.

## Legal single-host setup plan

Run on your already licensed Linux x86_64 host. Supply your own paths:

~~~sh
python3 scripts/learner_setup.py --sdp-env "$EDU_SDP_ENV" --bsp "$EDU_BSP" --qemu "$EDU_QEMU" --work "$EDU_WORK"
~~~

The initial plan is read-only and BLOCKED until SDK probing is explicitly enabled.
After trusting your SDK environment script, repeat with --probe-sdk. It invokes
the existing learner_clean_preflight.py, validates host utilities/user-scope access,
and prints exact exports and learner_bootstrap.sh commands. It does not invoke
QEMU, build, install, activate or prompt for a licence. Choose the work path before
session initialization; existing work is deliberately refused by the setup plan.

EDU_BSP is an inventory/compatibility checkpoint, not a mkqnximage BSP selector.
The chosen compatible BSP must already be installed into your licensed SDK's
mkqnximage environment. An arbitrary BSP directory existing does not prove that.
The original stock bootstrap remains the build authority and stops on errors.
Do not copy an owner's image, run commands from a BLOCKED plan, or infer a fresh
SDK install / second-SDK portability PASS. Existing canonical narrow versions and
CPU/memory/lease stop gates remain in force. Preseed is not learner completion.

## Local own-pack export

~~~sh
python3 scripts/learner_session.py export --work "$EDU_WORK" --out "$HOME/new-private-edu-pack"
~~~

Choose a new external directory outside the session. Export copies notes, current
own sources, all failed/successful attempt snapshots and logs, archived successful
builds (source/binary/image/startup/manifest), and hash-deduplicated matching disks
for native observations. pack.json inventories SHA256 for every copied file. All
native receipts are rechecked against their own archived build, source and disk;
a changed/missing asset fails export, leaving INCOMPLETE.txt, not a fake PASS.
Keep original disks available until export. A HOST-only pack is valid as an
unfinished notebook, never native acceptance. SDK libraries/images/binaries stay
outside git. This is a local copy, not permission to redistribute licensed assets;
review licences/privacy before any sharing. There is no upload action.

## Verification and remaining gates

Host tests use explicitly artificial fixtures to test orchestration and existing
oracles, not to claim new QNX evidence. Optional browser QA uses existing Playwright
and Chromium, no installation, server or media capture:

~~~sh
node tests/browser_learner_session.cjs /new/external/qa-directory
~~~

Set EDU_QA_CHROMIUM to your existing browser executable if needed. Desktop/mobile
viewport QA is not a human learner or physical mobile-device validation. The Nov8 own-wrapper native observations are archived in
[wrapper receipts](acceptance/wrapper-20261108/NOTES.md); historical observations
do not validate your new source. Single-host readiness is a separate existing-host
capability gate; a split-host PASS cannot satisfy it. No least-privilege, safety, timing, lifecycle, full-platform
health, independent human acceptance or broad portability claim follows.
