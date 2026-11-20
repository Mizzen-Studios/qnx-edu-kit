import os, subprocess, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class VerifyPrerequisites(unittest.TestCase):
    def test_missing_make_fails_explicitly(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp)/'dirname').symlink_to('/usr/bin/dirname')
            for args in ([], ['--host-only']):
                p=subprocess.run(['/bin/sh',str(ROOT/'verify.sh'),*args],env={**os.environ,'PATH':tmp},capture_output=True,text=True)
                self.assertEqual(p.returncode,2)
                self.assertIn('BLOCKED: GNU make is required',p.stderr)
