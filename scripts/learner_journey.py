#!/usr/bin/env python3
"""Offline aggregate for one notebook's stock wrong/correct/finish journey."""
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
import learner_session as notebook
import learner_stock as stock
import learner_lab as lab
ROOT = Path(__file__).resolve().parents[1]

def chain(phases):
    if [p['stage'] for p in phases] != ['step3', 'step3', 'step6']:
        raise ValueError('requires exactly wrong step3, corrected step3, finish step6')
    wrong, correct, finish = phases
    if [p['status'] for p in phases] != ['FAIL', 'PASS', 'PASS']:
        raise ValueError('wrong/correct/finish outcomes required')
    if {k for k,v in wrong['checks'].items() if v is not True} != {'device_readback'}:
        raise ValueError('wrong phase must fail only intended readback, not setup/logging/exit')
    if wrong['mmio'] != [('010000ed','12345679','edcba986')]:
        raise ValueError('wrong actual MMIO required')
    for p in (correct,finish):
        if not p['checks'] or not all(v is True for v in p['checks'].values()):
            raise ValueError('correct and finish checks must all pass')
    if correct['source_sha256'] == wrong['source_sha256']:
        raise ValueError('corrected source must differ')
    if correct['build_started'] <= wrong['finished']:
        raise ValueError('corrected build must follow actual wrong observation')
    if correct['started'] <= wrong['finished'] or finish['started'] <= correct['finished']:
        raise ValueError('observations must be sequential')
    if len({(p['image_sha256'],p['disk_sha256']) for p in phases}) != 1:
        raise ValueError('shared stock artifacts required')
    return True

def validate_export_inventory(work,data,exported,pack):
    if (exported/'INCOMPLETE.txt').exists(): raise ValueError('incomplete export')
    expected={name:lab.sha(work/name) for name in ('session.json','cockpit.html','step3/main.c','step6/main.c')}
    for record in data['attempts']:
        folder=work/'attempts'/record['id']
        for file in folder.rglob('*'):
            if file.is_symlink(): raise ValueError('symlink attempt evidence')
            if file.is_file(): expected[str(file.relative_to(work))]=lab.sha(file)
        if (folder/'native.json').is_file():
            r=json.loads((folder/'native.json').read_text());identity=r.get('stock_owner_sha256')
            prefix=Path('stock-artifacts')/identity if identity else Path('stock-artifacts')
            for name,asset in r['stock_assets'].items(): expected[str(prefix/name)]=asset['sha256']
            if identity:
                root=Path(r['stock_assets']['ifs.bin']['path']).parent
                for name in ('stock-build.json','stock-owner.json','build.private.log','tool-versions.private.log','build-start.json'): expected[str(prefix/name)]=lab.sha(root/name)
    if (work/'supplemental').is_dir():
        for file in (work/'supplemental').rglob('*'):
            if file.is_file(): expected[str(file.relative_to(work))]=lab.sha(file)
    actual={str(f.relative_to(exported)) for f in exported.rglob('*') if f.is_file() and f!=exported/'pack.json'}
    if actual!=set(expected) or pack.get('files')!=expected: raise ValueError('incomplete/mixed export inventory')
    return True

