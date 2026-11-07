# Six teaching snapshots

Follow [E2 build order](../docs/e2-build-order.md) in a separate learner copy.
Each step has starter/main.c (deliberately incomplete) and solution/main.c.

| Step | Boundary | Native observation still required for this snapshot |
|---|---|---|
| 1 | QNX process | Actual target identity and STEP1 marker |
| 2 | PCI attach | Exclusive EDU attach and STEP2 marker |
| 3 | BAR registers | ID/complement operation and STEP3 marker |
| 4 | Factorial polling | Input10, result3628800 and STEP4 marker |
| 5 | IAT plus polled DMA | IRQ raise/wait/ack and64-byte exact roundtrip |
| 6 | IAT resource manager | Actual client shell echo10/cat3628800 |

All twelve snapshots have source-bound qcc compilation evidence, not native
execution acceptance. The separately accepted accumulated E1 reference is not
a substitute for executing these exact binaries. make check-stepN boots that
reference after checking source equivalence; it does not deploy learner code.

Keep each future runtime receipt bound to snapshot source, executable and image
hashes, effective caps, fresh raw serial and exit status. Run one exclusive
guest at a time:CPU100%,1GiB,nice15; guest1vCPU/512MiB. No SDK/binaries in git.
Step6 stays in dispatch:collect functional output before stopping its owned
process. Starter TODO exits must never be relabelled as native PASS.
