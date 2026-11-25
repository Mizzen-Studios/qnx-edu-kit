"""Deterministic offline worksheet export; not claat or target execution."""
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def outputs():
    raw = (ROOT/'codelab/qnx-traps/catalog.json').read_bytes()
    data = json.loads(raw)
    data['sha256'] = hashlib.sha256(raw).hexdigest()
    # Script element is inert JSON; escape < to prevent a closing-tag injection.
    payload = json.dumps(data, ensure_ascii=True).replace('<', r'<')
    script = (ROOT/'codelab/qnx-traps/lab.js').read_text()
    css = '''body{font:18px/1.55 system-ui,sans-serif;color:#172b3a;background:#f6f9fc;margin:0}main{max-width:70ch;margin:auto;padding:1rem}h1{line-height:1.1;font-size:clamp(2rem,6vw,3rem)}fieldset{min-width:0;border:2px solid #56728a;margin:2rem 0;padding:1rem}legend{font-weight:bold;padding:.3rem}label{display:flex;gap:.6rem;align-items:start;padding:.7rem 0}input{margin-top:.4rem;flex-shrink:0}button{font:inherit;padding:.7rem 1rem;margin:.5rem .5rem .5rem 0;background:#174f79;color:white;border:2px solid #174f79;border-radius:4px;cursor:pointer}a{color:#174f79}a,button,input{outline-offset:4px}button:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid #aa4800}[role=status]{margin:.7rem 0;overflow-wrap:anywhere}aside{border-left:5px solid #aa4800;padding:.5rem 1rem;background:#fff0dd}code{overflow-wrap:anywhere}'''
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'self'; style-src 'unsafe-inline'; connect-src 'none'; img-src 'none'; base-uri 'none'; form-action 'none'"><title>QNX trap lab | HOST worksheet</title><style>'''+css+'''</style><main><nav><a href="../../index.html">Start here</a> · <a href="qnx-traps.html">Codelab instructions</a></nav><h1>Catch the QNX trap.</h1><p>Five steps. Predict, check, diagnose, fix.</p><aside><strong>HOST reasoning only. Native validation: NOT_RUN.</strong> No SDK, QEMU or commands run here. Choices stay in this page until you download them.</aside><p>Start with any step. Feedback explains the expected scenario, not an observed target result.</p><div id="worksheet"></div><button type="button" id="check-all">Check all steps</button><button type="button" id="download">Download answers for CLI</button><p id="summary" role="status" aria-live="polite">No answers checked. Native validation NOT_RUN.</p><noscript>This worksheet needs JavaScript; use the Python checker instead. Read the codelab instructions above.</noscript><p>CLI: <code>python3 scripts/check_traps.py --answers qnx-trap-answers.json</code></p><p>The catalog hash detects stale or mismatched worksheets, not cheating or authenticity. The answer key is intentionally readable. No native receipts are accepted.</p><script type="application/json" id="trap-data">'''+payload+'''</script><script src="lab.js" defer></script></main></html>
'''
    out=ROOT/'docs/site/codelab/qnx-traps'
    return {out/'index.html':page,out/'lab.js':script}
