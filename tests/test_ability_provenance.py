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
