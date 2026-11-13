# One notebook: wrong → correct → finish → own export

This is an **advanced working-stock lab**, not a browser simulator or turnkey fresh install. Start with the [canonical stock prerequisite gate](learner-route.md): existing licensed SDP, exclusive SDK/QEMU lease, controller/shared mount and approved hash-verified IFS/disk handoff. No new IFS, installation/login, routing rewrite or old-receipt import. Current coherent runtime acceptance remains pending until a new aggregate receipt is linked; older step6-only evidence cannot fill this notebook.

## Prepare once

Use the canonical full clean Git clone inside the existing shared mount with a fresh `EDU_CASE`, for example `edu-journey-20261113-1300`. Set `EDU_TESTED_COMMIT=$(git rev-parse HEAD)` and keep that checkout unchanged throughout execution. Init exactly one `EDU_WORK`; both step3 and step6 live there. SDK sees `/mnt/host/$EDU_CASE/{repo,own}`; HOST sees `$EDU_SHARE/$EDU_CASE/{repo,own}`. Save session-bound predictions using the notebook notes command.

## 1. Intentionally wrong step3

Complete only your own step3 BAR TODO: use the PCI API, validate memory BAR0 extent, map it, check ID010000ed, write **12345679** at offset4 and read the actual complement. Emit exactly one `LEARNER_MMIO id=... write=... read=...` line with actual values; exit0 after the completed operation. Register bounded `edu_learner` slog2 (one page, max_retries3) and write one actual-value `EDU_EVENT mmio id=... write=... read=...` event. A forged expected value is not evidence. Do not create corrected source yet.

Use the canonical SDK build dispatch with `--stage step3 --stock approved-stock-reuse`; preserve the same own notebook through the mount. Use a fresh SDK control directory for this boot (e.g. `sdk-wrong`, replacing every `sdk-control` occurrence consistently). Wait for SDK_READY before queueing. **STOP/REAP**, inspect the owner receipt, require no QEMU and FREE actual lease before native:

```sh
env EDU_NATIVE_LEASE=granted python3 scripts/learner_session.py run --work "$EDU_WORK" --stage step3 --stock "$EDU_STOCK" --timeout 600
```

Expected command status is **1**, not0: notebook nativefresh/FAIL, application `LEARNER_RC=0`, actual12345679→edcba986, **only** device_readback check false. All target/binding/cap/reaping/serial/slog checks must be true. A timeout, missing log or app failure is not the intended wrong-edit outcome: stop and inspect, never proceed blindly. Preserve this failed attempt.

## 2. Only then create the correction

After that actual observation, explain the wrong result in the same notebook, change only the intended write constant to12345678 and retain actual readback/logging. Save the corrected source hash and correction time. Build anew with `--stage step3`; never overwrite the wrong attempt bundle.

You may complete your own step6 registration and compile it serially in this same second SDK boot, after importing its prediction. Use the canonical step6 instructions and `--stage step6 --stock approved-stock-reuse`. This saves a boot, not a validation step. No parallel compiler/linker. A fresh second SDK control directory, e.g. `sdk-correct-finish`, keeps first-boot diagnostics intact. STOP/REAP and verify the FREE lease again.

Run step3 with the same HOST command above. Require nativefresh/PASS, actual12345678→edcba987 and app0; then, and only then, run the already-built own finish.

## 3. Finish with normal I/O, not reference code

```sh
env EDU_NATIVE_LEASE=granted python3 scripts/learner_session.py run --work "$EDU_WORK" --stage step6 --stock "$EDU_STOCK" --timeout 600
```

Require actual10→3628800, write/read rc0, IRQcompletion1/ack0, private same-owner pulse sent1/received1 and matching finite slog2. Explicit `--pci-line` selects existing config11 versus API10 without routing writes. Each stock invocation uses its own overlay; stock IFS/disk stay unchanged. One coherent journey, no retry loop. Stop/report any unexpected outcome. No MSI-X, new secpol/policy layer, CAN/C6, platform/package/swap change or media.

## 4. Explain, export and aggregate offline

Import final notes. Keep all three source snapshots, builds and native observations in the same notebook. Exactly three own builds and three own observations are required; the intended failure remains visible. Then:

```sh
python3 scripts/learner_session.py export --work "$EDU_WORK" --out "$EDU_BASE/own-export"
python3 scripts/learner_journey.py --work "$EDU_WORK" --export "$EDU_BASE/own-export" --tested-commit "$EDU_TESTED_COMMIT" --out "$EDU_BASE/journey.json"
```

The aggregate revalidates every attempt, exact tested driver bytes, failure reason/app0, phase ordering, distinct corrected source, shared stock hashes, current source badges and every export hash. It does not launch guests, fabricate outcomes or import receipts. Both current sources must be CURRENT_SOURCE_RECORDED_PASS. Keep licensed assets/raw ELF readback private outside Git; only original application source, hashes and reviewed text receipts may be committed.

Verify all guests reaped, no QEMU and FREE actual lease; stop for independent review. A later documentation SHA must name the exact runtime source SHA, never pretend the final documentation tip was rerun. No independent-human/fresh-SDK/all-six-stage or platform-health claim.
