# Fixed-cap build diagnosis

The first image build failed under the required 512 MiB SDK guest limit:
Linux guest OOM killed the kernel relocatable linker (guest pid 951), and a
retry after cloud-init settled also failed (pid 1035). qcc successfully produced
the edited application ELF; mkifs kernel relinking was the memory-heavy phase.
Neither CPU/memory limits nor guest RAM were raised. This is a build resource
failure, not a learner stage result. Recovery uses a private debug-stripped copy
of the licensed relocatable kernel in a separate search directory (original SDK
unmodified), plus the bootstrap linker memory-reduction flags. The prelinked
EXEC .sym experiment was rejected by mkifs and was not used. Exact local adapter
is retained as original shell/Python source only; no kernel copy is distributed.
The native receipts determine whether the resulting images actually work.
