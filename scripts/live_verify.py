#!/usr/bin/env python3
"""Fresh local custom QNX boot only; QSTI provenance is a separate gate; a saved transcript is never an input mode."""
import argparse, hashlib, json, os, pathlib, re, selectors, subprocess, sys, time
ROOT=pathlib.Path(__file__).resolve().parents[1]
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def sources():
    return {str(p.relative_to(ROOT)):digest(p) for p in sorted((ROOT/'native').glob('*')) if p.is_file()}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--step',type=int,choices=range(1,7));args=parser.parse_args()
    base=os.environ.get('EDU_LIVE_BUNDLE')
    if not base:
        print('BLOCKED: set EDU_LIVE_BUNDLE to an external fresh-built image/manifest directory');return 2
    bundle=pathlib.Path(base).resolve()
    try:
        manifest=json.loads((bundle/'manifest.json').read_text())
        if manifest['sources']!=sources(): raise ValueError('source hashes differ: rebuild required')
        image=bundle/'ifs-edu-followup10.bin'
        if digest(image)!=manifest['image_sha256']: raise ValueError('image hash mismatch')
        if os.environ.get('EDU_NATIVE_LEASE')!='granted': raise ValueError('explicit exclusive native lease required')
        disk=pathlib.Path(manifest['disk'])
        if not disk.is_file(): raise ValueError('external disk absent')
    except (OSError,KeyError,ValueError) as error:
        print('BLOCKED:',error);return 2
    command=['systemd-run','--user','--scope','--quiet','-p','CPUQuota=100%','-p','MemoryMax=1G',
             'nice','-n','15','qemu-system-x86_64','-machine','pc,accel=tcg','-cpu','max',
             '-smp','1','-m','512','-display','none','-serial','stdio','-monitor','none',
             '-no-reboot','-kernel',str(image),'-drive','file='+str(disk)+',format=raw,if=ide,snapshot=on',
             '-nic','user,model=virtio-net-pci','-object','can-bus,id=canbus0',
             '-device','kvaser_pci,canbus=canbus0','-device','edu,dma_mask=0xffffffff']
    start=time.time();run=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    selector=selectors.DefaultSelector();selector.register(run.stdout,selectors.EVENT_READ);data=b'';cap=None
    try:
        end=time.monotonic()+240
        while time.monotonic()<end:
            if cap is None:
                found=subprocess.run(['pgrep','-P',str(run.pid)],capture_output=True,text=True).stdout.split()
                # Walk descendants until QEMU, then bind effective cgroup limits.
                todo=list(found)
                while todo:
                    pid=todo.pop();proc=pathlib.Path('/proc')/pid
                    try:
                        cmd=(proc/'cmdline').read_bytes()
                        if b'qemu-system-x86_64' in cmd and cmd.split(b'\0')[0].endswith(b'qemu-system-x86_64'):
                            rel=next(x.split(':',2)[2] for x in (proc/'cgroup').read_text().splitlines() if x.startswith('0::'))
                            cg=pathlib.Path('/sys/fs/cgroup')/rel.lstrip('/')
                            cap={'pid':int(pid),'cpu':(cg/'cpu.max').read_text().strip(),'memory':(cg/'memory.max').read_text().strip(),'nice':os.getpriority(os.PRIO_PROCESS,int(pid))}
                            q,p=cap['cpu'].split()
                            if q=='max' or int(q)>int(p) or int(cap['memory'])>1073741824 or cap['nice']<15: raise RuntimeError('caps invalid')
                        else: todo+=subprocess.run(['pgrep','-P',pid],capture_output=True,text=True).stdout.split()
                    except FileNotFoundError: pass
            if selector.select(.1):
                chunk=os.read(run.stdout.fileno(),65536)
                if not chunk: break
                data+=chunk
                if b'EDU_PROBE_RC=' in data: break
            if run.poll() is not None: break
    finally:
        # systemd scope wrapper is not QEMU: signal captured owned QEMU first.
        if cap:
            try: os.kill(cap['pid'],15)
            except ProcessLookupError: pass
        try: run.wait(10)
        except subprocess.TimeoutExpired:
            if cap:
                try: os.kill(cap['pid'],9)
                except ProcessLookupError: pass
            run.terminate();run.wait(10)
    output=data.decode(errors='replace');sys.stdout.write(output)
    checks={str(n):bool(re.search(r'EDU STEP'+str(n)+r' PASS',output)) for n in range(1,7)}
    checks['6']=checks['6'] and 'EDU_SHELL_RESULT=3628800' in output and bool(re.search(r'EDU RESMGR IRQ completion=\d+ input=10 result=3628800 ack=00000000',output)) and 'EDU RESMGR ACCEPT PASS' in output
    success=bool(cap) and 'EDU TARGET QNX 8.0' in output and 'EDU_PROBE_RC=0' in output and all(checks.values())
    evidence={'started':start,'finished':time.time(),'sources':sources(),'image_sha256':manifest['image_sha256'],'caps':cap,'steps':checks,'success':success,'label':'observed in this QEMU run; app budget, not a QNX benchmark','target_provenance':manifest.get('target_provenance','custom QNX 8 IFS; QSTI provenance unverified')}
    out=bundle/('live-'+str(time.time_ns()));out.with_suffix('.log').write_bytes(data);out.with_suffix('.json').write_text(json.dumps(evidence,indent=2)+'\n')
    for n in ([args.step] if args.step else range(1,7)): print(('PASS' if success and checks[str(n)] else 'FAIL')+': step '+str(n)+' fresh QNX target')
    return 0 if success else 1
if __name__=='__main__': sys.exit(main())
