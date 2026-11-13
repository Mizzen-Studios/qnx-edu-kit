# Coherent own stock journey — 13 November 2026

**PASS: one own notebook, wrong FAIL/app0 → corrected PASS → own /dev/edu finish → verified export.** [Top-level aggregate receipt](receipt.json) binds all phases, their source/object/ELF, shared stock IFS/disk, exact tested source and export. [Verification inventory](verification.json), [resources/cleanup](resources.json), [notebook](notebook.json).

**Runtime source:** `769a4c906c6b172c3624f8fe897b71e3c5d7e6b8`, full clean non-shallow Git clone. CI43431441472 SUCCESS; that clone ran139 host tests137pass/2skip plus site/lint/proof/inventory checks. Later documentation commits package these exact observations; they are **not** new runtime executions at the final documentation SHA.

| Phase | Actual outcome | Own source | Native receipt / exact serial observation |
|---|---|---|---|
| Wrong step3 | actual12345679→edcba986; app0; only device_readback false, intended nativeFAIL | [wrong.c](wrong.c) | [receipt](wrong-native.json), [raw observation](wrong-observation.json), [readable log](wrong-native.txt) |
| Corrected step3 | actual12345678→edcba987; app0; all14checks true | [correct.c](correct.c) | [receipt](correct-native.json), [raw observation](correct-observation.json), [readable log](correct-native.txt) |
| Own step6 | normal write10/read3628800; write/read0, IRQcompletion1/ack0, pulse sent1/received1, matching slog2; all19checks true | [finish.c](finish.c) | [receipt](finish-native.json), [raw observation](finish-observation.json), [readable log](finish-native.txt) |

The [correction record](correction.json) timestamps creation **after** the wrong native observation. Only the write constant changed; actual readback/logging remained. The failed source, build and native receipt remain in the same notebook and export. Own finish registration is newly authored in this notebook; no reference binary, saved receipt import, output injection or polling fallback. Explicit `--pci-line` selects config11 versus API10; no routing rewrite.

## Build and platform boundary

Three fresh application builds under two serialized SDK boots; three native boots, exactly one per phase. Second SDK boot compiled corrected step3 then step6 serially; correct nativePASS preceded finish native execution. No retry, offline repair or failed-outcome relabeling in this journey.

Approved stock artifacts reused unchanged: IFS `68bbe1b49a9b723c09d152773ee323ec6ab576eb29de933bfe3f08fdae21c753`, disk `0aee00c281f8eeb5b02c66555ed9517e317bb1503002a19dbf2b0155de336532`, plus pinned VMDK/options. **No IFS generation, fresh SDK installation or second SDK.** Each runtime overlay is separate; exact serial ELF byte readback was verified before execution. Licensed artifacts and raw ELF readback stay outside Git in the private export.

SDK guest1GiB/native512MiB, HOST2GiB/CPU100%/nice15/smp1/TCG256/reserve64MiB/swap0. SDK peaks959688704/908460032B; native peaks517160960/515072000/515256320B. All owners confirm reaping; SDK STOP/REAP barriers were verified before native. Final zeroQEMU and FREE actual lease confirmed. No cap/swap/platform/package change requested or performed by this wave.

## Own export and scope

**108 files independently rehashed**, manifest completeness checked. Pack SHA256 `c559b4d84cccccf4e6f07206964c04c56c6320d374823c91c1a572503b608652`; [manifest](export-manifest.json). Both current step3 and step6 source badges are CURRENT_SOURCE_RECORDED_PASS. Aggregate SHA256 `1892768093e88f78bb4337aa20a7175cb7512192abd5fe97458edcd60139110b`.

One automated advanced-lab journey using an existing licensed SDK and disclosed local handoff, not independent human/fresh-install/all-six-stage/broad portability acceptance. SSH/platform health UNVERIFIED; trace NOT_RUN. No new secpol/HA layer, MSI-X, CAN/C6 work, IFS regeneration, recording/publication/contacts/install/login or spending. Old receipts/native pins remain unchanged. STOP for independent parent review.
