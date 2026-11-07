# Startup fault diagnosis — 7 November 2026

Unchanged baseline IFS a48335ec842c824d52bb2c713365e7afcf0ae8ec259369f3c20c0c723eccec2b reproduced the Memory fault before the learner; normal learner I/O still passed. Not healthy-platform acceptance.

Separately bound traced image c17fab9f9c82d068714dfd3c1d598f5388d32803c15947935919582a3754d66a changes external generated startup tracing/diagnostics. NOT the unchanged baseline. Shell trace attributes the fault to /system/bin/sshd -f /system/etc/ssh/sshd_config; qconn follows successfully. pidin shows qconn but no sshd; dumper lists sshd.core (7880704 bytes). Both host keys already existed, so no ssh-keygen command ran. Core contents remain external. Internal root cause remains UNVERIFIED; no SDK/sshd patch or SSH/full-platform health claim.

Inputs/caps bound separately in baseline.json and traced.json. Same matching clean disk, snapshot-on; CPU100%/1GiB/nice15, guest1vCPU/512MiB; exclusive flock. SDK stopped/reaped before native. C6 never executed; SocketCAN UNVERIFIED.

Failures preserved externally: inspection timeout180 before SDK boot later returned0 without resubmission; HOME-unset launchers; local sed/Python quoting failures; direct mkifs without guest swap OOM-killed guest linker PID928 anonRSS320040KiB, no normal queue exit and zero image not promoted. Isolated builder first failed output permission; after ownership correction and1GiB disk swap, edu-diagnosis-trace2 completed success/ExecMainStatus0/inactive. Raw generated scripts, licensed images and full logs stay external at /home/ubuntu/qnx-host/guest/shared/diagnosis-20261107 and shared/results. No SDK code in these receipts.

Source checkout c8651459463d81c5d66d685444bfa25b92c94bc9; baseline runner hash in receipt. No retrospective tested-commit binding for older builds. Independent human/owner re-review not done.
