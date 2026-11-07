#!/usr/bin/env python3
"""Declared capabilities; this check is NOT new runtime acceptance."""
import argparse, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def render(root=ROOT):
 d=json.loads((root/'docs/capabilities.json').read_text());seen=set()
 if d['schema']!='qnx-capabilities.v1':raise ValueError('unknown schema')
 lines=['# Capability ledger','',d['project'],'',d['boundary'],'','Canonical declarations: docs/capabilities.json. Generated view; ledger checks are not runtime acceptance.','','**Native observations: observed in this QEMU run · app budget, not a QNX benchmark.**','','| Capability | Domain | Level | Status | Bounded claim | Evidence |','|---|---|---|---|---|---|']
 for r in d['rows']:
  if r['id'] in seen or r['domain'] not in ('host','native') or r['status'] not in ('PASS','FAIL','UNVERIFIED'):raise ValueError('invalid/duplicate row')
  seen.add(r['id']);p=(root/r['evidence']).resolve()
  if not p.is_relative_to(root.resolve()) or not p.is_file():raise ValueError('missing/unsafe evidence: '+r['id'])
  if r.get('evidence_sha256') and hashlib.sha256(p.read_bytes()).hexdigest()!=r['evidence_sha256']:raise ValueError('evidence drift: '+r['id'])
  values=[r[k].replace('|','&#124;').replace(chr(10),' ') for k in ('id','domain','level','status','claim')]
  values.append('[source](../'+r['evidence']+')');lines.append('| '+' | '.join(values)+' |')
 return chr(10).join(lines)+chr(10)
def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
 try:
  content=render();dest=ROOT/'docs/capabilities.md'
  if a.write:dest.write_text(content)
  elif not dest.is_file() or dest.read_text()!=content:raise ValueError('stale capability view; use --write')
 except (OSError,KeyError,ValueError) as e:
  print('FAIL: capability ledger: '+str(e),file=sys.stderr);return 1
 print('PASS: capability declarations current; not new runtime proof');return 0
if __name__=='__main__':sys.exit(main())
