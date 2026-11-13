import json,os,signal,time
from pathlib import Path
w=Path(__file__).resolve().parent;g=Path('/home/ubuntu/qnx-host/guest');pid=int((g/'qemu.pid').read_text());cmd=Path('/proc/%d/cmdline'%pid).read_bytes();assert b'-m\x001024\x00' in cmd and b'tb-size=256' in cmd
cg=Path('/sys/fs/cgroup')/next(x.split(':',2)[2].strip().lstrip('/') for x in Path('/proc/%d/cgroup'%pid).read_text().splitlines() if x.startswith('0::'))
r={'pid':pid,'scope':str(cg),'breach':False,'samples':0,'peak_bytes':0,'swap_bytes':0}
try:
 while Path('/proc/%d'%pid).exists():
  try:
   a={k:(cg/k).read_text().strip() for k in ['cpu.max','memory.max','memory.swap.max','memory.current','memory.peak','memory.events','memory.swap.current']};assert a['cpu.max']=='100000 100000' and a['memory.max']=='2147483648' and a['memory.swap.max']=='0'
   a.update(epoch=time.time(),phase='shutdown' if (w/'STOP').exists() else 'stock_build',qemu_status=Path('/proc/%d/status'%pid).read_text());r['samples']+=1;r['peak_bytes']=max(r['peak_bytes'],int(a['memory.peak']));r['swap_bytes']=max(r['swap_bytes'],int(a['memory.swap.current']))
   with (w/'safety-tail.jsonl').open('a') as f:f.write(json.dumps(a)+'\n')
   if max(int(a['memory.current']),int(a['memory.peak']))+67108864>2147483648 or 'oom_kill 0' not in a['memory.events']:
    r.update(breach=True,breach_sample=a);(w/'STOP').write_text('resource safety breach');os.kill(pid,signal.SIGTERM);break
  except FileNotFoundError:break
  time.sleep(1)
finally:
 r['ended']=time.time();r['qemu_absent']=not Path('/proc/%d'%pid).exists();(w/'safety-tail-result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
