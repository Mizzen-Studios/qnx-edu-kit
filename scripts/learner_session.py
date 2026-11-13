#!/usr/bin/env python3
"""Local learner notebook; browser never executes commands. CLI wraps learner_lab."""
import argparse
import html
import hashlib
import fcntl
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import time
import uuid
sys.dont_write_bytecode = True
import learner_lab as lab
import learner_stock as stock
ROOT = Path(__file__).resolve().parents[1]
FIELDS = ('prediction', 'diagnosis', 'explanation')


def save(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2)+'\n')
    temp.replace(path)


def session(work):
    work = lab.external(work)
    data = json.loads((work/'session.json').read_text())
    if data['kind'] != 'edu-own-session-v1':
        raise ValueError('not an own learner session')
    return work, data


def create(work):
    work = lab.external(work)
    if work.exists():
        raise ValueError('choose a new external session directory')
    work.mkdir(parents=True)
    for stage in ('step3', 'step6'):
        lab.init(work/stage, stage)
    data = dict(kind='edu-own-session-v1', id=str(uuid.uuid4()), created=time.time(),
                notes={s:dict.fromkeys(FIELDS, '') for s in ('step3', 'step6', 'permission')}, attempts=[])
    save(work/'session.json', data)
    return render(work)


def notes(work, file):
    work, data = session(work)
    incoming = json.loads(Path(file).read_text())
    if incoming.get('session_id') != data['id']:
        raise ValueError('notes belong to another session')
    stage = incoming.get('stage')
    if stage not in data['notes']:
        raise ValueError('unknown stage')
    for key in FIELDS:
        value = incoming.get(key, '')
        if not isinstance(value, str) or len(value)>20000:
            raise ValueError('invalid note')
        data['notes'][stage][key] = value
    save(work/'session.json', data)
    render(work)


def attempt(work, stage, action, args):
    work, data = session(work)
    if not data['notes'][stage]['prediction'].strip():
        raise ValueError('save a prediction before building or observing')
    ident = f'{len(data["attempts"])+1:04d}-{stage}-{action}'
    folder = work/'attempts'/ident
    folder.mkdir(parents=True)
    source = work/stage/'main.c'
    shutil.copyfile(source, folder/'main.c')
    route = getattr(args, 'stock', None) is not None
    adapter = stock if route else lab
    driver = ROOT/'scripts'/('learner_stock.py' if route else 'learner_lab.py')
    command = [sys.executable, str(driver), action, '--stage', stage,
               '--source', str(source)]
    if route:
        shutil.copyfile(ROOT/'scripts/learner_stock.py',folder/'stock-adapter.py')
        shutil.copyfile(ROOT/'scripts/learner_lab.py',folder/'base-lab-driver.py')
        if action == 'build':
            command += ['--out',str(folder/'bundle'),'--sdp-env',args.sdp_env]
        else:
            prior=next((x for x in reversed(data['attempts']) if x['stage']==stage and x['action']=='build' and x['status']=='PASS' and x.get('route')=='stock-reuse-v1' and x['source_sha256']==lab.sha(source)),None)
            if not prior: raise ValueError('build this own source with stock adapter first')
            command += ['--bundle',str(work/'attempts'/prior['id']/'bundle'),'--stock',args.stock,'--receipt',str(folder/'native'),'--timeout',str(args.timeout)]
            shutil.copyfile(driver,folder/'run-driver.py')
            shutil.copyfile(ROOT/'scripts/stock_console.py',folder/'stock-console.py')
    elif action == 'build':
        command += ['--out',str(work/stage/'bundle'), '--sdp-env',args.sdp_env,
                    '--buildfile',args.buildfile, '--bsp-cwd',args.bsp_cwd]
    else:
        command += ['--bundle',str(work/stage/'bundle'), '--disk',args.disk,
                    '--receipt',str(folder/'native'), '--timeout',str(getattr(args,'timeout',180))]
        shutil.copyfile(ROOT/'scripts/learner_lab.py',folder/'run-driver.py')
    record = dict(id=ident, stage=stage, action=action, started=time.time(),
                  source_sha256=lab.sha(source), command=command, label='HOST', status='INTERRUPTED')
    if route: record['route']='stock-reuse-v1'
    data['attempts'].append(record)
    save(work/'session.json', data)
    with (folder/'command.log').open('w') as out:
        result = subprocess.run(command, stdout=out, stderr=subprocess.STDOUT)
    record.update(returncode=result.returncode, finished=time.time(),
                  status='PASS' if result.returncode == 0 else ('BLOCKED' if result.returncode == 2 else 'FAIL'))
    if action == 'build':
        if not route and (work/stage/'bundle').exists():
            shutil.copytree(work/stage/'bundle',folder/'bundle')
        if result.returncode == 0:
            try:
                adapter.verify_inputs(folder/'main.c',folder/'bundle',stage)
            except (OSError,ValueError,KeyError) as error:
                record.update(status='BLOCKED',validation_error=str(error))
    if action == 'run' and not (folder/'native.json').is_file():
        record.update(status='BLOCKED', validation_error='native receipt absent')
    if action == 'run' and (folder/'native.json').is_file():
        try:
            validate_native(work, record, folder)
            record['label'] = 'nativefresh'
        except (ValueError, KeyError, OSError) as error:
            record.update(status='BLOCKED', validation_error=str(error))
    save(work/'session.json', data)
    render(work)
    return result.returncode if record['status'] != 'BLOCKED' else 2


