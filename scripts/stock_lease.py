"""Inherited exclusive lease descriptor, not an environment-only lease claim."""
import fcntl, os
from pathlib import Path
LOCK=Path('/home/ubuntu/qnx-host/native-test.lock')
def acquire():
 fd=os.open(LOCK,os.O_CREAT|os.O_RDWR,0o600)
 fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
 os.set_inheritable(fd,True)
 return fd

def inherited():
 value=os.environ.get('EDU_STOCK_LEASE_FD')
 if value is None: return None
 fd=int(value)
 a=os.fstat(fd);b=LOCK.stat()
 if (a.st_dev,a.st_ino)!=(b.st_dev,b.st_ino): raise ValueError('wrong lease descriptor')
 # A fresh independent open must conflict; the inherited open must own the lock.
 with LOCK.open('a') as probe:
  try: fcntl.flock(probe,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError: pass
  else: raise ValueError('inherited lease is not held')
 fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
 return fd

def queue_clear(guest):
 # .running files are historical consumed requests, not queued .sh work.
 # Caller must also prove zero actual QEMU before a new owner boot.
 return not list((Path(guest)/'shared/queue').glob('*.sh'))
