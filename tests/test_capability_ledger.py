from pathlib import Path
import subprocess, unittest
ROOT=Path(__file__).resolve().parents[1]
class CapabilityLedger(unittest.TestCase):
 def test_declarations_and_pinned_evidence_current(self):
  subprocess.run(['python3',str(ROOT/'tools/capability_ledger.py')],check=True,capture_output=True)
 def test_readme_status_use_canonical_ledger(self):
  for name in ('README.md','STATUS.md'):
   self.assertIn('docs/capabilities.md',(ROOT/name).read_text())
