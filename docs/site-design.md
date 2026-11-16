# Local site design and rendering boundary

Plan before build: light tutorial canvas #fbf8f4, ink #181c1e, purple #6344aa,
rule #c0c0bb and warning #fff1d6/#b57913. System sans for prose and system mono
for commands: no font downloads or falsely claimed Onest assets. Left-aligned
78-character reading column, persistent evidence warning, sequential mini-map,
large architectural SVG figures. The memorable element is the four-stage device
lifecycle; not generic metric cards. The plan's mandated light theme supersedes
the shared dashboard dark theme.

Review: removed dashboard-like cards and ornamental badges. Borders separate
contracts and warnings only. No animations, remote assets or JS. Focus outlines,
responsive figures, overflow-safe code and tables, native details controls.

Host: python3 scripts/render_site.py regenerates docs/site; --check detects stale
output. Open docs/site/index.html locally, or serve the repository using a local
HTTP server bound to loopback. Never expose SDK/image directories. Output is
relative-link static HTML, ready for an owner-authorized Pages configuration,
not a Pages deployment. No workflow is installed and nothing is published.

This is a tested small renderer for the Markdown subset used here, not claat.
claat and Go are not installed; upstream export is not claimed. SVGs are original
accessible four-node renderings paired with Mermaid sources, not output claimed
from an unavailable Mermaid CLI. Tests validate XML and topology labels. The
source remains claat-format metadata plus Duration sections; exact upstream
claat compatibility still needs a real exporter run. No target claim depends
on which renderer is used.

## Freshness maintenance

After editing publication prose or the renderer, run `make refresh-docs` from
the repository root, then `./verify.sh --host-only`. Commit source changes and
generated derivatives together. Publication edits at `76c513c` omitted this
refresh and left the site and review appendix stale: a host packaging failure,
not a QNX runtime failure.

The ordered refresh renders HTML, inventories review
hashes, then renders again to copy those JSON inventories into the site.
The review inventory does not hash its own JSON projection; HTML is independent of
that inventory, so the second render reaches a fixed point. The target
checks outputs without rewriting historical receipts, source pins or dry-pack
assets. Repeating the target must produce no changes. Host freshness never
grants native or independent learner acceptance.

Run `python3 tools/proof_capture.py` and `python3 tools/claim_lint.py`
separately: these are stricter frozen-copy gates, not just site freshness.
As of Nov16 they deny changed README/codelab instruction copies at T01.
Do not rebind frozen assets or suppress that denial to make freshness pass.
