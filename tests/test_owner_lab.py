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
 def test_effective_caps_fail_closed_without_qemu(self):
  import tempfile
  tree=ast.parse((ROOT/'tools/owner_lab/guestctl.py').read_text())
  node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='verify_caps')
  ns={};exec(compile(ast.Module(body=[node],type_ignores=[]),'<caps-test>','exec'),ns)
  verify=ns['verify_caps']
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);group=root/'parent'/'child';group.mkdir(parents=True)
   def caps(where,cpu='100000 100000',memory='2147483648',swap='0'):
    for name,value in [('cpu.max',cpu),('memory.max',memory),('memory.swap.max',swap)]: (where/name).write_text(value)
   caps(group);verify(group,root,15)
   for cpu,memory,swap,nice in [('250000 100000','2147483648','0',15),('100000 100000','4294967296','0',15),('100000 100000','2147483648','max',15),('100000 100000','2147483648','0',0)]:
    caps(group,cpu,memory,swap)
    with self.assertRaises(SystemExit):verify(group,root,nice)
   caps(group,'max 100000','max','max');caps(group.parent);verify(group,root,15)
   (group.parent/'cpu.max').write_text('malformed')
   with self.assertRaises(SystemExit):verify(group,root,15)
   with self.assertRaises(SystemExit):verify(root.parent,root,15)
 def test_judges_exact_stock_recipe_and_history_boundary(self):
  judges=(ROOT/'docs/JUDGES.md').read_text()
  for text in ['local/snippets/qemu_options.edu','-device edu','mkqnximage --type=qemu --arch=x86_64 --ram=512M --cpu=1 --ssh-ident=none --build','. "$EDU_SDP_ENV"']:
   self.assertIn(text,judges)
  readme=(ROOT/'README.md').read_text()
  self.assertNotIn('BLOCKED_NATIVE_TIMEOUT',readme.split('## Historical',1)[0])