def validate_native(work, record, folder):
    """Recompute existing oracle and own source/build/disk/log bindings."""
    if record.get("route")=="stock-reuse-v1":
        return validate_stock_native(work,record,folder)
    receipt = json.loads((folder/'native.json').read_text())
    build = next((x for x in reversed(session(work)[1]['attempts'])
                  if x['stage']==record['stage'] and x['action']=='build'
                  and x['status']=='PASS' and x['source_sha256']==record['source_sha256']
                  and x['started'] <= record['started']), None)
    if not build:
        raise ValueError('no own source-bound build for this observation')
    bundle = work/'attempts'/build['id']/'bundle'
    manifest = lab.verify_inputs(folder/'main.c',bundle,record['stage'])
    for key,value in manifest.items():
        if receipt.get(key)!=value:
            raise ValueError('native receipt/build binding mismatch: '+key)
    if lab.sha(folder/'main.c') != record['source_sha256']:
        raise ValueError('attempt source changed')
    command = record['command']
    disk = Path(command[command.index('--disk')+1])
    if lab.sha(disk) != receipt['disk_sha256']:
        raise ValueError('disk changed or missing')
    output = (folder/'native.log').read_text()
    checks = lab.oracle(output,manifest) if record['stage']=='step3' else lab.dev_edu_oracle(output,manifest)
    required = set(checks) | {'bounded_completion','inputs_unchanged_after_boot','disk_unchanged','qemu_reaped'}
    if set(receipt['checks']) != required or any(type(v) is not bool for v in receipt['checks'].values()):
        raise ValueError('native receipt check set invalid')
    driver = folder/'run-driver.py'
    if not driver.exists():
        driver = ROOT/'scripts/learner_lab.py'  # Legacy unchanged-driver receipts only.
    if driver.is_symlink() or receipt.get('run_driver_sha256') != lab.sha(driver):
        raise ValueError('native driver changed or absent')
    if any(receipt['checks'].get(k)!=v for k,v in checks.items()):
        raise ValueError('oracle disagrees with receipt')
    expected = all(checks.values()) and all(receipt['checks'].values()) and bool(receipt.get('caps'))
    if type(receipt.get('success')) is not bool or type(record.get('returncode')) is not int:
        raise ValueError('native status/exit wrong type')
    if receipt['success'] != expected or record['returncode'] != (0 if expected else 1):
        raise ValueError('native status/exit mismatch')
    return bundle, disk


