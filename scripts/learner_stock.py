#!/usr/bin/env python3
"""Own stock-route adapter: fresh application build, explicitly reused stock image."""
import argparse,hashlib,json,os,re,subprocess,sys,time
from pathlib import Path
sys.dont_write_bytecode = True
import learner_lab as lab
ROOT=Path(__file__).resolve().parents[1]
PINS={'ifs.bin':'68bbe1b49a9b723c09d152773ee323ec6ab576eb29de933bfe3f08fdae21c753','disk-qemu':'0aee00c281f8eeb5b02c66555ed9517e317bb1503002a19dbf2b0155de336532','qemu_options':'f72b3d8f85b7f82f03c8572d10369a212ef87dfd322c0cc882ed441261d770df','options':'340ec003fd11044e6eea2d2e39eae00f024bfc483b70dc05cb1cc239a06665f5','disk-qemu.vmdk':'1d01efe9cc8d4a418416d50fac0b2dc8f12100ac2912a1418286e1169528576e'}
def save(p,data): Path(p).write_text(json.dumps(data,indent=2))
def kind(stage):
    lab.manifest_kind(stage)
    return 'learner-stock-'+stage+'-v1'
def stock_inputs(stock, provenance=None, owner_sha256=None):
    if provenance is not None:
        if provenance!='independent-cooperative-v1': raise ValueError('unsupported stock admission')
        import stock_provenance as fresh
        m=fresh.verify(stock,owner_sha256=owner_sha256)
        return {n:{'path':str(fresh.external(stock)/n),'sha256':d} for n,d in m['artifacts'].items()}
    stock=lab.external(stock)
    # Exact reviewed artifacts only: never relabel an arbitrary custom IFS as stock.
    result={}
    for name,digest in PINS.items():
        p=stock/name
        if not p.is_file() or p.is_symlink() or lab.sha(p)!=digest: raise ValueError('unapproved stock artifact: '+name)
        result[name]={'path':str(p),'sha256':digest}
    return result

def build(source,out,env,stage):
    source=Path(source).resolve();out=lab.external(out)
    if out.exists(): raise ValueError('new stock build directory required')
    out.mkdir(parents=True);snap=out/'learner-source.c';snap.write_bytes(source.read_bytes())
    obj=out/'learner.o';binary=out/'learner_bin'
    for phase,action,a,b in [('compile','qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g0 -Wall -Wextra -Wno-unused-variable -c "$3" -o "$2"',obj,snap),('link','qcc -Vgcc_ntox86_64 -o "$2" "$3" -lpci -lslog2',binary,obj)]:
        subprocess.run(['bash','-c',lab.measured_shell(action),'stock-'+phase,str(Path(env).resolve()),str(a),str(b)],check=True)
    if not binary.read_bytes().startswith(bytes([127,69,76,70])): raise ValueError('not ELF')
    if lab.sha(source)!=lab.sha(snap): raise ValueError('source changed during compile')
    m=dict(kind=kind(stage),route='stock-reuse-v1',observability='pulse-slog2-v1' if stage=='step6' else 'slog2-v1',source_sha256=lab.sha(snap),object_sha256=lab.sha(obj),binary_sha256=lab.sha(binary),built_at=time.time(),build_sequence=['compile -O0 -g0','link'],image_generation=False,build_driver_sha256=lab.sha(__file__))
    save(out/'manifest.json',m);return m

def verify_inputs(source,bundle,stage):
    bundle=lab.external(bundle);m=json.loads((bundle/'manifest.json').read_text())
    if m.get('kind')!=kind(stage) or m.get('route')!='stock-reuse-v1' or m.get('image_generation') is not False: raise ValueError('not a distinct stock application build')
    for p,k in [(Path(source),'source_sha256'),(bundle/'learner-source.c','source_sha256'),(bundle/'learner.o','object_sha256'),(bundle/'learner_bin','binary_sha256')]:
        if p.is_symlink() or lab.sha(p)!=m[k]: raise ValueError('stock build binding mismatch: '+k)
    return m

def byte_check(control,m):
    p=Path(control)/'003-readback.result.json'
    if not p.exists(): return False
    r=json.loads(p.read_text());s=r.get('output','').replace(chr(13),'')
    try: data=bytes.fromhex(s.split('STOCK_BYTES_BEGIN'+chr(10),1)[1].split('STOCK_BYTES_END',1)[0])
    except (IndexError,ValueError): return False
    return r.get('status')=='DONE' and hashlib.sha256(data).hexdigest()==m['binary_sha256']

