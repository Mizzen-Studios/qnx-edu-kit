"""Owned stock-native console, file-queued commands; no custom IFS or SDK launch. Stock artifact reuse, not generation."""
import argparse,fcntl,hashlib,json,os,re,selectors,shlex,signal,subprocess,time
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--stock',required=True);ap.add_argument('--overlay',required=True);ap.add_argument('--control',required=True);ap.add_argument('--timeout',type=int,default=1200);ap.add_argument('--stock-admission',choices=['independent-cooperative-v1']);ap.add_argument('--stock-owner-sha256');a=ap.parse_args()
stock=Path(a.stock).resolve();overlay=Path(a.overlay).resolve();control=Path(a.control).resolve();control.mkdir(parents=True,exist_ok=True);queue=control/'queue';queue.mkdir(exist_ok=True)
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
import stock_lease
lease=stock_lease.inherited()
if lease is None:
 lock=open('/home/ubuntu/qnx-host/native-test.lock','a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
if a.stock_admission:
 import stock_provenance
 assert lease is not None, 'whole-chain lease required'
 stock_provenance.verify(a.stock,owner_sha256=a.stock_owner_sha256)
assert subprocess.run(['pgrep','-f','^qemu-system-'],stdout=subprocess.DEVNULL).returncode==1
cg=Path('/sys/fs/cgroup')/next(x.split(':',2)[2].strip().lstrip('/') for x in Path('/proc/self/cgroup').read_text().splitlines() if x.startswith('0::'))
caps={k:(cg/k).read_text().strip() for k in ['cpu.max','memory.max','memory.swap.max']};assert caps=={'cpu.max':'100000 100000','memory.max':'2147483648','memory.swap.max':'0'} and os.getpriority(os.PRIO_PROCESS,0)>=15
opts=shlex.split((stock/'qemu_options').read_text());assert opts==['-device','edu']
settings=(stock/'options').read_text()
def opt(name,default):
 m=re.search(r'^'+name+r'=[\"\']?([^\"\'\n ]+)',settings,re.M);return m.group(1) if m else default
mode=opt('OPT_BOOT_MODE','default');mode='bios' if mode=='default' else mode;assert mode in ('bios','uefi')
assert opt('OPT_RAM','')=='512M' and opt('OPT_CPU','')=='1'
assert (stock/'ifs.bin').stat().st_size>0 and (stock/'disk-qemu').stat().st_size>0
base=stock/'disk-qemu.vmdk' if (stock/'disk-qemu.vmdk').exists() else stock/'disk-qemu';baseformat='vmdk' if base.suffix=='.vmdk' else 'raw'
if not overlay.exists():subprocess.run(['qemu-img','create','-f','qcow2','-F',baseformat,'-b',str(base),str(overlay)],check=True,capture_output=True)
args=['qemu-system-x86_64','-machine','pc','-accel','tcg,tb-size=256','-cpu','max','-smp','1','-m','512','-display','none','-monitor','none','-serial','stdio','-no-reboot','-drive','file='+str(overlay)+',format=qcow2,if=ide,id=drv0','-nic','none','-device','virtio-rng-pci']
if mode=='uefi':
 assert Path('/usr/share/qemu/OVMF.fd').is_file();args+=['-bios','/usr/share/qemu/OVMF.fd']
else:args+=['-kernel',str(stock/'ifs.bin')]
args+=opts
r={'status':'RUNNING','kind':'clean-stock-native-console-owner','caps':caps,'nice':os.getpriority(os.PRIO_PROCESS,0),'command':args,'stock_boot_mode':mode,'network':'none: serial transfer; no bridge/host networking repair','image_provenance':'REUSED hash-verified stock mkqnximage artifacts; only EDU option; lesson copied after boot','stock_hashes':{p.name:h(p) for p in [stock/'ifs.bin',stock/'disk-qemu',stock/'qemu_options',stock/'options']},'base_drive':str(base),'base_drive_sha256':h(base),'overlay_initial_sha256':h(overlay),'commands':[],'memory_samples':0}
if a.stock_admission:
 r['stock_admission']=a.stock_admission;r['stock_owner_sha256']=a.stock_owner_sha256;r['image_provenance']='Fresh independent controlled stock build, separately trusted cooperative owner receipt; not cryptographic attestation'
(control/'owner-start.json').write_text(json.dumps(r,indent=2)+'\n')
proc=None;sel=None;serial=bytearray();started=time.monotonic();lastsample=0;samples=[]
def sample():
 global lastsample
 if time.monotonic()-lastsample<1:return
 lastsample=time.monotonic();s={'time':time.time(),'memory':{k:(cg/k).read_text().strip() for k in ['memory.current','memory.peak','memory.events','memory.swap.current']},'processes':(cg/'cgroup.procs').read_text()}
 if proc and Path('/proc/%s/status'%proc.pid).exists():s['qemu_status']=Path('/proc/%s/status'%proc.pid).read_text()
 samples.append(s)
 with (control/'memory.jsonl').open('a') as f:f.write(json.dumps(s)+'\n')
 if max(int(s['memory']['memory.current']),int(s['memory']['memory.peak']))+67108864>2147483648:raise MemoryError('reserve64 breach')
 if 'oom_kill 0' not in s['memory']['memory.events']:raise MemoryError('HOST OOM')
def pump(wait=.05):
 sample()
 if time.monotonic()-started>a.timeout:raise TimeoutError('native owner total budget')
 if sel.select(wait):
  b=os.read(proc.stdout.fileno(),65536)
  if b:serial.extend(b);(control/'serial.private').write_bytes(serial)
  elif proc.poll() is not None:raise RuntimeError('QEMU exit '+str(proc.returncode))
def send(text):
 b=(text+'\n').encode()
 for i in range(0,len(b),96):proc.stdin.write(b[i:i+96]);proc.stdin.flush();time.sleep(.01)
def until(marker,start,timeout):
 end=time.monotonic()+timeout
 while time.monotonic()<end:
  pump()
  if marker in bytes(serial[start:]).decode(errors='replace').replace('\r','').splitlines():return bytes(serial[start:]).decode(errors='replace')
 raise TimeoutError('marker '+marker)
try:
 proc=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);r['pid']=proc.pid;sel=selectors.DefaultSelector();sel.register(proc.stdout,selectors.EVENT_READ);print('NATIVE_STARTED pid='+str(proc.pid),flush=True)
 while True:
  pump()
  if (control/'STOP').exists():r['status']='REQUESTED_STOP';break
  jobs=sorted(queue.glob('*.json'))
  if not jobs:continue
  job=jobs[0];req=json.loads(job.read_text());ident=job.stem;result={'id':ident,'kind':req['kind'],'started':time.time()}
  try:
   if req['kind']=='send':
    start=len(serial);send(req['text']);result['text']=req['text'];result['output']=until(req['marker'],start,req.get('timeout',60)) if req.get('marker') else '';result['status']='DONE'
   elif req['kind']=='transfer':
    data=Path(req['source']).read_bytes();assert hashlib.sha256(data).hexdigest()==req['sha256'];target=req['target'];assert re.fullmatch(r'/[A-Za-z0-9_./-]+',target)
    marker='EDU_COPY_INIT_'+ident;start=len(serial);send(': > '+target+'; echo '+marker);until(marker,start,20)
    for at in range(0,len(data),128):
     escaped=''.join(chr(92)+'0'+format(v,'03o') for v in data[at:at+128]);marker='EDU_COPY_'+ident+'_'+str(at);start=len(serial);send("printf '%b' '"+escaped+"' >> "+target+'; echo '+marker);until(marker,start,20)
     if at%4096==0:print('TRANSFER '+ident+' bytes='+str(at),flush=True)
    result.update(status='DONE',bytes=len(data),source=req['source'],source_sha256=req['sha256'],target=target,route='serial builtin printf octal chunks128; target hash verification separate')
   else:raise ValueError('unknown command kind')
  except Exception as e:result.update(status='FAIL',error=repr(e));r['status']='COMMAND_FAILURE';r['error']=repr(e)
  result['ended']=time.time();(control/(ident+'.result.tmp')).write_text(json.dumps(result,indent=2)+'\n');(control/(ident+'.result.tmp')).replace(control/(ident+'.result.json'));r['commands'].append({k:v for k,v in result.items() if k!='output'});job.rename(job.with_suffix('.done'));print('COMMAND '+ident+' '+result['status'],flush=True)
  if result['status']=='FAIL':break
except Exception as e:r['status']='FAIL';r['error']=repr(e)
finally:
 if proc and proc.poll() is None:
  proc.terminate()
  try:r['qemu_rc']=proc.wait(timeout=20)
  except subprocess.TimeoutExpired:proc.kill();r['qemu_rc']=proc.wait(timeout=10)
 elif proc:r['qemu_rc']=proc.returncode
 r['memory_samples']=len(samples);r['peak_cgroup_bytes']=max([int(s['memory']['memory.peak']) for s in samples] or [0]);r['stopped_reaped']=proc is not None and proc.poll() is not None;r['raw_serial_sha256']=hashlib.sha256(serial).hexdigest();r['overlay_final_sha256']=h(overlay) if overlay.exists() else None;r['stock_base_hashes_after']={p.name:h(p) for p in [stock/'ifs.bin',stock/'disk-qemu',stock/'qemu_options',stock/'options']};r['completed_at']=time.time();(control/'owner-final.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r.get(k) for k in ['status','error','peak_cgroup_bytes','stopped_reaped']}),flush=True)
