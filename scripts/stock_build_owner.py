#!/usr/bin/env python3
"""One supervised fresh stock SDK build and owner finalization. No native launch."""
import argparse, json, os, shlex, subprocess, sys, time
from pathlib import Path
import learner_lab as lab
import stock_lease as lease
import stock_provenance as provenance
ROOT=Path(__file__).resolve().parents[1]
CAPS={'cpu.max':'100000 100000','memory.max':'2147483648','memory.swap.max':'0'}
def no_qemu():
 # Include absolute executable paths; do not mistake the diagnostic shell for QEMU.
 return subprocess.run(['pgrep','-f',r'^(/[^ ]*/)?qemu-system-'],capture_output=True).returncode==1

def run(controller,case,environment):
 controller=provenance.external(controller);case=provenance.external(case)
 guest=controller.parent;share=guest/'shared'
 if not case.is_relative_to(share) or case.exists(): raise ValueError('new case under existing private shared mount required')
 fd=lease.inherited()
 own=fd is None
 if own: fd=lease.acquire()
 owner=None
 try:
  if not no_qemu(): raise ValueError('foreign QEMU present')
  if not lease.queue_clear(guest): raise ValueError('queued or unresolved SDK jobs; inspect original requests, never delete/retry')
  if int(dict(line.split(':',1) for line in Path('/proc/meminfo').read_text().splitlines())['MemAvailable'].split()[0])*1024<2147483648+67108864: raise ValueError('insufficient actual HOST memory headroom')
  case.mkdir(mode=0o700);repo=case/'repo'
  subprocess.run(['git','clone','--no-hardlinks',str(ROOT),str(repo)],check=True,capture_output=True)
  if subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT): raise ValueError('clean source checkout required')
  rel=case.relative_to(share);g=Path('/mnt/host')/rel
  build=case/'build.sh'
  q=shlex.quote
  build.write_text('#!/bin/bash\nset -euo pipefail\nchown -R qnx:qnx '+q(str(g))+'\nrunuser -u qnx -- env HOME=/home/qnx EDU_STOCK_BUILDER=sole-owner python3 '+q(str(g/'repo/scripts/stock_provenance.py'))+' build --project '+q('/home/qnx/edu-independent-'+case.name)+' --stock '+q(str(g/'stock'))+' --environment '+q(environment)+'\n')
  control=case/'sdk-control';control.mkdir();env=os.environ.copy();env['EDU_STOCK_LEASE_FD']=str(fd)
  with (case/'sdk-owner.log').open('w') as log:
   owner=subprocess.Popen([sys.executable,str(ROOT/'scripts/stock_sdk_owner.py'),'--controller',str(controller),'--control',str(control)],env=env,pass_fds=(fd,),stdout=log,stderr=subprocess.STDOUT)
   end=time.monotonic()+620
   while not (control/'SDK_READY').exists():
    if owner.poll() is not None: raise ValueError('SDK owner failed before ready')
    if time.monotonic()>end: raise ValueError('SDK readiness deadline')
    time.sleep(1)
   # This controller's timeout leaves the original job intact. No resubmission.
   job=subprocess.run([sys.executable,str(controller),'exec',str(build),'1500'],stdout=(case/'queue.private.log').open('w'),stderr=subprocess.STDOUT)
   if job.returncode: raise ValueError('original SDK job incomplete/failed: inspect queue.private.log; no retry')
  return finalize(case,owner)
 finally:
  if owner is not None:
   (case/'sdk-control/STOP').write_text('bounded stock builder shutdown')
   try: owner.wait(timeout=190)
   except subprocess.TimeoutExpired:
    # The supervised owner owns QEMU; never kill an unrelated PID.
    raise RuntimeError('SDK owner failed to reap within shutdown bound; preserve lease and inspect')
  if own: os.close(fd)

def finalize(case,owner):
 (case/'sdk-control/STOP').write_text('stock build complete')
 owner.wait(timeout=190)
 sdk=json.loads((case/'sdk-control/sdk-owner.json').read_text())
 if sdk.get('status')!='REQUESTED_STOP' or sdk.get('stopped_reaped') is not True or sdk.get('caps')!=CAPS or sdk.get('shutdown_resource_breach') or not no_qemu(): raise ValueError('SDK cleanup/caps failed')
 if not lease.queue_clear(case.parent.parent): raise ValueError('queue changed before finalization; preserve original requests')
 stock=case/'stock';m=provenance.verify(stock,False)
 # This private receipt is trusted only through the separately returned digest.
 r=dict(kind='edu-independent-stock-owner-v1',build_sha256=lab.sha(stock/'stock-build.json'),stock=str(stock),builder_sha256=lab.sha(provenance.__file__),caps=CAPS,stopped_reaped=True,queue_clear=True,foreign_qemu=0)
 (stock/'stock-owner.json').write_text(json.dumps(r,indent=2)+'\n')
 digest=lab.sha(stock/'stock-owner.json');provenance.verify(stock,owner_sha256=digest)
 print('STOCK_OWNER_SHA256='+digest,flush=True)
 return digest

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--controller',required=True);p.add_argument('--case',required=True);p.add_argument('--environment',default='/home/qnx/qnx800/qnxsdp-env.sh');a=p.parse_args()
 try: run(a.controller,a.case,a.environment);return 0
 except (ValueError,OSError,subprocess.SubprocessError) as e: print('BLOCKED:',e,file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