def aggregate(work, exported, commit):
    if not re.fullmatch('[0-9a-f]{40}',commit): raise ValueError('exact tested commit required')
    work,data=notebook.session(work); exported=lab.external(exported)
    frozen=lambda name:subprocess.check_output(['git','show',commit+':scripts/'+name],cwd=ROOT)
    if hashlib.sha256(frozen('learner_journey.py')).hexdigest()!=lab.sha(__file__):
        raise ValueError('aggregate validator must match tested source commit')
    runs=[];builds=[];admitted=[]
    for record in data['attempts']:
        folder=work/'attempts'/record['id']
        if record.get('route')!='stock-reuse-v1': raise ValueError('only own stock attempts accepted')
        notebook.validate_attempt(work,record,folder)
        for name,original in [('stock-adapter.py','learner_stock.py'),('base-lab-driver.py','learner_lab.py')]:
            if (folder/name).read_bytes()!=frozen(original): raise ValueError('attempt driver differs from tested commit')
        if record['action']=='build':
            if record['status']!='PASS':raise ValueError('all three own builds must pass')
            builds.append(record);continue
        for name,original in [('run-driver.py','learner_stock.py'),('stock-console.py','stock_console.py')]:
            if (folder/name).read_bytes()!=frozen(original):raise ValueError('runtime driver differs from tested commit')
        r=json.loads((folder/'native.json').read_text());admitted.append((r.get('stock_admission'),r.get('stock_owner_sha256'),{k:v['sha256'] for k,v in r['stock_assets'].items()}));log=notebook.stock_observed_output(folder)
        build=next((b for b in reversed(builds) if b['stage']==record['stage'] and b['source_sha256']==record['source_sha256']),None)
        if not build: raise ValueError('own preceding build required')
        runs.append(dict(stage=record['stage'],status=record['status'],attempt=record['id'],build_attempt=build['id'],
            started=record['started'],finished=record['finished'],build_started=build['started'],
            source_sha256=r['source_sha256'],object_sha256=r['object_sha256'],binary_sha256=r['binary_sha256'],
            image_sha256=r['image_sha256'],disk_sha256=r['disk_sha256'],checks=r['checks'],
            native_receipt_sha256=lab.sha(folder/'native.json'),native_log_sha256=lab.sha(folder/'native.log'),
            mmio=re.findall(r'^LEARNER_MMIO id=([0-9a-f]{8}) write=([0-9a-f]{8}) read=([0-9a-f]{8})$',log.replace('\r',''),re.M)))
    if len(data['attempts'])!=6 or len(builds)!=3:raise ValueError('one journey requires three builds and three observations')
    chain(runs)
    if any(a!=admitted[0] for a in admitted): raise ValueError('mixed platform admission identities')
    pack=json.loads((exported/'pack.json').read_text())
    if pack['session_id']!=data['id'] or (exported/'session.json').read_bytes()!=(work/'session.json').read_bytes():
        raise ValueError('export must belong to same unchanged own notebook')
    validate_export_inventory(work,data,exported,pack)
    for name,digest in pack['files'].items():
        p=exported/name
        if not p.resolve().is_relative_to(exported) or lab.sha(p)!=digest:raise ValueError('export hash mismatch')
    if pack['current_sources']!=notebook.source_state(work,data) or any(v['validation']!='CURRENT_SOURCE_RECORDED_PASS' for v in pack['current_sources'].values()):
        raise ValueError('both current own sources must be validated')
    return dict(kind='edu-coherent-own-stock-journey-v1',status='PASS',tested_source_commit=commit,session_id=data['id'],
        phases=runs,stock_pins=admitted[0][2],export_pack_sha256=lab.sha(exported/'pack.json'),export_files=len(pack['files']),
        current_sources=pack['current_sources'],image_generation=admitted[0][0]=='independent-cooperative-v1',stock_admission=admitted[0][0] or 'historical-pinned-reuse',stock_owner_sha256=admitted[0][1],
        scope='One automated own notebook, three fresh stock observations; existing legal SDK. Platform admission identity reported separately. Not independent human/fresh-install/all-six-stage acceptance.')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('work','export','tested-commit','out'):p.add_argument('--'+n,required=True)
    a=p.parse_args();out=lab.external(a.out)
    try:
        if out.exists():raise ValueError('fresh aggregate receipt required')
        result=aggregate(a.work,a.export,a.tested_commit);out.write_text(json.dumps(result,indent=2)+'\n');print('OWN_JOURNEY_VERIFIED',out);return 0
    except (OSError,ValueError,KeyError,subprocess.SubprocessError) as e:print('BLOCKED:',e,file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
