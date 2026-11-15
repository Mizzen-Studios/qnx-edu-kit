# Fresh captioned live recording — 15 November 2026

**PASS: one fresh coherent QNX8.0 journey, captured before live commands.** Exact tested runtime source: **a26962acd737f57bd6d3199384ccfa9cbd63f0f6**. Later evidence/site commits package this run; they are not another native rerun. No project code changes, old receipt/log/footage import, IFS regeneration or retry.

- Wrong own step3: actual12345679→edcba986, application exit0, independent FAIL **only device_readback**.
- Corrected **after observing failure**, only12345679→12345678 changed: actual12345678→edcba987, exit0, all14checks PASS.
- Own step6: actual normal write10/read3628800, real IRQcompletion1/ack00000000, same-owner private pulse sent1/received1 and matching finite slog2; all19checks PASS.
- Same notebook45154234-bc23-4ec0-862a-d59f4da49280: three fresh builds, three native observations, **102-file own export independently rehashed**, wrong failure retained. Current step3/step6 badges CURRENT_SOURCE_RECORDED_PASS.

[Aggregate receipt](receipt.json), [recording/media receipt](recording.json), [frame/time/byte provenance](video-provenance.json), [one-constant correction](correction.txt), [export manifest](export-manifest.json), [resource and cleanup summary](resources.json).

Original phase material: [wrong receipt](wrong-native.json) / [observation](wrong-observation.json) / [readable output](wrong-native.txt) / `wrong.c` source snapshot; [correct receipt](correct-native.json) / [observation](correct-observation.json) / [readable output](correct-native.txt) / `correct.c` source snapshot; [finish receipt](finish-native.json) / [observation](finish-observation.json) / [readable output](finish-native.txt) / `finish.c` source snapshot. Application C was reused as source input and freshly compiled in the new notebook; no old ELF, observation or receipt supplied any phase. The one-constant wrong/correct diff is timestamped after this run's wrong observation.

## Video and capture integrity

**165.000 seconds,1920×1080,H.264,30fps,2,692,342bytes; no audio/music/voice.** MP4 SHA256 **3aaa0223023e2fec76a9f6e7d832cdb08aabaafbdf5becf16079f96e0dadd37b**. Video and stills are private external artifacts, not Git objects. Private draft-release attachment, if created, is not publication or a visibility change.

This is an explicitly edited **terminal render of this live run**, not a continuous realtime screencast. Timed command stdout and native serial bytes were recorded before the first clone/build/native command. Each displayed runtime row maps to original capture event sequence and native serial byte range. Serial streams were independently reconstructed from captured chunks and byte-for-byte compared with this run's original serial files. Source/diff views are labeled separately. Captions are receipt annotations, not fabricated terminal output. Boot/build/ELF transport waits are omitted and output screens held for readability; the footer discloses editing throughout. No old logs were spliced in. Host personal paths are masked in media; no email/secret/personal path is displayed.

The export chapter is a separately timed **actual offline inspection of this same new own export** after native cleanup, not another guest run. It reads/re-hashes the export and prints real attempt statuses/retention, source badges and exact runtime source. The original raw capture remains unchanged; supplemental capture has its own hash. Full private raw capture includes ELF transport/readback and stays outside Git. Only hashes, source, reviewed application observations and frame provenance are committed; no SDK bytes, ELF, images or large video.

## Resource and scope boundaries

Two serialized existing SDK boots1GiB, three fresh native512MiB boots; HOST cap2GiB, CPU100%, nice15, smp1, TCG256MiB, swap0, reserve64MiB. SDK cgroup peaks997310464/1046822912bytes; native515190784/517193728/517484544bytes. Every SDK STOP/REAP barrier passed before native. All guests reaped; final zeroQEMU and FREE actual lease verified.

Approved stock reused unchanged: IFS68bbe1b49a9b723c09d152773ee323ec6ab576eb29de933bfe3f08fdae21c753, disk0aee00c281f8eeb5b02c66555ed9517e317bb1503002a19dbf2b0155de336532, plus pinned VMDK/options. No stock regeneration or licensed redistribution. Raw source/object/ELF/IFS/disk bindings are in the phase receipts.

One automated advanced-lab journey, not independent human learner/fresh install, a production driver, platform-health, secpol, MSI-X, HA, safety/timing or broad portability acceptance. SSH/platform health remain UNVERIFIED. CAN frozen, C6off; no contacts, login/install, public release or spending. Keep PRIVATE; STOP for owner review.
