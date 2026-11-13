import sys,json,tempfile,unittest,hashlib
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import learner_stock as stock
import learner_session as session
import learner_lab as lab
class StockAdapter(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.base=Path(self.tmp.name)
    def bundle(self):
        b=self.base/'bundle';b.mkdir();source=self.base/'main.c';source.write_text('own test source')
        for n,data in [('learner-source.c',source.read_bytes()),('learner.o',b'own object'),('learner_bin',bytes([127,69,76,70])+b'host fixture')]: (b/n).write_bytes(data)
        m=dict(kind=stock.kind('step6'),route='stock-reuse-v1',image_generation=False,source_sha256=lab.sha(source),object_sha256=lab.sha(b/'learner.o'),binary_sha256=lab.sha(b/'learner_bin'),observability='pulse-slog2-v1')
        stock.save(b/'manifest.json',m);return source,b,m
    def test_custom_ifs_manifest_cannot_be_relabelled(self):
        source,b,m=self.bundle();m['kind']='learner-dev-edu-v1';stock.save(b/'manifest.json',m)
        with self.assertRaises(ValueError): stock.verify_inputs(source,b,'step6')
    def test_changed_source_and_binary_rejected(self):
        source,b,m=self.bundle();source.write_text('different edit')
        with self.assertRaises(ValueError):stock.verify_inputs(source,b,'step6')
    def test_unapproved_stock_fails_before_any_qemu(self):
        source,b,m=self.bundle();root=self.base/'unapproved';root.mkdir()
        with patch.dict('os.environ',{'EDU_NATIVE_LEASE':'granted'}),patch.object(stock.subprocess,'Popen') as launch:
            with self.assertRaises(ValueError):stock.run(source,b,root,self.base/'native','step6')
            launch.assert_not_called()
    def test_log_without_byteproof_and_caps_cannot_pass(self):
        _,b,m=self.bundle();c=self.base/'control';c.mkdir()
        r=stock.checks('',m,c,{'stopped_reaped':True,'status':'REQUESTED_STOP','caps':{'fake':'cap'}})
        self.assertFalse(r['serial_bytes_verified']);self.assertFalse(r['caps_exact']);self.assertFalse(all(r.values()))
    def test_readback_corruption_rejected(self):
        _,b,m=self.bundle();c=self.base/'control';c.mkdir();stock.save(c/'003-readback.result.json',{'status':'DONE','output':'STOCK_BYTES_BEGIN'+chr(10)+'00'+chr(10)+'STOCK_BYTES_END'})
        self.assertFalse(stock.byte_check(c,m))
    def test_raw_serial_crlf_is_bound_without_normalization(self):
        folder=self.base/'observation';control=folder/'native.control';control.mkdir(parents=True)
        raw='EDU TARGET QNX 8.0.0 x86pc\r\nIRQ ack=00000000\r\r\n'
        stock.save(control/'004-observe.result.json',dict(status='DONE',output=raw))
        (folder/'native.log').write_bytes(raw.encode())
        self.assertEqual(session.stock_observed_output(folder),raw)
        (folder/'native.log').write_bytes(raw.replace('ack=00000000','ack=00000001').encode())
        with self.assertRaisesRegex(ValueError,'stock log changed'):session.stock_observed_output(folder)
        (folder/'native.log').write_bytes(raw.replace('\r','').encode())
        with self.assertRaisesRegex(ValueError,'stock log changed'):session.stock_observed_output(folder)
    def test_offline_revalidation_rejects_no_own_observation(self):
        w=self.base/'own';session.create(w)
        with patch.object(session.subprocess,'run') as launch:
            with self.assertRaisesRegex(ValueError,'requires own blocked'):session.revalidate(w,'missing')
            launch.assert_not_called()
    def test_cockpit_stock_path_and_no_custom_relabel(self):
        w=self.base/'own';session.create(w);page=(w/'cockpit.html').read_text()
        self.assertIn('Working stock route',page);self.assertIn('--stock',page);self.assertIn('Historical CUSTOM-IFS',page)
        self.assertNotIn('stock native PASS',page)
if __name__=='__main__':unittest.main()
