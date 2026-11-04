import os
from pathlib import Path
import subprocess
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
class CappedLauncherTests(unittest.TestCase):
    def invoke(self, script, args):
        with tempfile.TemporaryDirectory() as d:
            mock=Path(d)/'systemd-run'
            mock.write_text(chr(10).join(['#!/bin/sh',script,'']))
            mock.chmod(0o700)
            return subprocess.run([str(ROOT/'scripts/qemu-capped.sh')]+args, env={**os.environ,'PATH':d+':'+os.environ['PATH']},capture_output=True,text=True)
    def test_exact_cap_and_argument_boundaries(self):
        p=self.invoke('printf "%s'+chr(92)+'n" "$@"',['qemu-system-x86_64','a b',';not-a-command'])
        self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(p.stdout.splitlines(),['--user','--scope','--quiet','-p','CPUQuota=200%','-p','MemoryMax=4G','nice','-n','15','qemu-system-x86_64','a b',';not-a-command'])
    def test_cap_failure_has_no_uncapped_retry(self):
        self.assertEqual(self.invoke('exit 73',['true']).returncode,73)
    def test_missing_command(self):
        p=subprocess.run([str(ROOT/'scripts/qemu-capped.sh')],capture_output=True)
        self.assertEqual(p.returncode,2)
