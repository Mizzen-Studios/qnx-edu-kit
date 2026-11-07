# Owner-authorized single swap attempt — 7 November 2026

Gate remains NOT PASSED. One fresh stock generic build, 1800-second build limit (1830-second unit ceiling), 512 MiB guest + 1 GiB disk-backed guest swap. Host CPUQuota=100%, MemoryMax=1G, nice15, one vCPU unchanged. No host swap/cap changes, stripped kernel, cached private image, or licensing change. Previous diagnosis900 receipts preserved.

Finding: the earlier guest global OOM killed a linker in host-queue.service. Its OOMPolicy=stop then stopped the controller/waiter as well, losing the ordinary build exit. This attempt places the builder in a separate transient guest systemd service, with the queue/monitor outside that service. Capture service Result/ExecMainCode/ExecMainStatus even if the build wrapper cannot write an exit receipt.

Conditional next steps: only if the stock image completes, integrate fresh learner snippets, compile wrong/correct sources, and run distinct source/binary/image/disk-bound native assessments. Then learner /dev/edu normal I/O completion, not a transferred reference PASS. Otherwise preserve failure and stop; no second memory strategy or build retry. C6 STOPPED.
