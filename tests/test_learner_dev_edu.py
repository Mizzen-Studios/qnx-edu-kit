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

    def test_new_feature_observables_required_not_reference_strings(self):
        manifest={'source_sha256':'s','binary_sha256':'b','observability':'pulse-slog2-v1'}
        rows=('LEARNER_BIND source=s binary=b\nEDU TARGET QNX 8.0.0 x86_64\n'
              'EDU RESMGR SLOG2 configured pages=1 limit=8\n'
              'EDU RESMGR PULSE sequence=1 input=10 result=3628800 sent=1 received=1 owner=same-thread\n'
              'EDU RESMGR IRQ completion=1 input=10 result=3628800 ack=00000000\n'
              'LEARNER_DEV_EDU write_rc=0 read_rc=0 result=3628800\n'
              'LEARNER_SLOG2_BEGIN\n'
              'timestamp EDU_EVENT irq sequence=1 input=10 result=3628800 ack=00000000\n'
              'timestamp EDU_EVENT pulse sequence=1 input=10 result=3628800\n'
              'LEARNER_SLOG2_END rc=0\nLEARNER_RC=0\n')
        self.assertTrue(all(lab.dev_edu_oracle(rows,manifest).values()))
        for altered in (rows.replace('sent=1','sent=0'),rows.replace('received=1','received=0'),
                        rows.replace('sequence=1','sequence=2'),rows.replace('pages=1','pages=2'),
                        rows.replace('LEARNER_SLOG2_END rc=0','LEARNER_SLOG2_END rc=1'),
                        rows.replace('EDU_EVENT pulse','FAKE pulse'),
                        rows+rows,rows.replace('owner=same-thread','owner=worker')):
            self.assertFalse(all(lab.dev_edu_oracle(altered,manifest).values()))

    def test_pulse_is_same_owner_and_ack_precedes_publication(self):
        source=(ROOT/'native/edu_resmgr.c').read_text()
        for call in ['ChannelCreate(_NTO_CHF_PRIVATE)', 'ConnectAttach(', 'MsgSendPulse(',
                     'MsgReceivePulse(', 'ConnectDetach(', 'ChannelDestroy(', 'SLOG2_INFO', 'EDU_LOG_LIMIT 8U', 'SLOG2_LIMIT_RETRIES', 'config.max_retries = 3']:
            self.assertIn(call,source)
        self.assertIn('SLOG2_LIMIT_RETRIES',source)
        self.assertIn('config.max_retries = 3',source)
        self.assertNotIn('pthread_create',source)
        self.assertLess(source.index('regs[0x64/4] = pending'),source.index('handoff_error = irq_to_dispatch'))
        self.assertLess(source.index('handoff_error = irq_to_dispatch'),source.index('++irq_completions'))

    def test_finite_trace_capture_uses_only_already_present_tools(self):
        script=lab.startup('step6','source','binary')
        self.assertIn('command -v tracelogger',script)
        self.assertIn('tracelogger -s1 -S64K -k1 -b1',script)
        self.assertIn('wait "$trace_pid"',script)
        self.assertNotIn('slog2info -w',script)
        self.assertNotIn('tracelogger -c',script)
        driver=(ROOT/'scripts/learner_lab.py').read_text()
        self.assertLess(driver.index('trace, trace_bytes = trace_observation(output)'), driver.index('if trace_bytes is not None:'))
        self.assertIn('optional_trace=trace',driver)
        observed,data=lab.trace_observation('LEARNER_TRACE OMITTED tools_absent\n')
        self.assertEqual(observed['status'],'OMITTED');self.assertIsNone(data)
        observed,data=lab.trace_observation('LEARNER_TRACE_BEGIN format=hex\n 00 ff 31\nLEARNER_TRACE_END rc=0\n')
        self.assertEqual(data,b'\x00\xff1');self.assertEqual(observed['bytes'],3)
        for text in ['GG', 'a', '00 '*65537]:
            with self.assertRaises(ValueError):lab.trace_observation('LEARNER_TRACE_BEGIN format=hex\n'+text+'\nLEARNER_TRACE_END rc=0\n')

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
