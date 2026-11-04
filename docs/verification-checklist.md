# Live verification ledger — NOT tutorial instructions

The plan 7.5 register gate now has **live QEMU device evidence**, not QNX
API/driver evidence. Observations: installed QEMU 8.2.2 Ubuntu1.18 through
qtest on ARM64 Linux with an x86 PC machine. See [method](register-evidence.md)
and [text log](register-qtest-live.txt). No QNX lifecycle assertion follows.

| Row | Observed offset/width and behavior | State |
|---|---|---|
| PCI identity | 1234:11e8, BAR0 1 MiB memory at 0xe0000000; MEM+MASTER | QEMU PASS; QNX ownership pending |
| ID | 0x00 / 32, 0x010000ed, bytes ed000001; RO | QEMU PASS |
| Liveness | 0x04 / 32, five complementary inverse patterns | QEMU PASS |
| Factorial | 0x08 / 32, 0..13 modulo32; large input busy + ignored resubmit; bounded poll | QEMU PASS; driver accepts 0..12 |
| Status | 0x20 / 32, busy bit 1 RO; IRQ enable 0x80 RW | QEMU PASS |
| IRQ status | 0x24 / 32, RO pending OR bits 1 and 0x100 | QEMU PASS |
| IRQ raise | 0x60 / 32, OR pending and IOAPIC IRQ11 assertion | QEMU PASS |
| IRQ ack | 0x64 / 32, partial clear holds IRQ11; full lowers; retrigger | QEMU PASS |
| DMA source | 0x80 / 32,64; real host-to-device and reverse bytes | QEMU PASS |
| DMA destination | 0x88 / 32,64; real round-trip bytes both directions | QEMU PASS |
| DMA count | 0x90 / 32,64; 1/100/4096 work; 0/4097 abort QEMU | QEMU PASS |
| DMA command | 0x98 / 32,64; RUN1 DIR2 IRQ4; RUN clears; busy writes ignored | QEMU PASS |
| DMA buffer | 0x40000..0x40fff; full4096 and last byte; beyond/crossing abort | QEMU PASS |
| DMA mask | Default28-bit and override24-bit high source/dest alias low RAM | QEMU PASS; last valid bytes / first-above wrap tested |
| Interrupt model | Default INTx routed IOAPIC11; factorial/manual/DMA assert/clear | QEMU PASS; MSI/QNX delivery untested |

Use naturally aligned accesses. An unaligned qtest 64-bit write at 0x04
splits into two 32-bit writes (including factorial submission!), not rejection.
Aligned 64-bit ID read returns all ones. qtest byte/word reads return zero;
these are not supported device widths. Subword writes and full misalignment
matrix are unvalidated. Pinned source allows only 32-bit below 0x80 and
32/64-bit at DMA registers. QNX target validation remains pending for all rows.

## Required evidence per row

- Date, operator, clean-clone commit, host/guest architecture and OS.
- SDP build, toolchain selection, QSTI version/image hash (no image redistribution), QEMU version and pinned source hash.
- Exact reviewed local build/run commands, access widths, input/output and expected-vs-observed result; failure/timeout paths.
- Relevant source/doc reference lines and distinction between source reading, host model and live target result.
- Sanitized transcript file + hash, reviewer and limitations. No credentials, proprietary source, image or SDK files.

## Whole-project acceptance (QNX still pending)

1. Approved local licensed SDK setup, verified target boot and deployment user/path.
2. Current PCI server API review, BAR lifecycle, restart-safe re-probe, bounds.
3. QEMU register semantics verified independently; QNX code still needs SDK review and target tests.
4. Abilities and secpol deny/allow experiments; least privilege after attach; exact policy syntax verified. No guessed policy distributed.
5. Real IAT/InterruptWait lifecycle, concurrent operations, error and cleanup tests.
6. Real resource-manager finish line, malformed/overflow/partial I/O and concurrency tests.
7. DMA/cache/physical-address handling and restart/trace extras independently gated.
8. Eight source diagrams and rendered SVGs from verified flows; claat export validated.
9. Two fresh-agent clean-machine runs following only the codelab; actual elapsed times, failures and corrections recorded.
10. Mandatory real QNX capture; publication, Pages, PR and submission require separate permission.

Host model tests, if later added, must carry pinned-source provenance and UNVERIFIED MODEL labels; never upgrade these live statuses based on a host test.
