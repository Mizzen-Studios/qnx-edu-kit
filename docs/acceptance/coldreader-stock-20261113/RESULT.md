# Fresh clean-clone own stock checkpoint — 13 November 2026

**PASS native and own export after an offline notebook-validator fix.** One SDK boot, one native boot; no image regeneration or native retry. [Receipt](receipt.json), [actual observation](observation.json), [readable log](native-readable.log), [own source](own-step6.c), [export verification](export-validation.json).

A full clean, non-shallow Git clone at `667d62b5bf9536bbf5694d7753258f802be8a7cf` followed its published stock-reuse recipe. Own registration was completed in a fresh notebook, not copied from an old receipt. Fresh compile/link produced ELF `6ac7621815ad74592a99bd2abb3a2f80600e93313f8152b4aa5cdfc2124fdce0`; approved external stock IFS/disk were reused. This reproduces application build/observation, **not** stock image generation, SDK installation, an independent human result or the full wrong/correct learner journey.

## Actual observation

- QNX8 x86pc, normal write10/read3628800, both rc0; IRQcompletion1/ack00000000.
- API10/config11/pin1, explicit read-only `--pci-line`, no routing rewrite.
- Same-owner private pulse sent1/received1, matching finite slog2 IRQ/pulse entries.
- ELF serial readback verified; source/object/ELF/IFS/disk bindings and all19 native checks passed.
- SDK guest1GiB and native guest512MiB, HOST2GiB/CPU100%/nice15/smp1/swap0/TCG256/reserve64. SDK peak911470592B; native peak517201920B. SDK stopped/reaped before native; both owner receipts confirm reaping. No guests remain, actual lease FREE.
- Read-only probes: secpolpush absent; secpolmonitor installed. No policy loaded/displaced; deny/allow **BLOCKED**. Trace **NOT_RUN**. SSH/network health **UNVERIFIED**.

## Gaps found and repaired, not hidden

1. The initial clone's host suite had130pass/2skip/1fail: a test rejected the declared checkout location under qnx-host. Test-only fix3738c63 allows the actual repository prefix but continues rejecting undeclared lab paths. Failed log retained.
2. Native driver returned0 and all19checks true, but notebook validation reported `stock log changed`: `read_text()` normalized raw CRLF. The fix compares exact UTF-8 bytes against the original serial JSON. Changed bytes and normalized substitutes are still rejected. The [pre-revalidation notebook](notebook-before-revalidation.json) is preserved. Host-only `revalidate` checks all source/build/driver/stock/log/cap/oracle bindings, archives the prior notebook and updates its validation state. No target work repeated; raw native receipt/observation unchanged.

The new OWN export has41 independently rehashed files, pack SHA256 `f731641749aeb3928c5a0a71534e4e173939aaa7d3df937e2dda0e1cbbf4ac10`. Step6 is CURRENT_SOURCE_RECORDED_PASS; untouched step3 is CURRENT_STAGE_NOT_VALIDATED. Licensed artifacts, raw serial ELF readback and runtime overlay remain only in the private local export. Git contains original application source, hashes and text receipts. `native-readable.log` is whitespace-normalized for reading; `observation.json` retains the exact original serial text and the receipt records the raw log hash.

All older failed receipts/native pins remain unchanged. No MSI-X/CAN/C6, platform/package/swap changes, installation/login, media, publication or spending. Independent parent review pending.
