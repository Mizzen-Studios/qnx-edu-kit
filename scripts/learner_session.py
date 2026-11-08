#!/usr/bin/env python3
"""Local learner notebook; browser never executes commands. CLI wraps learner_lab."""
import argparse
import html
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import time
import uuid
import learner_lab as lab
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
                notes={s:dict.fromkeys(FIELDS, '') for s in ('step3', 'step6')}, attempts=[])
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
    command = [sys.executable, str(ROOT/'scripts/learner_lab.py'), action, '--stage', stage,
               '--source', str(source)]
    if action == 'build':
        command += ['--out',str(work/stage/'bundle'), '--sdp-env',args.sdp_env,
                    '--buildfile',args.buildfile, '--bsp-cwd',args.bsp_cwd]
    else:
        command += ['--bundle',str(work/stage/'bundle'), '--disk',args.disk,
                    '--receipt',str(folder/'native')]
    record = dict(id=ident, stage=stage, action=action, started=time.time(),
                  source_sha256=lab.sha(source), command=command, label='HOST', status='INTERRUPTED')
    data['attempts'].append(record)
    save(work/'session.json', data)
    with (folder/'command.log').open('w') as out:
        result = subprocess.run(command, stdout=out, stderr=subprocess.STDOUT)
    record.update(returncode=result.returncode, finished=time.time(),
                  status='PASS' if result.returncode == 0 else ('BLOCKED' if result.returncode == 2 else 'FAIL'))
    if action == 'build' and result.returncode == 0:
        shutil.copytree(work/stage/'bundle',folder/'bundle')
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
    if any(receipt['checks'].get(k)!=v for k,v in checks.items()):
        raise ValueError('oracle disagrees with receipt')
    expected = all(checks.values()) and all(receipt['checks'].values()) and bool(receipt.get('caps'))
    if receipt['success'] != expected or record['returncode'] != (0 if expected else 1):
        raise ValueError('native status/exit mismatch')
    return bundle, disk


