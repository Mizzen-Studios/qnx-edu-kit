# Private proof-capture DRY PACK

No recording or audio capture. Separate Olly OK required. No publication/upload authorized.

Frozen evidence: 01060c7c1aff834d6c0b016de7fd9f988f8f7e35
Exact whitespace narration word count: 211; planned 160 seconds (not measured).
C6 FAIL / STOPPED; SocketCAN UNVERIFIED. Historical native and host-only frames remain separate.

## L01 — 0–20 seconds · host-only provenance
Claim: Automated learner-owned C reproduction using reused SDK only, not fresh install, second SDK or human validation.
Planned frame: Local sanitized file view: docs/acceptance/fresh-checkout-20261107/provenance.json. Show receipt checks/observed markers and binding fields; cuts labelled recorded evidence, never live telemetry.
Narration: This private EDU lab binds learner-owned C edits to saved QNX observations in QEMU. The reproduction was automated using an existing SDK, not a fresh installation, second SDK or human study.
Frozen files: docs/acceptance/fresh-checkout-20261107/provenance.json SHA256 f09afc939f11365e4fe28f485165acc44d7d204a7df3f7a6d32dbab4e25d6440
REVIEW boundary: automated, not independent human review

## L02 — 20–45 seconds · recorded SDK build boundary
Claim: Recorded new stock platform using guest disk swap under serialized stated caps; existing legal SDK reused.
Planned frame: Local sanitized file view: docs/acceptance/fresh-checkout-20261107/preflight.json, docs/acceptance/fresh-checkout-20261107/platform-hashes.txt, docs/acceptance/fresh-checkout-20261107/sdk-caps.json. Show receipt checks/observed markers and binding fields; cuts labelled recorded evidence, never live telemetry.
Narration: The run reused an existing licensed SDK and generated a new stock generic platform outside the repository. The build used guest disk swap. SDK and target guests ran serially under the stated CPU and memory caps; no proprietary artifacts are distributed.
Frozen files: docs/acceptance/fresh-checkout-20261107/preflight.json SHA256 b06c41832702128049a27b218a7d21f63530add2766ccf5c9f556ab5ebcae8ed, docs/acceptance/fresh-checkout-20261107/platform-hashes.txt SHA256 5ca743be667db1586f11b08492721d2ec1e058198dc4ae78898a6a40f0845dc7, docs/acceptance/fresh-checkout-20261107/sdk-caps.json SHA256 6cfb79499436f343f28ca22beb03ea274e8d0cbe1b00976029334bcb1c42ed2c
REVIEW boundary: Stock generic build

## L03 — 45–75 seconds · recorded native QEMU observation
Claim: Wrong step3 edit: applicationPASS/exit0 but independent stageFAIL from actual readback.
Planned frame: Local sanitized file view: docs/acceptance/fresh-checkout-20261107/wrong-native.json, docs/acceptance/fresh-checkout-20261107/wrong-native.log, docs/acceptance/fresh-checkout-20261107/step3/wrong.c. Show receipt checks/observed markers and binding fields; cuts labelled recorded evidence, never live telemetry.
Narration: Here the wrong edit compiles and the application reports success. The independent stage check still rejects the observed readback. Printing PASS is not completion.
Frozen files: docs/acceptance/fresh-checkout-20261107/wrong-native.json SHA256 e6dff846f146d337ca8df51bc6bfc039af76624688ec37ed7423c17747871d4d, docs/acceptance/fresh-checkout-20261107/wrong-native.log SHA256 dc49ad5bba03f57e08167e411266600db3d283aa8dc4a41604ef9b50f0ba472e, docs/acceptance/fresh-checkout-20261107/step3/wrong.c SHA256 c834e1c45aa6a994f1a1aa69888a6d87fa98c786ae28bed620eb799134e903c4
REVIEW boundary: Wrong-edit rejected despite application PASS/exit0

## L04 — 75–100 seconds · recorded native QEMU observation
Claim: Correct step3 edit stagePASS with cooperative source/ELF/IFS/disk hash binding.
Planned frame: Local sanitized file view: docs/acceptance/fresh-checkout-20261107/correct-native.json, docs/acceptance/fresh-checkout-20261107/correct-native.log, docs/acceptance/fresh-checkout-20261107/step3/correct.c. Show receipt checks/observed markers and binding fields; cuts labelled recorded evidence, never live telemetry.
Narration: The corrected edit passes on a fresh boot. The receipt binds source, binary, image and disk bytes. These hashes are cooperative provenance, not protection against a malicious learner.
Frozen files: docs/acceptance/fresh-checkout-20261107/correct-native.json SHA256 4d5dc15560f8449f04e2cfbce8d6061f5c603826d9cdc4d6582fa539c1a1eafd, docs/acceptance/fresh-checkout-20261107/correct-native.log SHA256 fe7c00ad3378612a7eeb4d66578867432555f5d82c9f364dfc65cb97627aa687, docs/acceptance/fresh-checkout-20261107/step3/correct.c SHA256 2f37c2f234b10e78c9920372895b56e1efe7d4742cd099eb1f8a73ba46a8aaeb
REVIEW boundary: corrected BAR edit accepted

