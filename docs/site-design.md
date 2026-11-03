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