def export(work, dest):
    work, data = session(work)
    dest = lab.external(dest)
    if dest.exists() or dest == work or work in dest.parents:
        raise ValueError('choose a new external export directory outside session')
    dest.mkdir(parents=True)
    try:
        for name in ('session.json','cockpit.html'):
            shutil.copyfile(work/name,dest/name)
        for stage in data['notes']:
            (dest/stage).mkdir()
            shutil.copyfile(work/stage/'main.c',dest/stage/'main.c')
        for record in data['attempts']:
            folder = work/'attempts'/record['id']
            shutil.copytree(folder,dest/'attempts'/record['id'])
            if record['label']=='nativefresh':
                _,disk = validate_native(work,record,folder)
                target = dest/'disks'/lab.sha(disk)
                target.parent.mkdir(exist_ok=True)
                if not target.exists():
                    shutil.copyfile(disk,target)
        files = {str(p.relative_to(dest)):lab.sha(p) for p in sorted(dest.rglob('*')) if p.is_file()}
        save(dest/'pack.json',dict(kind='edu-own-pack-v1',session_id=data['id'], files=files,
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
        cmds = [cmd+' notes'+suffix+' --file /path/to/downloaded-notes.json',
                'flock "$EDU_NATIVE_LOCK" '+cmd+' build'+suffix+' --stage '+stage+' --sdp-env "$EDU_SDP_ENV" --buildfile "$EDU_PLATFORM/output/build/ifs.build" --bsp-cwd "$EDU_PLATFORM"',
                'flock "$EDU_NATIVE_LOCK" env EDU_NATIVE_LOCK="$EDU_NATIVE_LOCK" EDU_NATIVE_LEASE=granted '+cmd+' run'+suffix+' --stage '+stage+' --disk "$EDU_PLATFORM/output/disk-qemu"']
        fields = ''.join('<label>'+key.capitalize()+'<textarea name="'+key+'">'+esc(data['notes'][stage][key])+'</textarea></label>' for key in FIELDS)
        sections.append('<section id="'+stage+'"><h2>'+stage+': '+title+'</h2><p>'+expected+'</p><p>Edit your own source in your editor: <code>'+esc(str(work/stage/'main.c'))+'</code>. Save prediction first; diagnose after observing, then fix, rebuild and explain.</p><form data-stage="'+stage+'">'+fields+'<button>Save local draft</button> <button type="button" data-download="'+stage+'">Download notes for CLI import</button></form><details><summary>Exact build / observe commands</summary><pre>'+esc('\n'.join(cmds))+'</pre></details></section>')
    rows=[]
    for r in data['attempts']:
        base='attempts/'+r['id']+'/'
        links='<a href="'+base+'command.log">command output</a> · <a href="'+base+'main.c">source snapshot</a>'
        if (work/base/'native.json').exists():
            links+=' · <a href="'+base+'native.json">checks / provenance</a> · <a href="'+base+'native.log">raw target log</a>'
        rows.append('<li><strong>'+esc(r['id']+': '+r['status'])+'</strong> ['+esc(r['label'])+']<br>'+links+'</li>')
    seed=json.dumps(dict(id=data['id'])).replace('<',chr(92)+'u003c')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'none'; img-src 'none'; form-action 'none'; base-uri 'none'"><title>Your EDU lab notebook</title><style>
body{margin:0;background:#dae3ed;color:#20374a;font:17px/1.55 'Trebuchet MS',sans-serif}main{max-width:960px;margin:auto;background:#fff;min-height:100vh;padding:clamp(18px,4vw,48px);box-sizing:border-box}h1{font-size:clamp(30px,5vw,48px);line-height:1.1}h2{color:#174b62}section{border-top:4px solid #b9cbd8;padding:24px 0}p{max-width:75ch}label{display:block;margin:16px 0}textarea{display:block;box-sizing:border-box;width:100%;min-height:100px;font:inherit;border:1px solid #58748a;padding:10px}button{background:#174b62;color:white;border:0;border-radius:4px;padding:12px 16px;font:inherit;cursor:pointer;margin:4px 0}a{color:#174b62}a:focus,button:focus,textarea:focus,summary:focus{outline:3px solid #bc6d06;outline-offset:3px}pre,code{overflow-wrap:anywhere;white-space:pre-wrap;font-size:14px}li{margin:18px 0;overflow-wrap:anywhere}.boundary{border-left:5px solid #bc6d06;padding-left:16px}summary{cursor:pointer;padding:12px 0}nav a{display:inline-block;padding:10px}#message{min-height:28px}</style><main><h1>Your EDU lab notebook</h1><p class="boundary">HOST notebook, not native acceptance. Only your CLI build/run can add nativefresh observations. Historical / recorded references cannot complete this notebook. No server, shell console or browser command execution.</p><nav><a href="#step3">BAR read-back</a><a href="#step6">Your /dev/edu</a><a href="#evidence">Evidence</a></nav><p id="message" role="status">Notes save in this browser; download and import them to persist in your evidence pack.</p>'''+''.join(sections)+'<section id="evidence"><h2>Your evidence</h2><p>Failures remain alongside fixes. HOST means command/setup only; nativefresh means this session invoked the native driver with a matching own build, not independent attestation. Editing source invalidates old observations for your current edit.</p><ul>'+(''.join(rows) or '<li>No observations yet. Predict, edit your main.c, then build and observe via CLI.</li>')+'</ul><p>Export locally (includes licensed binary/image/disk if observed; never uploads):</p><pre>'+esc('python3 '+driver+' export --work '+shlex.quote(str(work))+' --out /new/external/private-pack')+'</pre><p>Refresh after CLI commands. No least-privilege, safety, timing, full-platform health, fresh SDK installation or human acceptance claim.</p></section></main><script>const session='+seed+';'+'''
for(const form of document.forms){const key=session.id+':'+form.dataset.stage;try{const saved=JSON.parse(localStorage.getItem(key));if(saved)for(const name of ['prediction','diagnosis','explanation'])form.elements[name].value=saved[name]||'';}catch(e){}const values=()=>Object.assign({session_id:session.id,stage:form.dataset.stage},Object.fromEntries(new FormData(form)));form.addEventListener('submit',e=>{e.preventDefault();try{localStorage.setItem(key,JSON.stringify(values()));document.querySelector('#message').textContent='Local draft saved. Download notes and import with CLI for pack persistence.';}catch(e){document.querySelector('#message').textContent='Browser storage unavailable. Download notes instead.';}});form.querySelector('[data-download]').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(values(),null,2)],{type:'application/json'}));a.download=form.dataset.stage+'-notes.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);document.querySelector('#message').textContent='Notes downloaded. Run the notes import command before building.';};}</script></html>'''
    (work/'cockpit.html').write_text(page)
    return work/'cockpit.html'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='action',required=True)
    for name in ('init','render','notes','build','run','export'):
        s=sub.add_parser(name);s.add_argument('--work',required=True)
        if name=='notes': s.add_argument('--file',required=True)
        if name=='export': s.add_argument('--out',required=True)
        if name in ('build','run'): s.add_argument('--stage',choices=('step3','step6'),required=True)
        if name=='build':
            for opt in ('sdp-env','buildfile','bsp-cwd'): s.add_argument('--'+opt,required=True)
        if name=='run': s.add_argument('--disk',required=True)
    a=p.parse_args()
    try:
        if a.action=='init': print(create(a.work))
        elif a.action=='render': print(render(a.work))
        elif a.action=='notes': notes(a.work,a.file)
        elif a.action=='export': print(export(a.work,a.out))
        else: return attempt(a.work,a.stage,a.action,a)
        return 0
    except (OSError,ValueError,KeyError,subprocess.SubprocessError) as e:
        print('BLOCKED:',e,file=sys.stderr);return 2

if __name__=='__main__': sys.exit(main())
