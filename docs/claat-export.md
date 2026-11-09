# Official claat local export (private draft)

**Nov9 tutorial-copy update:** current codelab differs from the immutable historical export receipts. Current static-site/host checks are not a fresh official claat export or native run. Historical export hashes remain unchanged; current source match is correctly false.

## Reproduce

Python 3 standard library, Linux, network only for the explicit first download:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/export-codelab.py \
  --download --tool-cache "$HOME/.cache/qnx-edu-claat" \
  --output "$HOME/qnx-edu-export-$(date -u +%Y%m%dT%H%M%SZ)"
CLAAT_TOOL_CACHE="$HOME/.cache/qnx-edu-claat" PYTHONDONTWRITEBYTECODE=1 \
  python3 -m unittest discover -s tests -p 'test_codelab_export.py' -v
```

Both paths must be outside the checkout; output must not exist. Omit
--download after caching. No Go installation is required. Linux amd64 runs
natively; ARM64 additionally needs the distribution's qemu-x86_64-static.
This is **user-mode process emulation**, not a QNX/QEMU guest boot. The wrapper
never installs dependencies, controls an SDK/VM, serves a port, or publishes.

## Pin and provenance

- Official repository: https://github.com/googlecodelabs/tools
- Release: https://github.com/googlecodelabs/tools/releases/tag/v2.2.6
- Asset: https://github.com/googlecodelabs/tools/releases/download/v2.2.6/claat-linux-amd64
- SHA-256: b7415471bd823562ebd9e6015e267a12fbf9340dfe839f8e2a175b6c7c0f397a
- Actual embedded version: 2.2.5-2023-06-15T18:32:06Z-872cbcf

The release label and embedded version differ upstream; both are checked, not
silently relabelled. The checksum was measured from the official HTTPS release
asset and is a reproducibility pin, **not an independently signed attestation**.
No binary, font, licensed SDK, or generated claat bundle is committed.

Verified on Ubuntu ARM64, 6 November 2026, using the already installed Ubuntu
qemu-user-static package 1:8.2.2+ds-0ubuntu1.18, /usr/bin/qemu-x86_64-static.
No packages were installed and no QNX guest was started by this work.

## What the wrapper does

The raw upstream command fails on the source's ../docs/diagrams/*.svg paths:
claat disallows image files outside the Markdown source directory. The wrapper
stages a copy at a common root and relocates local Markdown link/image paths
only. All lesson prose, metadata, durations, status and existing SVGs stay
unchanged. It invokes the actual official claat html exporter with -ga '';
**index.html and codelab.json are produced only by upstream claat**.

Repository-authored text (.md/.svg/.mmd/.json/.txt/.c/.h) from docs (excluding docs/site),
steps and native are copied alongside the output so the twelve step1..step6
starter/solution README links resolve locally. The incremental C snapshots derive from the unchanged E1 implementation;
no newly compiled snapshot target outcome is claimed.
The output contains a retained _source directory, the upstream qnx-edu-kit
bundle, and a separate house export-receipt.json. No fabricated claat metadata
is injected. The receipt records tool/source checksums, runner and checks.

Checks require six core google-codelab-step elements, twelve byte-identical
starter/solution README files, every exported HTML local href/src resolving
inside the bundle, and eight byte-identical SVG images. External references
are listed explicitly, not asserted to be available or safe for offline use.
Default upstream HTML references Google-hosted JS/CSS/fonts/support scripts;
this is **not** the repository's dependency-free static renderer and is not
an offline/privacy-hardened browser bundle. Export success is not a browser
render or target execution claim. Use a separate fresh output for each run;
claat update is not part of this workflow.

## Current E2 content and scope

The first-step warning now lives inside H2 step1 so upstream retains it.
Validation explicitly rejects missing PRIVATE DRAFT/QSTI warnings, missing
core steps, broken local links, changed source snapshots or changed SVGs.
Twelve readable main.c snapshots accompany the twelve README folders;
original native .c/.h and historical acceptance .json/.txt are text-only assets.
No licensed headers, binaries, images, or SDK implementation are staged.

E1 at 387ba38 is associated with all-six native functional PASS. All twelve E2 snapshots have separate compile-only receipts; per-snapshot target execution and two fresh learners remain pending. QSTI provenance is
unverified. Source/host/export checks do not earn target acceptance. The
44-minute upstream sum is only six unmeasured private planning estimates.
No publication, hosted site, video, submission or public PR is authorized.