## L05 — 100–135 seconds · recorded native QEMU observation
Claim: Initial edited manager failure preserved; corrected own manager shell write10/read3628800 and IRQcompletion/ack0, no reference checker.
Planned frame: Local sanitized file view: docs/acceptance/fresh-checkout-20261107/finish-native.json, docs/acceptance/fresh-checkout-20261107/finish-native.log, docs/acceptance/fresh-checkout-20261107/finish-corrected-native.json, docs/acceptance/fresh-checkout-20261107/finish-corrected-native.log, docs/acceptance/fresh-checkout-20261107/finish-corrected/manifest.json, docs/acceptance/fresh-checkout-20261107/finish-corrected/main.c. Show receipt checks/observed markers and binding fields; cuts labelled recorded evidence, never live telemetry.
Narration: The first device finish failed and remains preserved. After clarifying interrupt unmask and detach ordering, a rebuilt edited starter accepted a normal shell write of ten and returned three million six hundred twenty-eight thousand eight hundred, with an interrupt completion and acknowledgement. This is separate from the reference checker.
Frozen files: docs/acceptance/fresh-checkout-20261107/finish-native.json SHA256 19bf7205f52ef4fac7668f867fd2e31a54d99e542574359b79e54a7e2393bdc5, docs/acceptance/fresh-checkout-20261107/finish-native.log SHA256 e16c828871cd6da91865fb4d01d1568070cfe053f7dbbc69d80386ab8c800a73, docs/acceptance/fresh-checkout-20261107/finish-corrected-native.json SHA256 ef83383c93509cbb6113e4e9ff87d2685d73d2f4c799972a649c050b554ef6c2, docs/acceptance/fresh-checkout-20261107/finish-corrected-native.log SHA256 e7e6b0ecc14281609781a4dc805d5247db9bb5d958b1754fffd6bc5d7517b466, docs/acceptance/fresh-checkout-20261107/finish-corrected/manifest.json SHA256 62af484678314f28cc19787954e8d57c254566f9165cd87dd3775c7a0528279e, docs/acceptance/fresh-checkout-20261107/finish-corrected/main.c SHA256 64647c88597eff57f0723ffb2e479f90501f717065edd5a008827866fd8b76fe
REVIEW boundary: wrong host1/correct host0, initial finish host1/corrected finish host0

## L06 — 135–160 seconds · recorded native QEMU observation
Claim: Unchanged baseline reproduces startup fault; separate traced image attributes sshd, internal cause and platformhealthUNVERIFIED.
Planned frame: Local sanitized file view: docs/acceptance/startup-diagnosis-20261107/baseline.json, docs/acceptance/startup-diagnosis-20261107/baseline.log, docs/acceptance/startup-diagnosis-20261107/traced.json, docs/acceptance/startup-diagnosis-20261107/traced.log. Show receipt checks/observed markers and binding fields; cuts labelled recorded evidence, never live telemetry.
Narration: A startup fault remains. The unchanged image reproduces it; a separately traced image identifies sshd. Internal cause and platform health remain unverified. Council acceptance is conditional and native features are frozen. Recording or audio needs separate Olly approval.
Frozen files: docs/acceptance/startup-diagnosis-20261107/baseline.json SHA256 64c151b9e7bf93f9cb03c0d471d145e95d3eda34bfb7c0850f9279c8a3529108, docs/acceptance/startup-diagnosis-20261107/baseline.log SHA256 b8a49a701c109c41ac4e6b7deeabad885dd45d4d84299afb9ee2609764cadde6, docs/acceptance/startup-diagnosis-20261107/traced.json SHA256 09b26787145787d915bad34b2c705d0567afed5e4f8c1a532c1731de7e6a0894, docs/acceptance/startup-diagnosis-20261107/traced.log SHA256 8250b3fc1c34e70b7d8bc8554c43d3c98fda3a9857f7d8d4c6576f62d7e5235c
REVIEW boundary: Internal root cause and healthy-SSH/platform

