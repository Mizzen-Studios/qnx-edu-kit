import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('learner_finish', ROOT/'scripts/learner_lab.py')
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)

class FinishTests(unittest.TestCase):
    def test_finish_requires_bound_normal_io_and_irq(self):
        manifest = {'source_sha256':'s','binary_sha256':'b'}
        output = ('LEARNER_BIND source=s binary=b\nEDU TARGET QNX 8.0.0 x86_64\n'
                  'EDU RESMGR IRQ completion=1 input=10 result=3628800 ack=00000000\n'
                  'LEARNER_DEV_EDU write_rc=0 read_rc=0 result=3628800\nLEARNER_RC=0\n')
        self.assertTrue(all(lab.dev_edu_oracle(output,manifest).values()))
        for altered in (output.replace('source=s','source=other'),
                        output.replace('input=10','input=9'),
                        output.replace('write_rc=0','write_rc=1'),
                        output.replace('read_rc=0','read_rc=1'),
                        output.replace('ack=00000000','ack=00000001'),
                        output.replace('result=3628800','result=0'),
                        output.replace('EDU TARGET QNX','EDU TARGET Linux'),
                        output+'LEARNER_RC=0\n',
                        'REFERENCE STEP6 PASS\n',
                        '\n'.join(line for line in output.splitlines() if not line.startswith('EDU RESMGR IRQ'))):
            self.assertFalse(all(lab.dev_edu_oracle(altered,manifest).values()))

    def test_finish_and_bar_manifests_are_not_interchangeable(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            for kind,stage in [('learner-step3-v1','step6'),('learner-dev-edu-v1','step3'),('reference-v1','step6')]:
                (p/'manifest.json').write_text(json.dumps({'kind':kind}))
                with self.assertRaisesRegex(ValueError,'not a learner'):
                    lab.verify_inputs(p/'main.c',p,stage)

    def test_finish_initializes_actual_todo_and_preserves_edits(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=lab.init(tmp,'step6')
            self.assertIn('registration TODO',source.read_text())
            source.write_text('own edited registration')
            with self.assertRaises(ValueError):lab.init(tmp,'step6')
            self.assertEqual(source.read_text(),'own edited registration')

    def test_finish_wrapper_uses_real_device_io(self):
        script=lab.startup('step6','source','binary')
        self.assertIn('> /dev/edu',script)
        self.assertIn('observed=$(cat /dev/edu)',script)
        self.assertIn('wait "$learner_pid"',script)
        self.assertNotIn('edu_accept',script)
        self.assertNotIn('LEARNER_MMIO',script)

if __name__ == '__main__': unittest.main()