def checks(output,m,control,owner,approved=None):
    approved=PINS if approved is None else approved
    base=lab.dev_edu_oracle(output,m) if m['kind']==kind('step6') else lab.oracle(output,m)
    base['caps_exact']=owner.get('caps')=={'cpu.max':'100000 100000','memory.max':'2147483648','memory.swap.max':'0'} and owner.get('nice',0)>=15
    base['approved_boot_artifacts']=owner.get('stock_hashes')=={k:v for k,v in approved.items() if k!='disk-qemu.vmdk'} and owner.get('base_drive_sha256')==approved['disk-qemu.vmdk']
    base.update(serial_bytes_verified=byte_check(control,m),qemu_reaped=owner.get('stopped_reaped') is True,stock_unchanged=owner.get('stock_hashes')==owner.get('stock_base_hashes_after') and bool(owner.get('stock_hashes')),bounded_completion=owner.get('status')=='REQUESTED_STOP')
    if m['kind']==kind('step6'): base['explicit_stock_irq']=bool(re.search(r'^EDU IRQ metadata api=10 config=11 pin=1 mode=pci-line$',output.replace(chr(13),''),re.M))
    return base

def run(source,bundle,stock,receipt,stage,timeout=600,provenance=None,owner_sha256=None):
    if not 60<=timeout<=900: raise ValueError('stock timeout must be60..900')
    if os.environ.get('EDU_NATIVE_LEASE')!='granted': raise ValueError('explicit sole lease grant required')
    m=verify_inputs(source,bundle,stage);assets=stock_inputs(stock,provenance,owner_sha256)
    receipt=lab.external(receipt);control=receipt.with_suffix('.control')
    if control.exists() or receipt.with_suffix('.json').exists(): raise ValueError('fresh receipt required')
    control.mkdir(parents=True);queue=control/'queue';queue.mkdir()
    helper=ROOT/'scripts/stock_console.py'
    command=['systemd-run','--user','--scope','--quiet','-p','CPUQuota=100%','-p','MemoryMax=2G','-p','MemorySwapMax=0','nice','-n','15',sys.executable,str(helper),'--stock',str(Path(stock).resolve()),'--overlay',str(control/'state.qcow2'),'--control',str(control),'--timeout',str(timeout)]
    if provenance is not None: command += ['--stock-admission',provenance,'--stock-owner-sha256',owner_sha256]
    import stock_lease
    lease=stock_lease.inherited()
    if provenance is not None and lease is None: raise ValueError('whole-chain inherited lease required')
    started=time.time();proc=subprocess.Popen(command,pass_fds=(() if lease is None else (lease,)),stdout=(control/'controller.log').open('w'),stderr=subprocess.STDOUT)
    end=time.monotonic()+timeout;output='';problem=None
    def wait_for(test):
        while time.monotonic()<end:
            if test(): return
            if proc.poll() is not None: raise ValueError('stock console exited; inspect controller.log')
            time.sleep(.2)
        raise TimeoutError('stock deadline')
    def request(name,data):
        save(queue/(name+'.tmp'),data);(queue/(name+'.tmp')).rename(queue/(name+'.json'))
        path=control/(name+'.result.json');wait_for(path.exists);r=json.loads(path.read_text())
        if r.get('status')!='DONE': raise ValueError('stock command failed: '+name)
        return r
    try:
        wait_for(lambda:(control/'serial.private').exists() and b'Startup complete' in (control/'serial.private').read_bytes())
        prepared=request('001-prepare',dict(kind='send',text='mkdir /data/edu-own; echo STOCK_DIR_RC=$?; stty -echo; echo STOCK_READY',marker='STOCK_READY',timeout=30))
        if 'STOCK_DIR_RC=0' not in prepared['output']: raise ValueError('target directory preparation failed')
        request('002-transfer',dict(kind='transfer',source=str(Path(bundle).resolve()/'learner_bin'),sha256=m['binary_sha256'],target='/data/edu-own/learner'))
        request('003-readback',dict(kind='send',text='echo STOCK_BYTES_BEGIN; od -An -v -tx1 /data/edu-own/learner; echo STOCK_BYTES_END',marker='STOCK_BYTES_END',timeout=45))
        if not byte_check(control,m): raise ValueError('target ELF readback mismatch')
        binding='echo LEARNER_BIND source='+m['source_sha256']+' binary='+m['binary_sha256']+'; '
        begin='chmod 700 /data/edu-own/learner; '+binding+'echo "EDU TARGET $(uname -s) $(uname -r) $(uname -m)"; '
        if stage=='step6':
            action='/data/edu-own/learner --pci-line > /data/edu-own/app.log 2>&1 & learner_pid=$!; waitfor /dev/edu 5; printf "10\n" > /dev/edu; write_rc=$?; observed=$(cat /dev/edu); read_rc=$?; echo "LEARNER_DEV_EDU write_rc=$write_rc read_rc=$read_rc result=$observed"; result_rc=1; if test "$write_rc" = 0 && test "$read_rc" = 0 && test "$observed" = 3628800; then result_rc=0; fi; kill "$learner_pid"; wait "$learner_pid"; echo LEARNER_DAEMON_EXIT=$?; cat /data/edu-own/app.log; '
        else: action='/data/edu-own/learner; result_rc=$?; '
        # Read-only tool probes, no policy loading/displacement or fake deny/allow.
        finish='echo LEARNER_SLOG2_BEGIN; slog2info -b edu_learner; slog_rc=$?; echo LEARNER_SLOG2_END rc=$slog_rc; command -v secpolpush; echo SECPOL_PUSH_TOOL_RC=$?; command -v secpolmonitor; echo SECPOL_MONITOR_TOOL_RC=$?; echo LEARNER_TRACE OMITTED finish_only_scope; echo LEARNER_RC=$result_rc; echo STOCK_DONE'
        action=action.replace(chr(10),chr(92)+'n')
        output=request('004-observe',dict(kind='send',text=begin+action+finish,marker='STOCK_DONE',timeout=45))['output']
    except (ValueError,TimeoutError) as e: problem=str(e)
    finally:
        (control/'STOP').write_text('end bounded stock attempt')
        try:proc.wait(35)
        except subprocess.TimeoutExpired:
            # Helper pump checks total budget; do not abandon owned QEMU.
            proc.wait(max(1,int(end-time.monotonic())+35))
    owner=json.loads((control/'owner-final.json').read_text()) if (control/'owner-final.json').exists() else {}
    result=checks(output,m,control,owner,{k:v['sha256'] for k,v in assets.items()})
    if provenance is not None: result['independent_owner_binding']=owner.get('stock_admission')==provenance and owner.get('stock_owner_sha256')==owner_sha256
    result['inputs_unchanged_after_boot']=verify_inputs(source,bundle,stage)==m and stock_inputs(stock,provenance,owner_sha256)==assets
    success=bool(owner.get('caps')) and all(result.values()) and problem is None
    evidence=dict(m,success=success,checks=result,started=started,finished=time.time(),stock_assets=assets,disk_sha256=assets['disk-qemu']['sha256'],image_sha256=assets['ifs.bin']['sha256'],stock_provenance='REUSED approved Nov13 clean stock artifacts; NOT a new image build',caps=owner.get('caps'),owner=owner,run_driver_sha256=lab.sha(__file__),console_driver_sha256=lab.sha(helper),qemu_command=command,error=problem,optional_secpol='BLOCKED: no approved nondisplacing loaded policy/denyallow fixture; tools probed only',optional_trace='NOT_RUN finish-only scope; no performance claim')
    if provenance is not None:
        import stock_provenance as fresh
        evidence['stock_provenance']=fresh.verify(stock,owner_sha256=owner_sha256)
        evidence['stock_owner_sha256']=owner_sha256
        evidence['stock_admission']='independent-cooperative-v1'
    receipt.with_suffix('.log').write_text(output);save(receipt.with_suffix('.json'),evidence)
    print(output);print('STOCK_NATIVE_PASS' if success else 'STOCK_NATIVE_FAIL');return 0 if success else 1

def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='action',required=True)
    for action in ['build','run']:
        a=s.add_parser(action)
        for x in ['source','stage','out','sdp-env'] if action=='build' else ['source','stage','bundle','stock','receipt']:a.add_argument('--'+x,required=True)
        if action=='run':
            a.add_argument('--timeout',type=int,default=600)
            a.add_argument('--stock-admission',choices=['independent-cooperative-v1'])
            a.add_argument('--stock-owner-sha256')
    a=p.parse_args()
    try:
        if a.action=='build':print(json.dumps(build(a.source,a.out,a.sdp_env,a.stage)));return 0
        return run(a.source,a.bundle,a.stock,a.receipt,a.stage,a.timeout,a.stock_admission,a.stock_owner_sha256)
    except (ValueError,OSError,KeyError,subprocess.SubprocessError) as e:print('BLOCKED:',e,file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
