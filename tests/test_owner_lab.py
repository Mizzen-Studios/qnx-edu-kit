import ast, os, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class OwnerLabTests(unittest.TestCase):
 def test_missing_external_directory_fails_without_start(self):
  env=os.environ.copy();env.pop('EDU_LAB_DIR',None)
  p=subprocess.run([sys.executable,str(ROOT/'tools/owner_lab/guestctl.py'),'start'],env=env,capture_output=True,text=True)
  self.assertNotEqual(p.returncode,0);self.assertIn('Set EDU_LAB_DIR',p.stderr)
 def test_source_and_queue_contract(self):
  source=(ROOT/'tools/owner_lab/guestctl.py').read_text();ast.parse(source)
  for marker in ['CPUQuota=100%','MemoryMax=2G','MemorySwapMax=0','tb-size=256',"'-smp','1'","'nice','-n','15'",'job not cancelled']:
   self.assertIn(marker,source)
  subprocess.run(['bash','-n',str(ROOT/'tools/owner_lab/host-queue.sh')],check=True)
  queue=(ROOT/'tools/owner_lab/host-queue.sh').read_text()
  self.assertIn('rc.tmp',queue);self.assertIn('cmd.running',queue)
