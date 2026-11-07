#!/usr/bin/env python3
"""Bounded offline claim/link audit; semantic authority is REVIEW, not keyword PASS."""
import argparse,copy,hashlib,importlib.util,json,re,subprocess
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,t,a):self.links.extend(v for k,v in a if k in ('href','src') and v)
def build():
 errors=[];checked=[];surfaces=[]
 paths=[ROOT/'README.md',ROOT/'STATUS.md',ROOT/'REVIEW.md',ROOT/'docs/private-demo.md',ROOT/'docs/proof-capture/SCRIPT.md']
 if (ROOT/'codelab/codelab.md').exists():paths.append(ROOT/'codelab/codelab.md')
 if (ROOT/'docs/site').exists():paths+=sorted((ROOT/'docs/site').rglob('*.html'))
 else:paths += [ROOT/'docs/workbench/index.html',ROOT/'docs/replay/index.html']
 for p in paths:
  if not p.exists():errors.append('missing surface '+str(p));continue
  text=p.read_text();surfaces.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'claim_authority':'REVIEW.md; occurrence inventory and manual bounded claim review, not automatic semantic proof'})
  if p.suffix=='.html':parser=Links();parser.feed(text);links=parser.links
  else:links=re.findall(r'\]\(([^)]+)\)',text)
  for link in links:
   target=link.split('#')[0].split('?')[0]
   if not target or re.match(r'^[a-zA-Z]+:',target) or target.startswith('//'):continue
   # Local fragments are not checked as semantic anchors.
   q=p.parent/target
   if not q.exists():errors.append(str(p.relative_to(ROOT))+': missing local evidence/link '+target)
   checked.append({'source':str(p.relative_to(ROOT)),'target':target,'exists':q.exists()})
 spec=importlib.util.spec_from_file_location('dry',ROOT/'tools/proof_capture.py');dry=importlib.util.module_from_spec(spec);spec.loader.exec_module(dry)
 pack=json.loads((ROOT/'docs/proof-capture/pack.json').read_text());capture=dry.validate(pack);errors+=capture['errors']
 negative={}
 for name in ['unbound_claim','missing_asset','changed_digest']:
  bad=copy.deepcopy(pack)
  if name=='unbound_claim':bad['lines'][0]['claim']=''
  elif name=='missing_asset':bad['lines'][0]['assets'][0]['path']='docs/INTENTIONAL-MISSING-ASSET'
  else:bad['lines'][0]['assets'][0]['sha256']='0'*64
  failure=dry.validate(bad)['errors'];negative[name]={'rejected':bool(failure),'errors':failure}
  if not failure:errors.append('negative check accepted '+name)
 chronology=[]
 for p in sorted((ROOT/'docs/acceptance').rglob('*.json')):
  try:d=json.loads(p.read_text())
  except (ValueError,UnicodeError):continue
  if not isinstance(d,dict):continue
  host=d.get('host_tests',{})
  if isinstance(host,dict) and any(k in host for k in ['total','passed','tests_total']):counts=host
  elif 'tests_total' in d and 'passed' in d:counts={k:d[k] for k in ['tests_total','passed','skipped'] if k in d}
  else:continue
  rel=str(p.relative_to(ROOT))
  chronology.append({'receipt':rel,'sha256':sha(p),'tested_commit':d.get('tested_commit',d.get('source_commit',d.get('source'))),'counts':counts,'scope':'historical host suite at its own revision; never native proof or automatically current count'})
 return {'status':'FAIL' if errors else 'PASS','errors':errors,'scope':'Offline structural lint + explicit REVIEW mapping; not a universal semantic claim verifier','acceptance':'Council CONDITIONAL scoped evidence; native features FROZEN; outsider human learning and second independent SDK UNVERIFIED','capture':'DRY ONLY; separate Olly OK required for recording/audio','boundaries':['existing licensed SDK reused, not fresh install','sshd internal cause UNVERIFIED, no full-platform health','C6FAIL/STOPPED, SocketCANUNVERIFIED','no safety/timing/availability claims'],'surfaces':surfaces,'local_links':checked,'dry_pack':capture,'negative_checks':negative,'chronological_host_receipts':chronology,'chronology_order':'receipt paths; inspect tested commits, not monotonic pass-count progress'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args();d=build();out=ROOT/'docs/claim-lint.json'
 if a.write:out.write_text(json.dumps(d,indent=2)+'\n')
 elif not out.exists() or json.loads(out.read_text())!=d:d['errors'].append('stale claim-lint.json')
 print(json.dumps({'status':'FAIL' if d['errors'] else 'PASS','errors':d['errors'],'surfaces':len(d['surfaces']),'links':len(d['local_links']),'host_receipts':len(d['chronological_host_receipts'])}))
 return 1 if d['errors'] else 0
if __name__=='__main__':raise SystemExit(main())
