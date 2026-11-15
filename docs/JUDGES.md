# Judges: start here

QNX Global Hackathon 2026 entry (Low-level Software; Best Codelab/Tutorial). Apache-2.0. No paid resources used.

## Proven coherent journey

The [coherent stock result](acceptance/coherent-stock-20261113/RESULT.md) and [aggregate receipt](acceptance/coherent-stock-20261113/receipt.json) bind one own notebook, source/object/ELF hashes, shared stock IFS/disk and verified 108-file export.

1. Wrong edit: write `12345679`, read `edcba986`; **FAIL despite application exit 0**.
2. Correction created after observing failure: write `12345678`, read `edcba987`; **PASS**.
3. Own resource manager: normal write `10` / read `3628800`, real IRQ completion/acknowledge, same-owner private pulse and matching finite slog2 observations; **PASS**.

Exact tested runtime source: `769a4c906c6b172c3624f8fe897b71e3c5d7e6b8`. Later documentation commits package that run, not a final-tip native rerun. Historical failures remain unchanged.

## Advanced-lab prerequisites and route

Start with the [working stock learner route](learner-route.md), then the [one-notebook checklist](coherent-journey.md), [codelab](../codelab/codelab.md) and [cockpit help](learner-cockpit.md). Existing licensed QNX SDP 8.0, an exclusive SDK/QEMU lease and external approved hashed stock IFS/disk are required. No licensed artifacts are bundled.

Application compilation/linking in the existing SDK environment:

```sh
qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g0 -Wall -Wextra -Wno-unused-variable -c main.c -o main.o
qcc -Vgcc_ntox86_64 -o main main.o -lpci -lslog2
```

Target: QEMU `qemu-system-x86_64`, `-m 512 -smp 1 -device edu`, TCG. These are target flags, not a complete boot command: use the stock-console runner and route image/options/resource gates. **STOP/REAP SDK before native boot.** HOST2GiB, SDK1GiB, native512MiB, TCG256MiB, reserve64MiB, CPU100%, nice15, swap0.

Stock `mkqnximage` generation needs **at least 1GiB on the build machine** for this verified recipe: compare the [512MiB failure](acceptance/stock-20261113/NOTES.md) and [1GiB success](acceptance/stock-retry-20261113/RESULT.md). This is the measured recipe boundary, not a universal minimum guarantee. The coherent journey reused these hashed files without regenerating IFS. [Owner-lab controller contract](../tools/owner_lab/README.md).

### Exact observed stock generation command — existing licensed SDK only

For reference, this observed stock-generation recipe runs **inside the existing licensed SDP8.0 environment**, on the SDK build machine with **at least1GiB RAM**, in a fresh project directory. The target remains512MiB/one CPU: target RAM is not builder RAM. No installation or activation is implied. The supported coherent learner journey **reuses the approved hashed stock artifacts**; do not regenerate IFS for that route or substitute a newly built unreviewed image.

```sh
# SDK guest: set EDU_SDP_ENV to your existing licensed environment file.
. "$EDU_SDP_ENV"
mkdir stock-edu-project
cd stock-edu-project
mkdir -p local/snippets
printf '%s\n' '-device edu' > local/snippets/qemu_options.edu
mkqnximage --type=qemu --arch=x86_64 --ram=512M --cpu=1 --ssh-ident=none --build
```

The authored snippet adds only the EDU device to stock QEMU options. The installed runimage consumes generated output/build/qemu_options as QEMU_OPTIONS. See the [canonical stock recipe and legal handoff](learner-route.md), [512MiB build failure](acceptance/stock-20261113/NOTES.md) and [1GiB stock success](acceptance/stock-retry-20261113/RESULT.md). These commands document the observed recipe, **not a new build/native run at this commit**.

## Limits

**DIRECT route UNVERIFIED.** Independent human learner completion, fresh/second SDK installation, SSH/platform health, actual secpol and MSI-X are **not proven**. Host CI is not QNX runtime proof. No production safety, timing, availability or broad portability claim. `Published` is codelab metadata, not evidence of a public repository or hosted release.
