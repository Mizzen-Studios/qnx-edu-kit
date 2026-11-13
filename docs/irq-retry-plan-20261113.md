# One stock IRQ retry — Nov13 11:03 owner scope

Prior result: [stock retry](acceptance/stock-retry-20261113/RESULT.md), finish IRQ timeout while attached to PCI API IRQ10. Wrong/correct MMIO gates already proved there and are not repeated.

## Justification before native attempt

HostShare commit22ca7a77c94e7af4e7f8f182b82b9c1d0dc55fcf cold-stock probe reports API10/config11 and actual IRQ pulses with explicit --pci-line, without qtest or routing writes. Its completion/used ring is authoritative before treating ISR as a hint; EDU differs: its own pending register is not read-clear, so retain the real-wake + own pending bit + not-busy requirement. Do not transplant the virtio ISR workaround into EDU.

Installed private neutrino.h and pci/pci.h contain the required declarations; no SDK implementation/headers copied into Git. QNX8 API references: [InterruptAttachThread](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.lib_ref/topic/i/interruptattachthread.html) automatically unmasks on first attach unless NO_UNMASK; [InterruptUnmask](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.lib_ref/topic/i/interruptunmask.html) reserves argument0, attachment ID is second. Existing EDU attach/ack/unmask ordering stays unchanged.

Minimal source change: explicit --pci-line reads config bytes0x3c/0x3d, reports API/line/pin, rejects invalid legacy line/pin, and attaches to the existing line. Default mode remains API. No PCI config writes, PIRQ rewrites, qtest, guessed line11 constant or platform repair. Failed waits report errno/pending/status/result without accepting polled completion. Learner completed-source SHA256 c84e91925d84731b18e1ad11718b692a78e351bf2f633895e9781c7ef8641ef7.

One serial SDK compile/link, existing license only. SDK<=1024MiB, HOST2GiB CPU100 nice15 smp1 TCG256 swap0 reserve64. Stop/reap SDK before at most ONE native512MiB attempt. No image generation: IFS68bbe1b49a9b723c09d152773ee323ec6ab576eb29de933bfe3f08fdae21c753; disk0aee00c281f8eeb5b02c66555ed9517e317bb1503002a19dbf2b0155de336532. Transfer ELF, exact guest byte readback, then one /dev/edu10 transaction. Require actual3628800 plus IRQ/ack, otherwise precise BLOCKED. Historical receipts unchanged; stop/reap/free lease and owner review regardless of outcome. No current retry PASS is claimed by this plan.
