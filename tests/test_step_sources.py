import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('step_sources', ROOT/'tools/step_sources.py')
steps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(steps)


class StepSources(unittest.TestCase):
    def test_twelve_snapshots_match_unchanged_e1(self):
        for name, expected in steps.snapshots().items():
            self.assertEqual((ROOT/name).read_text(), expected, name)
        receipt = json.loads((ROOT/'docs/acceptance/native-20261107/receipt.json').read_text())
        for name, expected in receipt['sources'].items():
            self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), expected)

    def test_solutions_stop_at_their_boundary(self):
        for n in range(1, 5):
            source = (ROOT/f'steps/step{n}/solution/main.c').read_text()
            self.assertIn(f'EDU STEP{n} PASS', source)
            self.assertNotIn(f'EDU STEP{n+1} PASS', source)
            self.assertNotIn('InterruptAttachThread(', source)
            self.assertNotIn('edu_probe.c"', source)
        source = (ROOT/'steps/step5/solution/main.c').read_text()
        self.assertIn('InterruptAttachThread(', source)
        self.assertIn('edu_dma_roundtrip(h,bdf,r)', source)
        source = (ROOT/'steps/step6/solution/main.c').read_text()
        self.assertIn('InterruptWait(', source)
        self.assertIn('resmgr_attach(', source)
        self.assertNotIn('edu_resmgr.c"', source)

    def test_starters_refuse_the_missing_boundary(self):
        for n in range(1, 7):
            source = (ROOT/f'steps/step{n}/starter/main.c').read_text()
            self.assertIn('TODO:', source)
            self.assertIn('BLOCKED:', source)
            self.assertNotIn(f'EDU STEP{n} PASS', source)
        self.assertNotIn('resmgr_attach(', (ROOT/'steps/step6/starter/main.c').read_text())

    def test_snapshot_drift_rejected_before_live_gate(self):
        # Isolated tiny source checkout, never a fixture accepted as live output.
        with tempfile.TemporaryDirectory(dir=ROOT.parent) as d:
            copy = Path(d)
            for folder in ('native', 'steps', 'tools', 'scripts'):
                (copy/folder).mkdir()
            for name in steps.snapshots():
                dest = copy/name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT/name, dest)
            for path in (ROOT/'native').glob('*'):
                if path.is_file():
                    shutil.copyfile(path, copy/'native'/path.name)
            shutil.copyfile(ROOT/'tools/step_sources.py', copy/'tools/step_sources.py')
            shutil.copyfile(ROOT/'scripts/check-step.sh', copy/'scripts/check-step.sh')
            path = copy/'steps/step4/solution/main.c'
            path.write_text(path.read_text().replace('r[2]=10;', 'r[2]=11;'))
            result = subprocess.run(['sh', str(copy/'scripts/check-step.sh'), '4'], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('E1-derived source contract differs', result.stderr)
            # No live_verify.py was copied: reaching a guest path would fail this assertion.
            self.assertNotIn('live_verify.py', result.stderr)

    @unittest.skipUnless(shutil.which('cc'), 'host C compiler not installed')
    def test_step1_starter_host_syntax_only(self):
        subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', '-fsyntax-only',
                        str(ROOT/'steps/step1/starter/main.c')], check=True, capture_output=True)

    def test_warning_inside_first_step_and_no_can_course(self):
        text = (ROOT/'codelab/codelab.md').read_text()
        first = text.split('## 1. ', 1)[1].split('## 2. ', 1)[0]
        self.assertIn('PRIVATE DRAFT', first)
        self.assertIn('QSTI provenance remains unverified', first)
        self.assertIn('unmeasured planning estimates', first)
        self.assertNotIn('candump', text)
        self.assertNotIn('kvaser', text)
