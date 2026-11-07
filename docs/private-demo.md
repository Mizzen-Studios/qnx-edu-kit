# Private demo draft — EDU learner tutorial

**Draft only. No recording, upload, publication or submission authorized.** Target edit length **2:40**, hard ceiling 2:55 including titles. Timing is editorial allocation, never measured QNX performance. Narration ~225 words; rehearse privately before any separately authorized capture.

Persistent label: “Recorded QEMU evidence · automated learner reproduction · not independent human validation”. Show repository text and sanitized receipts only; no credentials, account UI, SDK code, headers, licence screens, binary/core contents or external access URLs. Do not launch QEMU for this shot list. Cuts must be labelled; never suggest continuous execution or compress a build into a latency claim.

| Edit time | Shot / exact evidence | Narration |
|---|---|---|
| 0:00–0:20 | README and REVIEW; fresh-checkout provenance.json, initial9075199 → documentation95afcff; receipt archive85fad4f | “This private EDU lab traces a learner-owned C edit to a native QNX observation in QEMU. These are saved results from an automated fresh-checkout reproduction, not an independent human study.” |
| 0:20–0:45 | docs/clean-step3-setup.md; fresh-checkout preflight.json and platform-hashes.txt | “The run reused an existing licensed SDK and generated a new stock generic platform outside the repository. The build used guest disk swap. SDK and target guests ran serially under the stated CPU and memory caps; no proprietary artifacts are distributed.” |
| 0:45–1:15 | fresh-checkout step3/wrong.c, wrong-native.log and wrong-native.json | “Here the wrong edit compiles and the application reports success. The independent stage check still rejects the observed readback. Printing PASS is not completion.” |
| 1:15–1:40 | step3/correct.c, correct-native.log and correct-native.json; show source/ELF/IFS/disk hashes without implying attestation | “The corrected edit passes on a fresh boot. The receipt binds source, binary, image and disk bytes. These hashes are cooperative provenance, not protection against a malicious learner.” |
| 1:40–2:15 | finish-native.json/log beside finish-corrected-native.json/log; docs/learner-dev-edu.md | “The first device finish failed and remains preserved. After clarifying interrupt unmask and detach ordering, a rebuilt edited starter accepted a normal shell write of ten and returned three million six hundred twenty-eight thousand eight hundred, with an interrupt completion and acknowledgement. This is separate from the reference checker.” |
| 2:15–2:40 | startup-diagnosis NOTES, baseline/traced receipt hashes; REVIEW limits | “A startup fault remains: an unchanged image reproduces it, while a separately traced image identifies sshd. Its internal cause is unverified. This is not SSH or whole-platform health, production-driver, safety, timing or portability acceptance. Independent owner re-review is next.” |

## Shot evidence index

All fresh evidence paths above resolve under docs/acceptance/fresh-checkout-20261107/. Provenance records initial clone9075199ab5f14924786adb7993ec596a8552ae73, host correctioncce9ef68ef6fee2fe27f99f72c573790a54a8ecc, finish instruction correction95afcff084a346b132e143d4a3bbd15eb81954a8. Corrected finish source64647c88597eff57f0723ffb2e479f90501f717065edd5a008827866fd8b76fe; ELF2e9735a6987181630018ce2d09e64ab9d6f4920b5be36ed842b082f85f5b2042; IFS3677f476f545ec40d690e28d0f3f98b1cfec7e4929f3779c251d40de2995ec0f. Full disk/driver bindings in finish-corrected-native.json. Diagnosis is separately bound under docs/acceptance/startup-diagnosis-20261107/; baseline and traced images must never be presented as identical.

C6 remains STOPPED; SocketCAN UNVERIFIED. No new runtime result is created by this draft.
