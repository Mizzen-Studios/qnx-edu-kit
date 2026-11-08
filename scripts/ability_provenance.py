#!/usr/bin/env python3
"""Offline typed ability evidence validator; shared CAN success is never ability PASS."""
import argparse
import hashlib
import json
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def validate(folder):
    folder = Path(folder)
    receipt = json.loads((folder/'receipt.json').read_text())
    meta = json.loads((folder/'provenance.json').read_text())
    run = json.loads((folder/'run.json').read_text())
    if meta.get('schema') != 'edu-ability-shared-run-v1' or meta.get('evidence_type') != 'ability-only-observation':
        raise ValueError('wrong ability provenance type')
    if meta.get('shared_run_type') != 'canopy-incident-capture' or meta.get('shared_success_scope') != 'CAN restart/traffic only; NOT ability acceptance':
        raise ValueError('shared success scope invalid')
    for name,key in [('run.json','shared_run_sha256'),('native-transcript.txt','mixed_transcript_sha256')]:
        if sha(folder/name) != meta.get(key): raise ValueError('changed shared evidence: '+name)
    if meta.get('transcript_scope') != 'mixed containment, ability and CAN slog2; not a full boot log':
        raise ValueError('transcript scope invalid')
    if type(receipt.get('ability_only')) is not bool or receipt['ability_only'] is not True or receipt.get('same_elf_separate_processes') is not True:
        raise ValueError('ability receipt type invalid')
    if receipt.get('run') != run.get('run_id') or receipt.get('run') != meta.get('run_id'):
        raise ValueError('run identity mismatch')
    for key in ('image_sha256','disk_sha256'):
        if receipt.get(key) != run.get(key): raise ValueError('shared binding mismatch: '+key)
    if sha(ROOT/'native/ability_lesson.c') != receipt.get('source_sha256'): raise ValueError('ability source mismatch')
    if not re.fullmatch('[0-9a-f]{64}',receipt.get('same_elf_sha256','')): raise ValueError('ELF digest missing')
    if meta.get('elf_binding_scope') != 'same ELF digest recorded in original ability receipt; shared run metadata does not independently bind this ELF':
        raise ValueError('ELF scope invalid')
    text = (folder/'native-transcript.txt').read_bytes().decode().replace(chr(13),'')
    expected = [('deny','none',-1,1),('allow','0-0',0,0)]
    for mode,subrange,rc,errno in expected:
        values = receipt.get(mode,{})
        if any(type(values.get(k)) is not int for k in ('rc','errno','process_exit')): raise ValueError('wrong type in ability result')
        if (values['rc'],values['errno'],values['process_exit']) != (rc,errno,0): raise ValueError('unexpected ability result')
        line = f'ABILITY_LESSON mode={mode} io_subrange={subrange} others=deny-lock operation=IO_LEVEL_1 rc={rc} errno={errno}'
        if text.splitlines().count(line) != 1 or text.splitlines().count(f'ABILITY_{mode.upper()}_RC=0') != 1:
            raise ValueError('ability transcript mismatch')
    events = [x for x in text.splitlines() if x.startswith(('ABILITY_LESSON ', 'ABILITY_DENY_RC=', 'ABILITY_ALLOW_RC='))]
    if len(events)!=4 or not events[0].startswith('ABILITY_LESSON mode=deny ') or not events[2].startswith('ABILITY_LESSON mode=allow '): raise ValueError('ability event ordering invalid')
    return dict(status='PASS',scope='offline ability evidence validation; NOT new native execution',shared_run_success_not_consumed=True,run_id=run['run_id'])
if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',nargs='?',default=ROOT/'docs/acceptance/ability-20261108');a=p.parse_args()
    try: print(json.dumps(validate(a.folder)))
    except (OSError,ValueError,KeyError,TypeError) as e: p.exit(2,'BLOCKED: '+str(e)+chr(10))
