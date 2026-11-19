#!/usr/bin/env python3
"""Hold the exclusive lease across a trusted owner's entire SDK/native script."""
import argparse,json,os,subprocess,sys,time
from pathlib import Path
import stock_lease
from stock_build_owner import no_qemu

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('script',help='trusted private owner script, not a downloaded manifest');a=p.parse_args()
 fd=stock_lease.acquire();env=os.environ.copy();env['EDU_STOCK_LEASE_FD']=str(fd)
 try:
  if not no_qemu(): raise ValueError('foreign QEMU before chain')
  rc=subprocess.run(['bash',str(Path(a.script).resolve())],env=env,pass_fds=(fd,)).returncode
  if not no_qemu(): raise RuntimeError('QEMU remains after owned chain; do not start another lease')
  return rc
 finally: os.close(fd)
if __name__=='__main__':
 try: sys.exit(main())
 except (ValueError,OSError,subprocess.SubprocessError) as e: print('BLOCKED:',e,file=sys.stderr);sys.exit(2)
