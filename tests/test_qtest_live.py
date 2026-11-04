"""Explicit opt-in integration tests run the installed executable, never a model."""
import os
from pathlib import Path
import subprocess
import unittest
ROOT=Path(__file__).resolve().parents[1]
class QtestLive(unittest.TestCase):
    def test_requires_opt_in(self):
        result=subprocess.run(['python3','scripts/edu_qtest.py'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertIn('--run required',result.stderr)
    @unittest.skipUnless(os.getenv('EDU_LIVE_QTEST')=='1','set EDU_LIVE_QTEST=1 for actual QEMU')
    def test_actual_installed_qemu(self):
        result=subprocess.run(['python3','scripts/edu_qtest.py','--run'],cwd=ROOT,capture_output=True,text=True,timeout=45)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertIn('PASS live register suite including isolated fatal DMA bounds',result.stdout)
        self.assertEqual(result.stdout.count('PASS expected QEMU fatal DMA'),4)
