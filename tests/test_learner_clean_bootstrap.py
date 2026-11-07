import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import subprocess

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('clean', ROOT/'scripts/learner_clean_preflight.py')
clean = importlib.util.module_from_spec(spec)
spec.loader.exec_module(clean)

class CleanBootstrapTests(unittest.TestCase):
    def test_missing_sdk_is_blocked_not_native_pass(self):
        with tempfile.TemporaryDirectory() as d:
            r = clean.probe(Path(d)/'missing', Path(d)/'fresh')
            self.assertFalse(r['ready_for_clean_build_attempt'])
            self.assertEqual(r['native_acceptance'], 'NOT_RUN')
            self.assertEqual(r['portability'], 'UNVERIFIED')

    def test_existing_work_refused(self):
        with tempfile.TemporaryDirectory() as d:
            r = clean.probe(Path(d)/'missing', d)
            self.assertFalse(r['checks']['fresh_workspace'])

    def test_missing_licensed_component_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); env = p/'env'; env.write_text('# supplied SDK')
            response = subprocess.CompletedProcess([], 0, '/qcc\n/mkifs\n/mkqnximage\n'+d+'\n', '')
            with patch.object(clean.subprocess, 'run', return_value=response):
                r = clean.probe(env, p/'fresh')
            self.assertTrue(r['checks']['sdk_tools_present'])
            self.assertFalse(r['checks']['licensed_components_present'])
            self.assertFalse(r['ready_for_clean_build_attempt'])

    def test_real_qnx8_layout_is_accepted_without_usr_prefix(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); env = p/'env'; env.write_text('# supplied SDK')
            for name in ['x86_64/boot/sys/startup-x86', 'x86_64/boot/sys/procnto-smp-instr',
                         'x86_64/sbin/pci-server', 'x86_64/lib/libpci.so']:
                file = p/name; file.parent.mkdir(parents=True, exist_ok=True); file.touch()
            response = subprocess.CompletedProcess([], 0, '/qcc\n/mkifs\n/mkqnximage\n'+d+'\n', '')
            with patch.object(clean.subprocess, 'run', return_value=response):
                r = clean.probe(env, p/'fresh')
            self.assertTrue(r['ready_for_clean_build_attempt'])
            self.assertEqual(r['native_acceptance'], 'NOT_RUN')
            self.assertEqual(r['portability'], 'UNVERIFIED')

    def test_probe_does_not_launch_or_install(self):
        source = (ROOT/'scripts/learner_clean_preflight.py').read_text()
        self.assertNotIn('Popen(', source)
        self.assertNotIn('--activate', source)
        self.assertIn('timeout=30', source)