def stock_observed_output(folder):
    observed = json.loads((folder/'native.control/004-observe.result.json').read_text())
    # read_text performs universal-newline conversion; serial evidence must not.
    output = (folder/'native.log').read_bytes().decode('utf-8')
    if observed.get('status') != 'DONE' or observed.get('output') != output:
        raise ValueError('stock log changed')
    return output


def validate_stock_native(work,record,folder):
    receipt=json.loads((folder/'native.json').read_text())
    prior=next((x for x in reversed(session(work)[1]['attempts']) if x['action']=='build' and x['stage']==record['stage'] and x['status']=='PASS' and x.get('route')=='stock-reuse-v1' and x['source_sha256']==record['source_sha256'] and x['started']<=record['started']),None)
    if not prior: raise ValueError('no own stock build for this source')
    bundle=work/'attempts'/prior['id']/'bundle';m=stock.verify_inputs(folder/'main.c',bundle,record['stage'])
    if any(receipt.get(k)!=v for k,v in m.items()): raise ValueError('stock build/receipt mismatch')
    command=record['command'];root=Path(command[command.index('--stock')+1]);assets=stock.stock_inputs(root)
    if assets!=receipt.get('stock_assets'): raise ValueError('stock artifact binding mismatch')
    if lab.sha(folder/'run-driver.py')!=receipt['run_driver_sha256'] or lab.sha(folder/'stock-console.py')!=receipt['console_driver_sha256']: raise ValueError('stock drivers changed')
    control=folder/'native.control';owner=json.loads((control/'owner-final.json').read_text())
    if owner.get('caps')!=receipt.get('caps'): raise ValueError('stock caps changed')
    if owner!=receipt.get('owner'): raise ValueError('stock owner evidence changed')
    output=stock_observed_output(folder)
    checked=stock.checks(output,m,control,owner)
    checked['inputs_unchanged_after_boot']=stock.verify_inputs(folder/'main.c',bundle,record['stage'])==m and stock.stock_inputs(root)==assets
    if checked!=receipt.get('checks'): raise ValueError('stock oracle disagrees')
    success=all(checked.values()) and bool(owner.get('caps')) and receipt.get('error') is None
    if type(receipt.get('success')) is not bool or receipt['success']!=success or record['returncode']!=(0 if success else 1): raise ValueError('stock status/exit mismatch')
    return bundle,Path(assets['disk-qemu']['path'])


def revalidate(work, ident):
    """Offline recovery of an own stock observation rejected by host validation.

    Never invokes a guest, changes raw receipts, imports evidence or changes
    source identity. Preserve the pre-recovery notebook inside the export.
    """
    work, data = session(work)
    record = next((r for r in data['attempts'] if r['id'] == ident), None)
    if (record is None or record.get('route') != 'stock-reuse-v1'
            or record.get('action') != 'run' or record.get('status') != 'BLOCKED'
            or type(record.get('returncode')) is not int
            or record['returncode'] not in (0, 1) or not record.get('validation_error')):
        raise ValueError('requires own blocked stock observation with completed driver')
    candidate = dict(record, status='PASS' if record['returncode'] == 0 else 'FAIL', label='nativefresh')
    candidate.pop('validation_error')
    validate_attempt(work, candidate, work/'attempts'/ident)
    before = (work/'session.json').read_bytes()
    archive = work/'supplemental'/('before-revalidation-'+hashlib.sha256(before).hexdigest()+'.json')
    archive.parent.mkdir(exist_ok=True)
    archive.write_bytes(before)
    candidate['offline_revalidation'] = dict(at=time.time(), previous_error=record['validation_error'],
                                             validator_sha256=lab.sha(__file__), archive=str(archive.relative_to(work)))
    record.clear(); record.update(candidate)
    save(work/'session.json', data)
    render(work)
    return candidate['status']


def source_state(work, data):
    """Historical outcomes are immutable; current validation is source-bound."""
    result = {}
    for stage in ('step3', 'step6'):
        digest = lab.sha(work/stage/'main.c')
        matched = any(r['stage'] == stage and r['action'] == 'run'
                      and r['status'] == 'PASS' and r['label'] == 'nativefresh'
                      and r['source_sha256'] == digest for r in data['attempts'])
        result[stage] = dict(source_sha256=digest,
                            validation='CURRENT_SOURCE_RECORDED_PASS' if matched else 'CURRENT_STAGE_NOT_VALIDATED')
    return result


