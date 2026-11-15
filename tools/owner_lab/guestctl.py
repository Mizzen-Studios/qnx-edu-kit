#!/usr/bin/env python3
import os,sys,time,json,socket,subprocess
from pathlib import Path
p=Path(os.environ.get('EDU_LAB_DIR','')).expanduser().resolve()
if not os.environ.get('EDU_LAB_DIR'):raise SystemExit('Set EDU_LAB_DIR to existing external guest assets; no installation is performed')
qmp=p/'qmp.sock'
def verify_caps(group, root, nice):
 """Fail closed before QEMU: effective cgroup-v2 ancestor limits and priority."""
 group=group.resolve();root=root.resolve()
 if group!=root and root not in group.parents:raise SystemExit('Invalid cgroup path')
 cpu=[];memory=[];swap=[]
 try:
  for parent in [group,*group.parents]:
   if parent!=root and root not in parent.parents:continue
   for name,dest in [('memory.max',memory),('memory.swap.max',swap)]:
    path=parent/name
    if path.exists():
     value=path.read_text().strip()
     if value!='max':dest.append(int(value))
   path=parent/'cpu.max'
   if path.exists():
    quota,period=path.read_text().split()
    if quota!='max':
     quota=int(quota);period=int(period)
     if quota<=0 or period<=0:raise ValueError('invalid CPU quota')
     cpu.append(quota/period)
 except (OSError,ValueError) as exc:raise SystemExit('Unreadable canonical caps: '+str(exc))
 if not cpu or min(cpu)>1 or not memory or min(memory)>2147483648 or min(memory)<=0 or not swap or min(swap)!=0 or nice!=15:
  raise SystemExit('Refusing QEMU: require effective CPU<=100%, memory<=2GiB, swap0, nice15')
def request(cmd):
 with socket.socket(socket.AF_UNIX) as s:
  s.settimeout(10); s.connect(str(qmp)); f=s.makefile('rwb',buffering=0); f.readline()
  def call(obj):
   f.write((json.dumps(obj)+'\n').encode())
   while True:
    data=json.loads(f.readline())
    if 'return' in data or 'error' in data:return data
  call({'execute':'qmp_capabilities'});return call({'execute':cmd})
mode=sys.argv[1]
if mode=='run':
 root=Path('/sys/fs/cgroup')
 relative=next(line.split(':',2)[2] for line in Path('/proc/self/cgroup').read_text().splitlines() if line.startswith('0::'))
 group=root/relative.lstrip('/')
 verify_caps(group,root,os.getpriority(os.PRIO_PROCESS,0))
 sdk_memory=os.environ.get('CAN_SDK_MEMORY_MIB','512')
 edu_memory=os.environ.get('EDU_SDK_MEMORY_MIB')
 if edu_memory is not None:
  if edu_memory != '1024': raise SystemExit('EDU SDK opt-in must be1024; native guests remain512')
  sdk_memory=edu_memory
 elif sdk_memory not in ('512','768'): raise SystemExit('SDK memory override must be512 or768')
 args=['qemu-system-x86_64','-machine','q35','-accel','tcg,tb-size=256','-cpu','max','-smp','1','-m',sdk_memory,'-display','none','-no-reboot','-serial','stdio','-monitor','none','-qmp',f'unix:{qmp},server=on,wait=off','-drive',f'file={p}/guest.qcow2,format=qcow2,if=virtio','-drive',f'file={p}/seed.iso,format=raw,media=cdrom,readonly=on','-nic','user,model=virtio-net-pci','-virtfs',f'local,path={p}/shared,mount_tag=hostshare,security_model=mapped-xattr,id=shared']
 (p/'launch.json').write_text(json.dumps({'args':args,'started':time.time()},indent=2))
 proc=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL)
 (p/'qemu.pid').write_text(str(proc.pid)); log=open(p/'serial.log','ab')
 try:
  while True:
   b=proc.stdout.read1(65536)
   if not b:break
   if log.tell()+len(b)>8*1024*1024:
    log.close();os.replace(p/'serial.log',p/'serial.previous.log');log=open(p/'serial.log','wb')
   log.write(b);log.flush()
 finally:
  log.close();rc=proc.wait();(p/'exit.json').write_text(json.dumps({'rc':rc,'ended':time.time()}));sys.exit(rc)
elif mode=='start':
 if qmp.exists():
  try: print(request('query-status'));sys.exit(0)
  except (OSError,ValueError):qmp.unlink()
 (p/'shared/ready').unlink(missing_ok=True)
 os.execvp('systemd-run',['systemd-run','--user','--scope','--quiet','-p','CPUQuota=100%','-p','MemoryMax=2G','-p','MemorySwapMax=0','nice','-n','15',sys.executable,__file__,'run'])
elif mode=='status':print(request('query-status'))
elif mode=='stop':
 print(request('system_powerdown'))
 for _ in range(120):
  try:request('query-status')
  except (OSError,ValueError):print('stopped');break
  time.sleep(1)
 else: print('ACPI timeout; QMP quit');print(request('quit'))
elif mode=='exec':
 source=Path(sys.argv[2]); timeout=int(sys.argv[3]) if len(sys.argv)>3 else 900
 ident=str(time.time_ns());queue=p/'shared/queue';res=p/'shared/results';tmp=queue/(ident+'.tmp');tmp.write_bytes(source.read_bytes());tmp.rename(queue/(ident+'.sh'))
 print('job',ident,flush=True);end=time.monotonic()+timeout
 while time.monotonic()<end:
  rc=res/(ident+'.rc')
  if rc.exists():print((res/(ident+'.log')).read_text());sys.exit(int(rc.read_text()))
  time.sleep(2)
 print('timed out; job not cancelled; inspect shared/results/'+ident+'.log',file=sys.stderr);sys.exit(124)
else:raise SystemExit('start|status|stop|exec script [timeout]')
