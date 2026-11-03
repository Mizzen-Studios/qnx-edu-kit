#!/usr/bin/env python3
"""Small deterministic renderer for this repository's Markdown subset.
Not claat. No network, JS, CDN or third-party modules; metadata is retained in
source. Export pages keep repository-relative links, suitable for local use or
owner-authorized Pages serving later. SVG layouts are original deterministic
renderings of the accompanying four-node Mermaid design sources, not mmdc output.
"""
import argparse
import html
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/site'
CSS = '''
:root{color-scheme:light;--ink:#181c1e;--paper:#fbf8f4;--accent:#6344aa;--line:#c0c0bb}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:system-ui,sans-serif;line-height:1.65}
header{padding:1rem 4vw;border-bottom:3px solid var(--accent)}header a{margin-right:1.5rem}main{max-width:78ch;margin:2rem auto;padding:0 1.25rem 4rem}
h1{font-size:clamp(2rem,5vw,3.2rem);line-height:1.12}h2{margin-top:3rem;border-top:1px solid var(--line);padding-top:1rem;scroll-margin-top:1rem}h3{margin-top:2rem}
a{color:var(--accent);text-underline-offset:.18em}a:focus-visible,summary:focus-visible{outline:3px solid #6344aa;outline-offset:4px}
blockquote{border-left:5px solid #b57913;background:#fff1d6;margin:1rem 0;padding:.6rem 1rem}pre{overflow:auto;background:#232729;color:#fbf8f4;padding:1rem;border-radius:4px}code{font-family:monospace}
img{max-width:100%;height:auto}table{border-collapse:collapse;width:100%;display:block;overflow:auto}td,th{border:1px solid var(--line);padding:.5rem;text-align:left}details{border:1px solid var(--line);padding:.7rem}summary{cursor:pointer}.duration{color:#5b4a25}li{margin:.5rem 0}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
'''

def slug(s):
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

def destination(url, source):
    if '://' in url or url.startswith(('#','mailto:')):
        return url
    target = (source.parent / url).resolve()
    rel = target.relative_to(ROOT).as_posix()
    if rel == 'docs/site/index.html': rel = 'index.html'
    if target.suffix == '.md': rel = rel[:-3]+'.html'
    # every generated content page has canonical paths rooted at docs/site
    depth = len(source.relative_to(ROOT).parts)-1
    return '../'*depth+rel

def inline(value, source):
    value=html.escape(value)
    def image(m):return '<img loading="lazy" alt="'+m[1]+'" src="'+html.escape(destination(html.unescape(m[2]),source),quote=True)+'">'
    value=re.sub(r'!\[([^]]*)\]\(([^)]+)\)',image,value)
    value=re.sub(r'\[([^]]+)\]\(([^)]+)\)',lambda m:'<a href="'+html.escape(destination(html.unescape(m[2]),source),quote=True)+'">'+m[1]+'</a>',value)
    value=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',value)
    return value

def render(source):
    lines=source.read_text().splitlines()
    if source.parent.name=='codelab':
        lines=lines[next(i for i,line in enumerate(lines) if line.startswith('# ')):]
    out=[]; code=False; fence=chr(96)*3; listing=False; table=False
    for line in lines:
        if line.startswith(fence):
            if listing:out.append('</ul>');listing=False
            out.append('</code></pre>' if code else '<pre><code>');code=not code;continue
        if code:out.append(html.escape(line)+'\n');continue
        if listing and not line.startswith('- '):out.append('</ul>');listing=False
        if table and not line.startswith('|'):out.append('</tbody></table>');table=False
        if not line.strip():continue
        if line.startswith(('<details>','</details>')):out.append(line);continue
        if line.startswith('|'):
            cells=[x.strip() for x in line.strip('|').split('|')]
            if all(re.fullmatch(r'[: -]+',x) for x in cells):continue
            if not table:out.append('<table><tbody>');table=True
            out.append('<tr>'+''.join('<td>'+inline(c,source)+'</td>' for c in cells)+'</tr>');continue
        m=re.match(r'^(#{1,3}) (.*)',line)
        if m:
            n=len(m[1]); out.append(f'<h{n} id="{slug(m[2])}">'+inline(m[2],source)+f'</h{n}>');continue
        if line.startswith('Duration:'):out.append('<p class="duration">Planning estimate: '+html.escape(line.split(':',1)[1].strip())+' minutes</p>');continue
        if line.startswith('- '):
            if not listing:out.append('<ul>');listing=True
            out.append('<li>'+inline(line[2:],source)+'</li>');continue
        if line.startswith('> '):out.append('<blockquote>'+inline(line[2:],source)+'</blockquote>');continue
        out.append('<p>'+inline(line,source)+'</p>')
    if listing:out.append('</ul>')
    if table:out.append('</tbody></table>')
    if code:raise ValueError('unclosed code fence: '+str(source))
    depth=len(source.relative_to(ROOT).parts)-1
    base='../'*depth
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>edu-kit · private teaching draft</title><style>'+CSS+'</style><header><a href="'+base+'index.html">edu-kit</a><a href="'+base+'codelab/codelab.html">Codelab</a><span>Host evidence only · QNX pending</span></header><main>'+''.join(out)+'</main></html>\n'

def outputs():
    files=[ROOT/'README.md',ROOT/'codelab/codelab.md']+sorted((ROOT/'steps').glob('**/*.md'))+sorted((ROOT/'docs').glob('*.md'))
    result={OUT / f.relative_to(ROOT).with_suffix('.html'):render(f) for f in files}
    result[OUT/'index.html']=render(ROOT/'README.md')
    result[OUT/'LICENSE']=(ROOT/'LICENSE').read_text()
    for f in (ROOT/'docs/diagrams').glob('*'):
        result[OUT/'docs/diagrams'/f.name]=f.read_text()
    for f in (ROOT/'docs').glob('*.txt'):result[OUT/'docs'/f.name]=f.read_text()
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    stale=[]
    for path,content in outputs().items():
        if args.check:
            if not path.exists() or path.read_text()!=content:stale.append(str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    if stale:raise SystemExit('FAIL: stale local site: '+', '.join(stale))
    print('PASS: local static rendering current (not claat or QNX verification)' if args.check else 'Rendered local static site; nothing published')
if __name__=='__main__':main()
