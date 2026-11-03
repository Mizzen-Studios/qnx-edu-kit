# Feature gates — kickoff 2026-11-03

Owner plan: plan_v3, superseding KevScope. CANopy: Automotive & Mobility. edu-kit: Low-level. New code authored during this kickoff; do not backdate commits or represent the owner-provided 2 November work-start date as local implementation evidence.

## Completed foundation, not target acceptance

- Two PRIVATE Apache-2.0 repositories created in Mizzen-Studios.
- Host safety/reference simulation and artifact checks in canopy-qnx.
- Six-step codelab outline and starter/solution acceptance specifications here. They are not compilable driver solutions.
- Host-only CI; target checks remain nonzero/BLOCKED.
- Pinned source investigation: [platform report](platform-gates-20261103.md).

## Owner dependencies

- Updated owner decision (3 Nov21:19UTC): use the existing ARM64 Ubuntu24.04 VM with QEMU x86_64 TCG software emulation, no KVM requirement. qemu-system-x86 and qemu-user-static8.2.2 are installed; Linux guest/user feasibility testing is in progress. QNX/SDP host-tool compatibility still needs the SDK.
- Licensed SDK/QSTI details; no account creation or SDK files in Git.
- Progress stays in the current session until the owner sorts Discord. No further channel-creation retries are required; no channel/posts were created during kickoff.
- Review applicable file/binary licences before upstream template reuse; do not assume repository metadata overrides proprietary notices.

## CANopy acceptance backlog

C1 boot/doctor; C2 SJA1000 board with 3 byte-exact RX/TX runs; C3 isolated /can supervision with main stack/SSH preserved in 3 runs; C4 external canstats and restart trace; C5 QPP CAN/VSS connector and golden tests; C6 target safestop + independent actuator; C7 learned pilot and measured held-out accuracy; C8 eth0 agent20Hz during CAN outage; C9 source-tagged dashboard and real shell; C10 deterministic director/record/replay; C11 floods/FI/budgets and clean-clone live evidence; C12 criteria/API evidence README; C13 local rendered video. All target acceptance is pending. Host models and simulated replay cannot pass live criteria.

## edu-kit acceptance backlog

E1 real per-step PCI/BAR/poll/IAT/resmgr code, with 10 factorial = 3628800 live; E2 claat-rendered tutorial,8diagrams and two fresh-agent clean runs; E3 reviewed secpol/restart/reprobe and source-derived host register model; E4 local video <=2:45; E5 Pages-ready static site and non-Linux route tested or labelled untested. Verify every register live before tutorial documentation. No publishing authorized.

## Dated decision gates (UTC/UK winter)

| Date | Evidence required | Fallback |
|---|---|---|
| 5 Nov | supplied x86_64 mods-can loads and board build possible | libcan driver, retain vehicle layers |
| 16 Nov | SJA1000 RX/TX byte-exact | QNX can-vcan + on-target sim, explicitly disclosed |
| 20 Nov | SLM usable | HAM, then own supervisor |
| 25 Nov | QPP builds | /dev/vss resource manager |
| 4 Dec | secpol works | code-level ability drop documented |
| 7 Dec | rival recheck; dashboard cut decision | cut C/E scope if required |
| 8 Dec | tutorial verified twice clean | owner decision on attaching tutorial to CANopy |
| 12 Dec | freeze | cut stretch first |
| 14 Dec | ready for owner-approved submission | never auto-submit |
| 15 Dec19:00 | owner-provided deadline | official page recheck required; access currently403 |

Stretch begins only after a recorded core hero run. No upstream PR, public repo, Pages publication, upload, external contact, submission or paid resource without required owner approval. No QNX benchmark/comparison or certification claim. Every simulated figure must be marked simulation, never observed QNX.

Demo of fail-safe patterns; not an ISO 26262 / IEC 61508 claim.
