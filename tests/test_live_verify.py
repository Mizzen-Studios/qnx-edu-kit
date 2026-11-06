import importlib.util,json,os,pathlib,subprocess,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('live_verify',ROOT/'scripts/live_verify.py')
live=importlib.util.module_from_spec(spec);spec.loader.exec_module(live)
class FreshOnly(unittest.TestCase):
    def run_gate(self,bundle):
        return subprocess.run(['python3',str(ROOT/'scripts/live_verify.py')],capture_output=True,text=True,env={**os.environ,'EDU_LIVE_BUNDLE':str(bundle),'EDU_NATIVE_LEASE':'granted'})
    def test_stale_source_rejected_before_boot(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d);(p/'manifest.json').write_text(json.dumps({'sources':{}}))
            result=self.run_gate(p);self.assertEqual(result.returncode,2);self.assertIn('source hashes differ',result.stdout)
    def test_corrupt_image_rejected_before_boot(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d);(p/'ifs-edu-followup10.bin').write_bytes(b'not image')
            (p/'manifest.json').write_text(json.dumps({'sources':live.sources(),'image_sha256':'wrong'}))
            result=self.run_gate(p);self.assertEqual(result.returncode,2);self.assertIn('image hash mismatch',result.stdout)
    def test_no_transcript_replay_argument(self):
        result=subprocess.run(['python3',str(ROOT/'scripts/live_verify.py'),'--transcript','saved.log'],capture_output=True)
        self.assertEqual(result.returncode,2)
    def test_no_polling_resmgr_fallback(self):
        s=(ROOT/'native/edu_resmgr.c').read_text();self.assertIn('InterruptAttachThread(',s);self.assertIn('InterruptWait(',s)
        self.assertNotIn('nanosleep(',s);self.assertNotIn('Polling only',s)
