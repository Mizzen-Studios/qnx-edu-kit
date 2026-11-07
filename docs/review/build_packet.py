#!/usr/bin/env python3
"""Offline review inventory: no runtime, SDK, or network actions."""
import hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def rec(path,label,logs=(),commit=None,note=''):
 p=ROOT/path; d=json.loads(p.read_text()) if p.suffix=='.json' else {}
 hashes={}
 def walk(x,prefix=''):
  if isinstance(x,dict):
   for k,v in x.items():walk(v,prefix+'/'+k)
  elif isinstance(x,list):
   for i,v in enumerate(x):walk(v,prefix+'/'+str(i))
  elif isinstance(x,str) and re.fullmatch('[0-9a-f]{64}',x):hashes[prefix]=x
 walk(d)
 return dict(path=path,sha256=sha(p),label=label,receipt_hash_fields=hashes,raw_logs=[dict(path=l,sha256=sha(ROOT/l)) for l in logs],tested_source_commit=commit or 'UNVERIFIED: receipt binds source bytes, not a tested repository commit',archival_commit=git('log','--diff-filter=A','--format=%H','--',path).splitlines()[-1],note=note)
def build():
 b='docs/acceptance/'; n=b+'native-20261107/'; c=b+'clean-step3-20261107/'; f=b+'learner-finish-clean-20261107/'
 e={
 'reference':rec(n+'receipt.json','observed in this QEMU run',[n+'serial.txt'],note='Image and four source hashes present. Binary/disk hashes and tested commit absent: UNVERIFIED binding. Do not infer them from later source or commit.'),
 'reference-clean':rec(n+'clean-checkout-receipt.json','observed in this QEMU run',[n+'clean-checkout-verify.txt'],note='STATUS associates checkout 387ba38ce696c92bb3d8332ea7f01d5a0630cbfc; receipt itself does not bind that commit, executable or disk. Association is not receipt proof.'),
 'compile':rec(b+'e2-qcc-20261107/receipt.json','observed SDK compilation only',[b+'e2-qcc-20261107/compile.txt'],note='Twelve source hashes; twelve binary hashes extracted separately from raw compile log. No image/runtime claim. Solutions Werror; starters retain warnings.'),
 'step3-wrong':rec(c+'native-clean/final-topology/wrong-native.json','observed in this QEMU run',[c+'native-clean/final-topology/wrong-native.log']),
 'step3-correct':rec(c+'native-clean/final-topology/correct-native.json','observed in this QEMU run',[c+'native-clean/final-topology/correct-native.log']),
 'finish':rec(f+'unmasked/native.json','observed in this QEMU run',[f+'unmasked/native.log',f+'unmasked/build.log'],note='Authoritative success uses unmasked/main.c and manifest.json, NOT root-level earlier failed build. Daemon terminated143 by harness; not graceful-stop acceptance.'),
 'stock-build':rec(c+'swap-attempt/outcome.json','observed SDK build only',[c+'swap-attempt/build.log',c+'swap-attempt/service-confirmed.log',c+'swap-attempt/queue-after.log']),
 'oom':rec(c+'diagnosis900/outcome.json','observed historical failure',[c+'diagnosis900/dmesg-after.log',c+'diagnosis900/service-exit.log'],note='No normal build exit survived; null must remain null. No image built.'),
 'old-learner':rec(b+'learner-20261107/parent-review.json','host-only recorded-evidence inspection',[b+'learner-20261107/wrong-native.log',b+'learner-20261107/correct-native.log'],commit='fece07440b019167b0d7449fe1479bbf04001a42',note='Commit explicitly associated in parent review, not in native receipt. Adapted E1/stripped-kernel history, not clean setup.'),
 'host':rec(f+'final-host-receipt.json','host-only',[f+'final-host.log'],commit='cec75567bfd65f02b4afb3ebb674ffe5116906d8'),
 'old-host':rec(c+'parent-review.json','host-only',[c+'parent-host-final.log'],commit='d419bce01d35d3c92ed55b80b7f9faa854cb6ca3'),
 'export':rec(f+'claat-export-receipt.json','host-only',note='Tool and source hash bound; tested commit absent. Current codelab hash compared explicitly. No browser/offline/availability claim.'),
 'qtest':rec('docs/register-qtest-live.txt','observed in this QEMU run',['docs/register-qtest-live.txt'],commit='7afd82275940f45e0b0b0105205a58c255cb713c',note='QEMU-only, no QNX; BASE is recorded, probe and executable hashes in raw log. No OS image.')}
 e['compile']['binary_hashes_from_raw_log']=dict((name,h) for h,name in re.findall(r'^([0-9a-f]{64})  (output/\S+)$',(ROOT/(b+'e2-qcc-20261107/compile.txt')).read_text(),re.M))
 e['export']['current_source_matches_receipt']=sha(ROOT/'codelab/codelab.md')==json.loads((ROOT/e['export']['path']).read_text())['source_sha256']
 # Line-level coverage includes all prose/code, not just a keyword-selected subset.
 sources=[ROOT/'README.md',ROOT/'STATUS.md',ROOT/'REVIEW.md',ROOT/'codelab/codelab.md']+sorted((ROOT/'docs').glob('*.md'))+sorted((ROOT/'steps').glob('**/*.md'))+sorted((ROOT/'docs/acceptance').glob('**/*.md'))
 groups=[('reference',['reference','reference-clean','compile'],r'PCI|BAR|factorial|IAT|Interrupt|IRQ|DMA|resmgr|resource.manager|/dev/edu|STEP[1-6]|step[1-6]'),('clean learner',['step3-wrong','step3-correct','finish','stock-build','oom'],r'learner|clean|swap|stock|Memory fault|sshd'),('host framework',['host','old-host'],r'host|model|test|guard|framework|source.contract|Python|stdlib|dependenc'),('export/site',['export'],r'claat|render|site|SVG|diagram|snapshot'),('register reference',['qtest'],r'qtest|register|QEMU.device')]
 surfaces=[]
 for p in sources:
  rows=[]
  for i,line in enumerate(p.read_text().splitlines(),1):
   if not line.strip():continue
   ids=sorted({key for _,keys,pat in groups if re.search(pat,line,re.I) for key in keys})
   rows.append(dict(line=i,text=line,receipt_paths=[e[k]['path'] for k in ids],evidence_candidates=ids,label='UNVERIFIED unless bounded by REVIEW.md catalog',note='Instruction/planned/expected/source-design text is not runtime proof; candidate references do not assert full sentence acceptance.'))
  surfaces.append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p),lines=rows))
 site=[]
 for p in sorted((ROOT/'docs/site').rglob('*.html')):
  rel=p.relative_to(ROOT/'docs/site'); src=ROOT/rel.with_suffix('.md') if rel.as_posix()!='index.html' else ROOT/'README.md'
  site.append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p),source=str(src.relative_to(ROOT)),coverage='same source line inventory; generated projection, not independent evidence'))
 return dict(schema='qnx-private-review.v1',reviewed_tip='e9174bd73412c98fcf17b40a9e5b6d931ebc4dec',labels=['observed in this QEMU run','host-only','UNKNOWN','UNVERIFIED'],evidence=e,source_surfaces=surfaces,site_projection=site,claim_catalog=dict(path='REVIEW.md',sha256=sha(ROOT/'REVIEW.md')))
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--check',action='store_true');opts=a.parse_args();out=ROOT/'docs/review/appendix.json';value=json.dumps(build(),separators=(',',':'))+'\n'
 if opts.check:
  if not out.exists() or out.read_text()!=value:raise SystemExit('FAIL: stale review appendix')
  print('PASS: review source/site hashes and receipt inventory current (offline inspection only)')
 else:out.write_text(value)
