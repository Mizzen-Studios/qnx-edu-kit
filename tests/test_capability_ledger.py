from pathlib import Path
import hashlib, importlib.util, json, subprocess, tempfile, unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('capability_ledger',ROOT/'tools/capability_ledger.py')
ledger=importlib.util.module_from_spec(spec);spec.loader.exec_module(ledger)
class CapabilityLedger(unittest.TestCase):
 def test_declarations_and_pinned_evidence_current(self):
  subprocess.run(['python3',str(ROOT/'tools/capability_ledger.py')],check=True,capture_output=True)
 def test_readme_status_use_canonical_ledger(self):
  for name in ('README.md','STATUS.md'):
   self.assertIn('docs/capabilities.md',(ROOT/name).read_text())
 def test_invalid_missing_and_changed_evidence_rejected(self):
  # Declaration fixtures only, never accepted as target evidence.
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp);(root/'docs').mkdir();(root/'evidence.txt').write_text('declaration fixture')
   row=dict(id='fixture',domain='native',level='compile',status='UNVERIFIED',claim='test fixture only',evidence='evidence.txt',evidence_sha256=hashlib.sha256((root/'evidence.txt').read_bytes()).hexdigest())
   data=dict(schema='qnx-capabilities.v1',project='fixture',boundary='not runtime',rows=[row])
   path=root/'docs/capabilities.json'
   def save():path.write_text(json.dumps(data))
   save();self.assertIn('UNVERIFIED',ledger.render(root))
   for field,value in [('status','RUNNING'),('domain','pretend-native'),('evidence','../escape'),('evidence','absent.txt'),('evidence_sha256','0'*64)]:
    original=row[field];row[field]=value;save()
    with self.assertRaises(ValueError):ledger.render(root)
    row[field]=original
   data['rows'].append(dict(row));save()
   with self.assertRaises(ValueError):ledger.render(root)
