#!/usr/bin/env python3
"""Offline dry-pack check only: no guests, recording, browser or audio."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/proof-capture'
def sha(b): return hashlib.sha256(b).hexdigest()
def validate(pack):
 errors=[]; lines=[]; previous=0; words=0; seen=set()
 review=(ROOT/'REVIEW.md').read_text()
 for row in pack['lines']:
  ident=row['id']; count=len(row['narration'].split()); words+=count
  if ident in seen: errors.append(ident+': duplicate line')
  seen.add(ident)
  if row['start']!=previous or row['end']<=row['start']: errors.append(ident+': noncontiguous beat')
  previous=row['end']
  if count>3*(row['end']-row['start']): errors.append(ident+': excessive planned speech rate')
  if not row['claim'] or not row['frame'] or not row['assets']: errors.append(ident+': unbound claim/frame')
  if row['review_quote'] not in review: errors.append(ident+': claim boundary missing from REVIEW')
  for asset in row['assets']:
   path=asset['path']; p=ROOT/path
   if p.resolve().is_relative_to(ROOT) is False or not p.is_file(): errors.append(ident+': missing/unsafe asset '+path); continue
   try: frozen=subprocess.check_output(['git','show',asset.get('commit',pack['frozen_commit'])+':'+path],cwd=ROOT,stderr=subprocess.DEVNULL)
   except subprocess.CalledProcessError: errors.append(ident+': asset absent at frozen commit '+path); continue
   if sha(frozen)!=asset['sha256'] or sha(p.read_bytes())!=asset['sha256']: errors.append(ident+': changed frozen asset '+path)
  lines.append({'id':ident,'words':count,'start':row['start'],'end':row['end'],'claim':row['claim'],'frame':row['frame'],'label':row['label'],'assets':row['assets']})
 if previous>=180: errors.append('duration is not under3min')
 if pack.get('recorded') is not False: errors.append('recorded must remain false')
 if pack.get('capture_authorization')!='NOT_GRANTED: separate Olly OK required': errors.append('capture gate invalid')
 return {'kind':'private-proof-capture-DRY-PACK','status':'FAIL' if errors else 'PASS','errors':errors,'frozen_commit':pack['frozen_commit'],'packet_source_commit':pack.get('packet_source_commit',pack['frozen_commit']),'narration_words':words,'planned_seconds':previous,'duration_verified':'editorial plan only; no rehearsal/recorded duration','recorded':False,'recording_performed':False,'audio_performed':False,'publication_performed':False,'claim_mapping_review':'explicit human-authored mapping to REVIEW; hashes check presence/identity, not semantic truth','lines':lines}
def script(pack,report):
 out=['# Private proof-capture DRY PACK', '', 'No recording or audio capture. Separate Olly OK required. No publication/upload authorized.', '', 'Default historical asset binding (not current acceptance): '+pack['frozen_commit'], 'Instruction-copy freeze (not runtime acceptance): '+pack.get('packet_source_commit',pack['frozen_commit']), 'recorded: false; acceptance CONDITIONAL (receipt-inspected, not re-run). Historical receipt source/build pins are unchanged.', 'Exact whitespace narration word count: '+str(report['narration_words'])+'; planned '+str(report['planned_seconds'])+' seconds (not measured).', 'C6 FAIL / STOPPED; SocketCAN UNVERIFIED. Historical native and host-only frames remain separate.', '']
 for x in pack['lines']:
  out.extend(['## '+x['id']+' — '+str(x['start'])+'–'+str(x['end'])+' seconds · '+x['label'],'Claim: '+x['claim'],'Planned frame: '+x['frame'],'Narration: '+x['narration'],'Frozen files: '+', '.join(a['path']+' SHA256 '+a['sha256']+' @ '+a.get('commit',pack['frozen_commit']) for a in x['assets']),'REVIEW boundary: '+x['review_quote'],''])
 return '\n'.join(out)+'\n'
def main():
 print("HISTORICAL diagnostic: original proof/claim pins remain strict; FAIL is not current HOST CI failure. See docs/HISTORICAL-DIAGNOSTICS.md", file=__import__("sys").stderr)
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');args=a.parse_args()
 pack=json.loads((BASE/'pack.json').read_text());report=validate(pack);body=script(pack,report)
 if args.write:
  (BASE/'SCRIPT.md').write_text(body);(BASE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 else:
  if (BASE/'SCRIPT.md').read_text()!=body: report['errors'].append('stale SCRIPT.md')
  if json.loads((BASE/'report.json').read_text())!=validate(pack): report['errors'].append('stale report.json')
 print(json.dumps({'status':'FAIL' if report['errors'] else 'PASS','narration_words':report['narration_words'],'planned_seconds':report['planned_seconds'],'errors':report['errors']}))
 return 1 if report['errors'] else 0
if __name__=='__main__':raise SystemExit(main())
