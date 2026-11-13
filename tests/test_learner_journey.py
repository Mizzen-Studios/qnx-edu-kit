import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import learner_journey as journey
class Journey(unittest.TestCase):
    def phases(self):
        rows=[]
        for i,(stage,status) in enumerate([('step3','FAIL'),('step3','PASS'),('step6','PASS')]):
            rows.append(dict(stage=stage,status=status,checks={'device_readback':i!=0,'exit_zero':True,'serial_bytes_verified':True},mmio=[('010000ed','12345679','edcba986')] if i==0 else [],source_sha256=str(i),image_sha256='shared-image',disk_sha256='shared-disk',build_started=i*10+1,started=i*10+2,finished=i*10+3))
        return rows
    def test_expected_failure_is_not_ordinary_setup_failure(self):
        rows=self.phases();self.assertTrue(journey.chain(rows));rows[0]['checks']['exit_zero']=False
        with self.assertRaises(ValueError):journey.chain(rows)
    def test_no_prebuilt_correction_or_mixed_stock(self):
        rows=self.phases();rows[1]['build_started']=0
        with self.assertRaises(ValueError):journey.chain(rows)
        rows=self.phases();rows[2]['disk_sha256']='another'
        with self.assertRaises(ValueError):journey.chain(rows)
    def test_wrong_order_and_no_correction_fail(self):
        rows=self.phases();rows[1]['source_sha256']=rows[0]['source_sha256']
        with self.assertRaises(ValueError):journey.chain(rows)
        rows=self.phases();rows[2]['started']=0
        with self.assertRaises(ValueError):journey.chain(rows)
