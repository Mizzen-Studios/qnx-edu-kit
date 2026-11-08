import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import learner_session as cockpit
import learner_setup as setup


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work=Path(self.temp.name)/'own'
        cockpit.create(self.work)

    def predict(self,stage='step3',text='wrong complement should fail'):
        _,data=cockpit.session(self.work)
        file=Path(self.temp.name)/'notes.json'
        file.write_text(json.dumps(dict(session_id=data['id'],stage=stage,prediction=text)))
        cockpit.notes(self.work,file)

    def test_own_source_notes_and_no_overwrite(self):
        source=self.work/'step3/main.c'
        source.write_text('own edit')
        self.predict(text='<script>alert(1)</script>')
        self.assertEqual(source.read_text(),'own edit')
        self.assertIn('&lt;script&gt;', (self.work/'cockpit.html').read_text())
        with self.assertRaises(ValueError):cockpit.create(self.work)
        self.assertEqual(cockpit.session(self.work)[1]['notes']['step3']['prediction'],'<script>alert(1)</script>')

    def test_permission_notes_export_without_native_badge(self):
        self.predict(stage='permission',text='IO deny should report EPERM; allow only subrange0')
        out=Path(self.temp.name)/'permission-pack'
        cockpit.export(self.work,out)
        data=json.loads((out/'session.json').read_text())
        self.assertIn('EPERM',data['notes']['permission']['prediction'])
        self.assertEqual(data['attempts'],[])
        self.assertIn('not pathname policy',(out/'cockpit.html').read_text())

    def test_shared_can_supplement_is_not_native_acceptance(self):
        folder=self.work/'supplemental';folder.mkdir()
        (folder/'run.json').write_bytes((ROOT/'docs/acceptance/ability-20261108/run.json').read_bytes())
        out=Path(self.temp.name)/'shared-only'
        manifest=json.loads(cockpit.export(self.work,out).read_text())
        self.assertEqual(json.loads((out/'session.json').read_text())['attempts'],[])
        self.assertTrue(all(x['validation']=='CURRENT_STAGE_NOT_VALIDATED' for x in manifest['current_sources'].values()))

    def test_reference_notes_cannot_import(self):
        file=Path(self.temp.name)/'reference.json'
        file.write_text(json.dumps(dict(session_id='reference',stage='step3',prediction='PASS')))
        with self.assertRaisesRegex(ValueError,'another session'):cockpit.notes(self.work,file)

    def test_prediction_gate_and_blocked_run_retained(self):
        args=argparse.Namespace(disk='/missing')
        with self.assertRaisesRegex(ValueError,'prediction'):cockpit.attempt(self.work,'step3','run',args)
        self.predict()
        with patch.object(cockpit.subprocess,'run',return_value=subprocess.CompletedProcess([],2)):
            self.assertEqual(cockpit.attempt(self.work,'step3','run',args),2)
        record=cockpit.session(self.work)[1]['attempts'][0]
        self.assertEqual((record['label'],record['status']),('HOST','BLOCKED'))
        self.assertTrue((self.work/'attempts'/record['id']/'command.log').exists())
        self.assertTrue((self.work/'attempts'/record['id']/'main.c').exists())

    def test_zero_exit_without_native_receipt_never_passes(self):
        self.predict()
        with patch.object(cockpit.subprocess,'run',return_value=subprocess.CompletedProcess([],0)):
            self.assertEqual(cockpit.attempt(self.work,'step3','run',argparse.Namespace(disk='/missing')),2)

    def native_fixture(self,wrong=False,stage='step3'):
        _,data=cockpit.session(self.work)
        source=self.work/stage/'main.c'
        build=dict(id='0001-build',stage=stage,action='build',status='PASS',label='HOST',started=1,returncode=0,source_sha256=cockpit.lab.sha(source))
        folder=self.work/'attempts'/'0002-run';folder.mkdir(parents=True)
        shutil=__import__('shutil');shutil.copyfile(source,folder/'main.c')
        bundle=self.work/'attempts'/build['id']/'bundle';bundle.mkdir(parents=True)
        shutil.copyfile(source,bundle.parent/'main.c')
        files={'learner-source.c':source.read_bytes(),'learner_bin':b'ELF host fixture','learner.ifs':b'host fixture','learner-start.sh':b'host fixture'}
        for name,value in files.items():(bundle/name).write_bytes(value)
        manifest=dict(kind=cockpit.lab.manifest_kind(stage),source_sha256=cockpit.lab.sha(source),binary_sha256=cockpit.lab.sha(bundle/'learner_bin'),image_sha256=cockpit.lab.sha(bundle/'learner.ifs'),startup_sha256=cockpit.lab.sha(bundle/'learner-start.sh'))
        cockpit.save(bundle/'manifest.json',manifest)
        disk=Path(self.temp.name)/'disk';disk.write_text('host fixture only')
        output='EDU TARGET QNX 8.0 x86_64\nLEARNER_BIND source='+manifest['source_sha256']+' binary='+manifest['binary_sha256']+'\n'
        if stage=='step3':output+='LEARNER_MMIO id=010000ed write='+('12345679 read=edcba986' if wrong else '12345678 read=edcba987')+'\n'
        else:output+='EDU RESMGR IRQ completion=1 input=10 result=3628800 ack=00000000\nLEARNER_DEV_EDU write_rc=0 read_rc=0 result=3628800\n'
        output+='LEARNER_RC=0\n'
        (folder/'native.log').write_text(output)
        oracle=cockpit.lab.oracle if stage=='step3' else cockpit.lab.dev_edu_oracle
        checks=oracle(output,manifest)
        checks.update(dict.fromkeys(('bounded_completion','inputs_unchanged_after_boot','disk_unchanged','qemu_reaped'),True))
        cockpit.save(folder/'native.json',dict(manifest,checks=checks,success=not wrong,caps={'fixture':True},disk_sha256=cockpit.lab.sha(disk),run_driver_sha256=cockpit.lab.sha(ROOT/'scripts/learner_lab.py')))
        record=dict(id=folder.name,stage=stage,action='run',status='FAIL' if wrong else 'PASS',label='nativefresh',started=2,source_sha256=build['source_sha256'],returncode=1 if wrong else 0,command=['--disk',str(disk)])
        data['attempts']=[build,record];cockpit.save(self.work/'session.json',data)
        return folder,record

    def test_existing_oracle_wrong_fails_despite_app_zero_correct_passes(self):
        folder,record=self.native_fixture(wrong=True)
        cockpit.validate_native(self.work,record,folder)
        receipt=json.loads((folder/'native.json').read_text());receipt['success']=True
        cockpit.save(folder/'native.json',receipt)
        with self.assertRaisesRegex(ValueError,'status/exit'):cockpit.validate_native(self.work,record,folder)

    def test_bool_success_and_bool_exit_rejected(self):
        folder,record=self.native_fixture()
        path=folder/'native.json'
        original=path.read_text()
        receipt=json.loads(original);receipt['success']=1
        cockpit.save(path,receipt)
        with self.assertRaisesRegex(ValueError,'wrong type'):
            cockpit.validate_native(self.work,record,folder)
        path.write_text(original);record['returncode']=False
        with self.assertRaisesRegex(ValueError,'wrong type'):
            cockpit.validate_native(self.work,record,folder)

    def test_pack_has_own_source_binary_image_disk_and_tamper_fails(self):
        folder,record=self.native_fixture()
        cockpit.render(self.work)
        out=Path(self.temp.name)/'pack'
        manifest=json.loads(cockpit.export(self.work,out).read_text())
        for suffix in ('main.c','learner_bin','learner.ifs','native.log'):
            self.assertTrue(any(k.endswith(suffix) for k in manifest['files']))
        self.assertTrue(any(k.startswith('disks/') for k in manifest['files']))
        (folder/'native.log').write_text('reference PASS')
        with self.assertRaises(ValueError):cockpit.export(self.work,Path(self.temp.name)/'bad-pack')
        self.assertTrue((Path(self.temp.name)/'bad-pack/INCOMPLETE.txt').exists())

    def test_build_only_export_revalidates_binary(self):
        self.native_fixture()
        _,data=cockpit.session(self.work)
        data['attempts']=data['attempts'][:1]
        cockpit.save(self.work/'session.json',data)
        cockpit.export(self.work,Path(self.temp.name)/'good-build')
        (self.work/'attempts/0001-build/bundle/learner_bin').write_text('CORRUPT')
        with self.assertRaisesRegex(ValueError,'binary_sha256'):
            cockpit.export(self.work,Path(self.temp.name)/'bad-build')

    def test_metadata_cannot_bypass_native_validation(self):
        folder,record=self.native_fixture()
        _,original=cockpit.session(self.work)
        import copy
        for key,value in [('label','HOST'),('status','BLOCKED'),('action','build')]:
            with self.subTest(key=key):
                data=copy.deepcopy(original);data['attempts'][1][key]=value
                cockpit.save(self.work/'session.json',data)
                with self.assertRaisesRegex(ValueError,'mismatch'):
                    cockpit.export(self.work,Path(self.temp.name)/('bad-'+key))
        data=copy.deepcopy(original);data['attempts'][1]['label']='HOST'
        cockpit.save(self.work/'session.json',data)
        (folder/'native.log').write_text('CORRUPT')
        with self.assertRaises(ValueError):
            cockpit.export(self.work,Path(self.temp.name)/'corrupt-host')

    def test_invalid_metadata_and_missing_receipt_fail_closed(self):
        folder,record=self.native_fixture()
        _,original=cockpit.session(self.work)
        import copy
        for key,value in [('action','other'),('stage','other'),('status','other'),('returncode',True)]:
            with self.subTest(key=key):
                data=copy.deepcopy(original);data['attempts'][1][key]=value
                cockpit.save(self.work/'session.json',data)
                with self.assertRaises((ValueError,KeyError)):
                    cockpit.export(self.work,Path(self.temp.name)/('invalid-'+key))
        cockpit.save(self.work/'session.json',original)
        (folder/'native.json').unlink()
        with self.assertRaises(OSError):
            cockpit.export(self.work,Path(self.temp.name)/'missing-json')

    def test_current_edit_keeps_history_but_not_current_pass(self):
        folder,record=self.native_fixture()
        (self.work/'step3/main.c').write_text('a newer edit')
        cockpit.render(self.work)
        page=(self.work/'cockpit.html').read_text()
        self.assertIn('0002-run: PASS',page)
        self.assertIn('HISTORICAL — SOURCE MISMATCH',page)
        self.assertIn('step3: CURRENT_STAGE_NOT_VALIDATED',page)
        manifest=json.loads(cockpit.export(self.work,Path(self.temp.name)/'historic').read_text())
        self.assertEqual(manifest['current_sources']['step3']['validation'],'CURRENT_STAGE_NOT_VALIDATED')
        self.assertEqual(manifest['current_sources']['step3']['source_sha256'],cockpit.lab.sha(self.work/'step3/main.c'))
        self.assertTrue(any(k.startswith('disks/') for k in manifest['files']))

    def test_dev_edu_irq_ack_is_separate_required_check(self):
        folder,record=self.native_fixture(stage='step6')
        cockpit.validate_native(self.work,record,folder)
        path=folder/'native.log';path.write_text(path.read_text().replace('ack=00000000','ack=00000001'))
        with self.assertRaisesRegex(ValueError,'oracle'):cockpit.validate_native(self.work,record,folder)

    def test_setup_no_sdk_execution_without_explicit_probe(self):
        with patch.object(setup.clean,'probe') as probe:
            result=setup.plan('/absent/sdk','/absent/bsp','/absent/qemu',self.work/'new')
        probe.assert_not_called()
        self.assertFalse(result['ready_for_attempt'])
        self.assertEqual(result['native_acceptance'],'NOT_RUN')
        self.assertIn('learner_bootstrap.sh','\n'.join(result['commands']))
        self.assertNotIn('/home/ubuntu/qnx-host','\n'.join(result['commands']))
