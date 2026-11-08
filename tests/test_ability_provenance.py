import json,shutil,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import ability_provenance as provenance
class AbilityProvenance(unittest.TestCase):
 def test_actual_evidence_passes(self):
  self.assertEqual(provenance.validate(ROOT/'docs/acceptance/ability-20261108')['status'],'PASS')
 def test_wrong_type_and_changed_bytes_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   folder=Path(tmp)/'ability';shutil.copytree(ROOT/'docs/acceptance/ability-20261108',folder)
   original=(folder/'provenance.json').read_bytes()
   data=json.loads(original);data['evidence_type']='native-acceptance';(folder/'provenance.json').write_text(json.dumps(data))
   with self.assertRaisesRegex(ValueError,'wrong ability provenance type'):provenance.validate(folder)
   (folder/'provenance.json').write_bytes(original)
   (folder/'run.json').write_bytes((folder/'run.json').read_bytes()+b' ')
   with self.assertRaisesRegex(ValueError,'changed shared evidence'):provenance.validate(folder)
 def test_bool_errno_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   folder=Path(tmp)/'ability';shutil.copytree(ROOT/'docs/acceptance/ability-20261108',folder)
   data=json.loads((folder/'receipt.json').read_text());data['allow']['errno']=False
   (folder/'receipt.json').write_text(json.dumps(data))
   with self.assertRaisesRegex(ValueError,'wrong type'):provenance.validate(folder)

 def test_literal_can_receipt_cannot_be_ability_receipt(self):
  import subprocess
  with tempfile.TemporaryDirectory() as tmp:
   folder=Path(tmp)/'ability';shutil.copytree(ROOT/'docs/acceptance/ability-20261108',folder)
   (folder/'receipt.json').write_bytes((folder/'run.json').read_bytes())
   with self.assertRaisesRegex(ValueError,'ability receipt type invalid'):provenance.validate(folder)
   result=subprocess.run([sys.executable,str(ROOT/'scripts/ability_provenance.py'),str(folder)],capture_output=True,text=True)
   self.assertEqual(result.returncode,2)
   self.assertIn('ability receipt type invalid',result.stderr)
 def test_catalog_and_appendix_reject_literal_substitution(self):
  import importlib.util
  from unittest.mock import patch
  def module(name,path):
   spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
  ledger=module('typed_ledger','tools/capability_ledger.py')
  packet=module('typed_packet','docs/review/build_packet.py')
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);folder=root/'docs/acceptance/ability-20261108';folder.parent.mkdir(parents=True)
   shutil.copytree(ROOT/'docs/acceptance/ability-20261108',folder)
   (root/'docs/capabilities.json').write_bytes((ROOT/'docs/capabilities.json').read_bytes())
   (folder/'receipt.json').write_bytes((folder/'run.json').read_bytes())
   # Keep only the ability row: fixture does not need unrelated evidence copies.
   data=json.loads((root/'docs/capabilities.json').read_text());data['rows']=[x for x in data['rows'] if x['id']=='ability-stage']
   (root/'docs/capabilities.json').write_text(json.dumps(data))
   with self.assertRaisesRegex(ValueError,'ability receipt type invalid'):ledger.render(root)
   with patch.object(packet,'ROOT',root):
    with self.assertRaisesRegex(ValueError,'ability receipt type invalid'):packet.build()