def validate_attempt(work, record, folder):
    """Validate by operation and artifacts, never use a display label as a gate."""
    action, status = record['action'], record['status']
    if action not in ('build', 'run') or record['stage'] not in ('step3', 'step6'):
        raise ValueError('invalid attempt action/stage')
    if status not in ('PASS', 'FAIL', 'BLOCKED', 'INTERRUPTED'):
        raise ValueError('invalid attempt status')
    if lab.sha(folder/'main.c') != record['source_sha256']:
        raise ValueError('attempt source changed')
    rc = record.get('returncode')
    if status != 'INTERRUPTED' and (type(rc) is not int or (status == 'PASS' and rc != 0)
                                         or (status == 'FAIL' and rc != 1)):
        raise ValueError('attempt status/exit mismatch')
    if status == 'INTERRUPTED' and rc is not None:
        raise ValueError('interrupted attempt has final exit status')
    has_native = any((folder/name).exists() for name in ('native.json', 'native.log'))
    disk = None
    if action == 'build':
        if has_native or record['label'] != 'HOST':
            raise ValueError('build action/label/assets mismatch')
        if status == 'PASS':
            if record.get('returncode') != 0:
                raise ValueError('build status/exit mismatch')
            (stock if record.get('route')=='stock-reuse-v1' else lab).verify_inputs(folder/'main.c', folder/'bundle', record['stage'])
        elif status == 'FAIL' and record.get('returncode') != 1:
            raise ValueError('build status/exit mismatch')
    elif has_native:
        _, disk = validate_native(work, record, folder)
        expected = 'PASS' if record['returncode'] == 0 else 'FAIL'
        if record['label'] != 'nativefresh' or status != expected:
            raise ValueError('native action/label/status mismatch')
    elif record['label'] != 'HOST' or status not in ('BLOCKED', 'INTERRUPTED'):
        raise ValueError('run without native evidence cannot claim an observation')
    return disk


def export(work, dest):
    work, data = session(work)
    dest = lab.external(dest)
    if dest.exists() or dest == work or work in dest.parents:
        raise ValueError('choose a new external export directory outside session')
    dest.mkdir(parents=True)
    try:
        render(work)
        for name in ('session.json','cockpit.html'):
            shutil.copyfile(work/name,dest/name)
        for stage in ('step3','step6'):
            (dest/stage).mkdir()
            shutil.copyfile(work/stage/'main.c',dest/stage/'main.c')
        for record in data['attempts']:
            folder = work/'attempts'/record['id']
            disk = validate_attempt(work, record, folder)
            shutil.copytree(folder,dest/'attempts'/record['id'])
            if record.get('route')=='stock-reuse-v1' and (folder/'native.json').exists():
                receipt=json.loads((folder/'native.json').read_text())
                for name,asset in receipt['stock_assets'].items():
                    target=dest/'stock-artifacts'/name;target.parent.mkdir(exist_ok=True)
                    if not target.exists(): shutil.copyfile(asset['path'],target)
            if disk is not None and record.get('route')!='stock-reuse-v1':
                target = dest/'disks'/lab.sha(disk)
                target.parent.mkdir(exist_ok=True)
                if not target.exists():
                    shutil.copyfile(disk,target)
        if (work/'supplemental').is_dir():
            if (work/'supplemental').is_symlink() or any(p.is_symlink() for p in (work/'supplemental').rglob('*')):
                raise ValueError('supplemental symlinks unsupported')
            shutil.copytree(work/'supplemental',dest/'supplemental',symlinks=False)
        files = {str(p.relative_to(dest)):lab.sha(p) for p in sorted(dest.rglob('*')) if p.is_file()}
        save(dest/'pack.json',dict(kind='edu-own-pack-v1',session_id=data['id'], files=files, current_sources=source_state(work, data),
             reference_imports='unsupported; recorded reference is not learner work',
             privacy='Local licensed artifacts. Review licences before sharing. No upload provided.'))
    except BaseException:
        (dest/'INCOMPLETE.txt').write_text('Export failed; not a complete evidence pack.\n')
        raise
    return dest/'pack.json'


