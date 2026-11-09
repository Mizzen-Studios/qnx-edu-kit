import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('learner_lab', ROOT/'scripts/learner_lab.py')
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)

class LearnerTests(unittest.TestCase):
    def output(self, row='010000ed write=12345678 read=edcba987', rc=0):
        return ('EDU TARGET QNX 8.0 x86_64\nLEARNER_BIND source=s binary=b\n'
                f'LEARNER_MMIO id={row}\nLEARNER_RC={rc}\n')

    def test_actual_readback_and_exit_required(self):
        m = {'source_sha256':'s', 'binary_sha256':'b'}
        self.assertTrue(all(lab.oracle(self.output(),m).values()))
        self.assertTrue(all(lab.oracle(self.output().replace('QNX 8.0 ','QNX 8.0.0 '),m).values()))
        self.assertFalse(all(lab.oracle(self.output().replace('QNX 8.0 ','Linux 8.0 '),m).values()))
        for output in ['EDU STEP3 PASS\n', self.output(rc=1),
                       self.output('010000ed write=12345678 read=12345678'),
                       self.output('00000000 write=12345678 read=edcba987'),
                       self.output().replace('source=s','source=other'),
                       self.output()+'LEARNER_RC=0\n',
                       self.output()+'LEARNER_BIND source=s binary=b\n',
                       self.output().replace('LEARNER_BIND source=s binary=b\n','')+'LEARNER_BIND source=s binary=b\n']:
            self.assertFalse(all(lab.oracle(output,m).values()))

    def test_native_timeout_is_bounded_before_any_launch(self):
        for value in (0, -1, 901, True, 1.5):
            with self.assertRaisesRegex(ValueError, "1..900"):
                lab.run("missing", "missing", "missing", "missing", timeout=value)

    def test_reference_manifest_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p/'manifest.json').write_text(json.dumps({'sources':{},'image_sha256':'reference'}))
            with self.assertRaisesRegex(ValueError,'not a learner'):
                lab.verify_inputs(p/'source.c',p)

    def test_init_copies_todo_and_preserves_edits(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = lab.init(tmp)
            self.assertIn('implementation TODO',source.read_text())
            source.write_text('learner edit')
            with self.assertRaises(ValueError): lab.init(tmp)
            self.assertEqual(source.read_text(),'learner edit')

    def test_build_compiles_snapshot_and_rebuilds_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            source = p/'main.c'; source.write_text('learner source')
            buildfile = p/'bsp.build'; buildfile.write_text('learner BSP')
            out = p/'out'
            calls = []
            def execute(command, **kwargs):
                calls.append(command)
                if command[3] == 'learner-build':
                    self.assertEqual((out/'learner-source.c').read_text(),'learner source')
                    (out/'learner_bin').write_bytes(b'\x7fELFtarget')
                else:
                    self.assertIn('LEARNER_RC=$?',(out/'learner-start.sh').read_text())
                    (out/'learner.ifs').write_bytes(b'new image')
            with patch.object(lab.subprocess,'run',side_effect=execute):
                m = lab.build(source,out,p/'env.sh',buildfile,p)
            self.assertEqual(len(calls),2)
            self.assertEqual(m['source_sha256'],lab.sha(source))
            self.assertEqual(m['image_sha256'],lab.sha(out/'learner.ifs'))
            lab.verify_inputs(source,out)

    def test_native_refuses_free_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            disk = p/'disk'; disk.write_text('external disk')
            with patch.object(lab,'verify_inputs',return_value={}), patch.dict(lab.os.environ,
                    {'EDU_NATIVE_LEASE':'granted','EDU_NATIVE_LOCK':str(p/'lock')}):
                with self.assertRaisesRegex(ValueError,'lock is free'):
                    lab.run(p/'source',p,disk,p/'receipt')

    def test_identified_qemu_is_killed_on_cap_rejection(self):
        # Structural guard: ownership assignment must precede validation, and
        # finally must use owned_pid rather than the possibly unset cap object.
        source = (ROOT/'scripts/learner_lab.py').read_text()
        self.assertLess(source.index('owned_pid = pid'),source.index('cap = caps(pid)'))
        cleanup = source.split('    finally:',1)[1]
        self.assertIn('os.kill(owned_pid,signal.SIGTERM)',cleanup)
        self.assertIn('os.kill(owned_pid,signal.SIGKILL)',cleanup)
        self.assertIn('proc.wait(10)',cleanup)

    def test_standalone_sdk_copy_allows_external_build(self):
        with patch.object(lab,'REPO_COPY',False):
            self.assertEqual(lab.external(ROOT/'sdk-output'),ROOT/'sdk-output')
            with self.assertRaisesRegex(ValueError,'repository copy'):
                lab.init(ROOT/'sdk-output')

    def test_checkout_outputs_forbidden(self):
        with self.assertRaises(ValueError): lab.external(ROOT/'.build/learner')

    def test_tampered_inputs_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            files = {'main.c':'source_sha256','learner-source.c':'source_sha256',
                     'learner_bin':'binary_sha256','learner.ifs':'image_sha256',
                     'learner-start.sh':'startup_sha256'}
            m = {'kind':'learner-step3-v1'}
            for name,key in files.items():
                (p/name).write_text(key)
                m[key] = lab.sha(p/name)
            (p/'manifest.json').write_text(json.dumps(m))
            lab.verify_inputs(p/'main.c',p)
            for name in files:
                old = (p/name).read_text()
                (p/name).write_text('tampered')
                with self.assertRaisesRegex(ValueError,'mismatch'):
                    lab.verify_inputs(p/'main.c',p)
                (p/name).write_text(old)

if __name__=='__main__': unittest.main()
