import os,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PathPreflight(unittest.TestCase):
    def invoke(self,env):
        return subprocess.run(['sh',str(ROOT/'scripts/learner-path-preflight.sh')],env=env,capture_output=True,text=True)
    def test_unset_paths_block_before_creation(self):
        env={k:v for k,v in os.environ.items() if not k.startswith('EDU_')}
        result=self.invoke(env);self.assertEqual(result.returncode,2);self.assertIn('BLOCKED: set EDU_CONTROLLER',result.stderr)
    def test_writable_external_host_paths_and_permission_diagnostic(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);controller=base/'controller.py';controller.write_text('# HOST fixture, never executed')
            share=base/'share';share.mkdir();stock=base/'stock';stock.mkdir()
            env={**os.environ,'EDU_CONTROLLER':str(controller),'EDU_SHARE':str(share),'EDU_STOCK':str(stock),'EDU_SDP_ENV':'/external/sdk-guest/env.sh','EDU_NATIVE_LEASE':str(base/'lock')}
            p=self.invoke(env);self.assertEqual(p.returncode,0,p.stderr);self.assertIn('HOST paths only',p.stdout)
            share.chmod(0o500)
            try:
                if os.geteuid()!=0:
                    p=self.invoke(env);self.assertEqual(p.returncode,2);self.assertIn('writable/searchable',p.stderr)
            finally:share.chmod(0o700)
            self.assertFalse((base/'lock').exists())
    def test_placeholders_do_not_reach_mkdir(self):
        env={**os.environ,**{k:'/absolute/path/to/replace' for k in ['EDU_CONTROLLER','EDU_SHARE','EDU_STOCK','EDU_SDP_ENV','EDU_NATIVE_LEASE']}}
        p=self.invoke(env);self.assertEqual(p.returncode,2);self.assertIn('placeholder',p.stderr)