def render(work):
    work,data = session(work)
    esc = html.escape
    sections = []
    driver = shlex.quote(str(ROOT/'scripts/learner_session.py'))
    for stage,title,expected in [('step3','BAR read-back','Wrong write12345679 must FAIL despite app exit0; fix12345678 to read edcba987.'),
                                  ('step6','Your /dev/edu','Normal write10 to read3628800; separate IRQ completion1 and ack00000000 required.')]:
        cmd = 'python3 '+driver
        suffix = ' --work '+shlex.quote(str(work))
        cmds = ['# Working stock route: docs/learner-route.md and docs/coherent-journey.md',
                '# ADVANCED LAB: existing licensed SDP, exclusive SDK/QEMU lease, approved stock IFS/disk handoff.',
                '# HOST notes only; import before building:',
                cmd+' notes'+suffix+' --file /path/to/downloaded-notes.json',
                '# SDK GUEST namespace: EDU_GUEST_SOURCE=$EDU_GUEST_WORK/'+stage+'/main.c',
                'python3 "$EDU_GUEST_REPO/scripts/learner_session.py" build --work "$EDU_GUEST_WORK" --stage '+stage+' --stock approved-stock-reuse --sdp-env "$EDU_SDP_ENV"',
                '# STOP/REAP SDK and verify actual lease FREE; then HOST ONLY.',
                '# HOST namespace: EDU_HOST_SOURCE=$EDU_WORK/'+stage+'/main.c',
                'env EDU_NATIVE_LEASE=granted '+cmd+' run'+suffix+' --stage '+stage+' --stock "$EDU_STOCK" --timeout 600',
                '# Step3: observe wrong FAIL/app0 BEFORE creating corrected source, then rebuild and run.',
                '# Complete same-session step6, then export and validate aggregate (no receipt imports):',
                cmd+' export'+suffix+' --out /new/external/stock-own-export',
                'python3 "$EDU_REPO/scripts/learner_journey.py"'+suffix+' --export /new/external/stock-own-export --tested-commit "$EDU_TESTED_COMMIT" --out /new/external/journey.json',
                '# Historical CUSTOM-IFS route: docs/learner-route-custom-legacy.md; not these stock commands.',
                '# Standalone split receipts are not imported notebook attempts.']
        fields = ''.join('<label>'+key.capitalize()+'<textarea aria-label="'+key.capitalize()+'" name="'+key+'">'+esc(data['notes'][stage][key])+'</textarea></label>' for key in FIELDS)
        sections.append('<section id="'+stage+'"><h2>'+stage+': '+title+'</h2><p>'+expected+'</p><p>Edit your own source in your editor: <code>'+esc(str(work/stage/'main.c'))+'</code>. Save prediction first; diagnose after observing, then fix, rebuild and explain.</p><form data-stage="'+stage+'">'+fields+'<button>Save local draft</button> <button type="button" data-download="'+stage+'">Download notes for CLI import</button></form><details><summary>Split-host handoff — not a current execution</summary><pre>'+esc('\n'.join(cmds))+'</pre></details></section>')
    permission=data['notes'].get('permission',dict.fromkeys(FIELDS,''))
    fields=''.join('<label>'+key.capitalize()+'<textarea aria-label="'+key.capitalize()+'" name="'+key+'">'+esc(permission[key])+'</textarea></label>' for key in FIELDS)
    sections.append('<section id="permission"><h2>Ability-only permission experiment</h2><p>Supplemental notes only; not pathname policy or a native acceptance badge. Run the same ability_lesson ELF in separate deny/allow processes; IO subrange0..0, not default root. Preserve errno/transcripts and source/ELF/image/disk lineage. See docs/ability-lesson.md in your checkout.</p><form data-stage="permission">'+fields+'<button>Save local draft</button> <button type="button" data-download="permission">Download notes for CLI import</button></form></section>')
    current = source_state(work, data)
    rows=[]
    for r in data['attempts']:
        base='attempts/'+r['id']+'/'
        links='<a href="'+base+'command.log">command output</a> · <a href="'+base+'main.c">source snapshot</a>'
        if (work/base/'native.json').exists():
            links+=' · <a href="'+base+'native.json">checks / provenance</a> · <a href="'+base+'native.log">raw target log</a>'
        match = r['source_sha256'] == current[r['stage']]['source_sha256']
        qualification = 'source matches current edit' if match else 'HISTORICAL — SOURCE MISMATCH; current edit not validated by this attempt'
        rows.append('<li><strong>'+esc(r['id']+': '+r['status'])+'</strong> ['+esc(r['label'])+'] — '+qualification+'<br>'+links+'</li>')
    rows.insert(0, '<li>'+esc('; '.join(stage+': '+value['validation'] for stage,value in current.items()))+'</li>')
    revisions = {stage: hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest() for stage,value in data['notes'].items()}
    seed=json.dumps(dict(id=data['id'], notes_revisions=revisions)).replace('<',chr(92)+'u003c')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'none'; img-src 'none'; form-action 'none'; base-uri 'none'"><title>Your EDU lab notebook</title><style>
body{margin:0;background:#dae3ed;color:#20374a;font:17px/1.55 'Trebuchet MS',sans-serif}main{max-width:960px;margin:auto;background:#fff;min-height:100vh;padding:clamp(18px,4vw,48px);box-sizing:border-box}h1{font-size:clamp(30px,5vw,48px);line-height:1.1}h2{color:#174b62}section{border-top:4px solid #b9cbd8;padding:24px 0}p{max-width:75ch}label{display:block;margin:16px 0}textarea{display:block;box-sizing:border-box;width:100%;min-height:100px;font:inherit;border:1px solid #58748a;padding:10px}button{background:#174b62;color:white;border:0;border-radius:4px;padding:12px 16px;font:inherit;cursor:pointer;margin:4px 0}a{color:#174b62}a:focus,button:focus,textarea:focus,summary:focus{outline:3px solid #bc6d06;outline-offset:3px}pre,code{overflow-wrap:anywhere;white-space:pre-wrap;font-size:14px}li{margin:18px 0;overflow-wrap:anywhere}.boundary{border-left:5px solid #bc6d06;padding-left:16px}summary{cursor:pointer;padding:12px 0}nav a{display:inline-block;padding:10px}#message{min-height:28px}</style><main><h1>Your EDU lab notebook</h1><p class="boundary">Supported topology: split-host SDK guest build → STOP/REAP guest → capped HOST QEMU. Advanced lab: existing licensed SDP, exclusive SDK/QEMU lease and approved stock IFS/disk handoff required. HOST notebook, not native acceptance. Single-host BLOCKED_NATIVE_TIMEOUT; root cause UNVERIFIED. Follow docs/learner-route.md in your checkout. No current native execution is claimed. Historical / recorded references cannot complete this notebook. No server, shell console or browser command execution.</p><nav><a href="#step3">BAR read-back</a><a href="#step6">Your /dev/edu</a><a href="#evidence">Evidence</a></nav><p id="message" role="status">Notes save in this browser; download and import them to persist in your evidence pack.</p>'''+''.join(sections)+'<section id="evidence"><h2>Your evidence</h2><p>Failures remain alongside fixes. HOST means command/setup only; nativefresh means this session invoked the native driver with a matching own build, not independent attestation. Editing source invalidates old observations for your current edit.</p><ul>'+(''.join(rows) or '<li>No observations yet. Predict, edit your main.c, then build and observe via CLI.</li>')+'</ul><p>Export HOST notes and any actual notebook-owned attempts locally (standalone split receipts require their separately labeled pack; never uploads):</p><pre>'+esc('python3 '+driver+' export --work '+shlex.quote(str(work))+' --out /new/external/private-pack')+'</pre><p>Refresh after CLI commands. No least-privilege, safety, timing, full-platform health, fresh SDK installation or human acceptance claim.</p></section></main><script>const session='+seed+';'+'''
for(const form of document.forms){
 const key=session.id+':'+form.dataset.stage, revision=session.notes_revisions[form.dataset.stage];
 const names=['prediction','diagnosis','explanation'];
 const values=()=>Object.assign({session_id:session.id,stage:form.dataset.stage},Object.fromEntries(new FormData(form)));
 let conflict=null;
 try{const saved=JSON.parse(localStorage.getItem(key));if(saved){
  const draft=saved.notes||saved;
  const same=names.every(name=>(draft[name]||'')===form.elements[name].value);
  if(saved.base_revision===revision){for(const name of names)form.elements[name].value=draft[name]||'';}
  else if(same){localStorage.removeItem(key);}
  else{
   conflict=document.createElement('p');conflict.setAttribute('role','alert');
   conflict.textContent='Draft conflict: authoritative CLI notes changed (or draft has no revision). CLI notes are shown. Choose restore or discard before downloading or saving.';
   for(const [label,restore] of [['Restore conflicting draft',true],['Discard conflicting draft',false]]){
    const button=document.createElement('button');button.type='button';button.textContent=label;
    button.onclick=()=>{if(restore){for(const name of names)form.elements[name].value=draft[name]||'';localStorage.setItem(key,JSON.stringify({base_revision:revision,notes:values()}));}else localStorage.removeItem(key);conflict.remove();conflict=null;};conflict.append(button);
   }form.append(conflict);
  }
 }}catch(e){}
 form.addEventListener('submit',e=>{e.preventDefault();if(conflict)return;try{localStorage.setItem(key,JSON.stringify({base_revision:revision,notes:values()}));document.querySelector('#message').textContent='Local draft saved. Download notes and import with CLI for pack persistence.';}catch(e){document.querySelector('#message').textContent='Browser storage unavailable. Download notes instead.';}});
 form.querySelector('[data-download]').onclick=()=>{if(conflict)return;const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(values(),null,2)],{type:'application/json'}));a.download=form.dataset.stage+'-notes.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);document.querySelector('#message').textContent='Notes downloaded. Run the notes import command before building.';};
}</script></html>'''
    (work/'cockpit.html').write_text(page)
    return work/'cockpit.html'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='action',required=True)
    for name in ('init','render','notes','build','run','export','revalidate'):
        s=sub.add_parser(name);s.add_argument('--work',required=True)
        if name=='notes': s.add_argument('--file',required=True)
        if name=='export': s.add_argument('--out',required=True)
        if name=='revalidate': s.add_argument('--attempt',required=True)
        if name in ('build','run'):
            s.add_argument('--stage',choices=('step3','step6'),required=True)
            s.add_argument('--stock',help='explicit approved stock directory; selects distinct stock adapter')
        if name=='build':
            s.add_argument('--sdp-env',required=True)
            for opt in ('buildfile','bsp-cwd'): s.add_argument('--'+opt)
        if name=='run':
            s.add_argument('--disk')
            s.add_argument('--timeout',type=int,default=180)
    a=p.parse_args()
    try:
        if a.action=='init': print(create(a.work))
        elif a.action=='render': print(render(a.work))
        elif a.action=='notes': notes(a.work,a.file)
        elif a.action=='export': print(export(a.work,a.out))
        else:
            work,_ = session(a.work)
            with (work/'session.lock').open('a') as lock:
                try:
                    fcntl.flock(lock,fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    raise ValueError('another session action is active')
                if a.action == 'revalidate':
                    print(revalidate(work, a.attempt)); return 0
                return attempt(work,a.stage,a.action,a)
        return 0
    except (OSError,ValueError,KeyError,subprocess.SubprocessError) as e:
        print('BLOCKED:',e,file=sys.stderr);return 2

if __name__=='__main__': sys.exit(main())
