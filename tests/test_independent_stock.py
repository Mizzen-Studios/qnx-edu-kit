"""HOST/SYNTHETIC admission negatives. Never launches SDK/QEMU."""
import copy, hashlib, json, sys, tempfile, unittest, uuid
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import stock_provenance as p
import learner_stock as stock
import learner_lab as lab
import stock_lease
class IndependentStock(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.base=Path(self.tmp.name);self.root=self.base/'stock';self.root.mkdir()
  for n in p.ARTIFACTS: (self.root/n).write_text('SYNTHETIC HOST fixture '+n)
  (self.root/'disk-qemu.vmdk').write_text('RW 1 FLAT "disk-qemu" 0\n');(self.root/'disk-qemu').write_bytes(b'HOST synthetic'+b' '*512)
  (self.root/'options').write_text("OPT_RAM='512M'\nOPT_CPU='1'\n")
  (self.root/'qemu_options').write_text('-device edu\n');(self.root/'build.private.log').write_text('HOST fixture EOF, NOT SDK')
  tool=dict(path='/guest-only/tool',sha256='a'*64,version_rc=0,version_output_sha256='b'*64)
  self.m=dict(kind=p.KIND,id=str(uuid.uuid4()),recipe=p.COMMAND,builder_sha256=lab.sha(p.__file__),repo_commit='c'*40,repo_tree='d'*40,tools={n:tool for n in ('mkqnximage','mkifs','qcc')},tools_after={n:tool for n in ('mkqnximage','mkifs','qcc')},artifacts={n:lab.sha(self.root/n) for n in p.ARTIFACTS},inputs={'options':lab.sha(self.root/'options'),'snippets/qemu_options.edu':hashlib.sha256(b'-device edu\n').hexdigest()},log_sha256=lab.sha(self.root/'build.private.log'),returncode=0,eof=True,started=1,finished=2,project='/guest-only/project',stock='/guest-only/stock',environment_sha256='e'*64,provenance='HOST synthetic cooperative fixture')
  self.save()
 def save(self):
  (self.root/'stock-build.json').write_text(json.dumps(self.m))
  owner=dict(kind='edu-independent-stock-owner-v1',build_sha256=lab.sha(self.root/'stock-build.json'),stock=str(self.root),builder_sha256=lab.sha(p.__file__),caps={'cpu.max':'100000 100000','memory.max':'2147483648','memory.swap.max':'0'},stopped_reaped=True,queue_clear=True,foreign_qemu=0)
  (self.root/'stock-owner.json').write_text(json.dumps(owner));self.owner=lab.sha(self.root/'stock-owner.json')
 def verify(self): return p.verify(self.root,owner_sha256=self.owner)
 def test_split_namespace_and_explicit_trusted_digest(self):
  self.assertEqual(self.verify(),self.m)
  self.assertNotEqual(stock.stock_inputs(self.root,'independent-cooperative-v1',self.owner)['ifs.bin']['sha256'],stock.PINS['ifs.bin'])
 def test_self_consistent_manifest_without_handoff_rejected(self):
  with self.assertRaisesRegex(ValueError,'trusted owner'):p.verify(self.root)
 def test_unknown_optin(self):
  with self.assertRaises(ValueError):stock.stock_inputs(self.root,'anything',self.owner)
 def test_legacy_still_rejects_new_hashes(self):
  with self.assertRaises(ValueError):stock.stock_inputs(self.root)
 def test_all_artifact_mutations_rejected(self):
  for name in p.ARTIFACTS:
   with self.subTest(name=name):
    old=(self.root/name).read_bytes();(self.root/name).write_bytes(old+b'changed')
    with self.assertRaises(ValueError):self.verify()
    (self.root/name).write_bytes(old)
 def test_manifest_mutation_breaks_owner_binding(self):
  self.m['repo_commit']='f'*40;(self.root/'stock-build.json').write_text(json.dumps(self.m))
  with self.assertRaises(ValueError):self.verify()
 def test_mixed_owner(self):
  with self.assertRaises(ValueError):p.verify(self.root,owner_sha256='0'*64)
 def test_typed_owner_rejected(self):
  owner=json.loads((self.root/'stock-owner.json').read_text());owner['stopped_reaped']='true';(self.root/'stock-owner.json').write_text(json.dumps(owner));self.owner=lab.sha(self.root/'stock-owner.json')
  with self.assertRaises(ValueError):self.verify()
 def test_custom_recipe_and_schema(self):
  for key,value in [('kind','learner-dev-edu-v1'),('recipe',p.COMMAND+['--custom']),('eof',1),('returncode',False),('builder_sha256','0'*64)]:
   with self.subTest(key=key):
    old=self.m[key];self.m[key]=value;self.save()
    with self.assertRaises(ValueError):self.verify()
    self.m[key]=old
 def test_custom_or_extra_local_inputs(self):
  for name in ('snippets/ifs.lesson','startup.sh','../escape','/absolute'):
   self.m['inputs'][name]='a'*64;self.save()
   with self.assertRaises(ValueError):self.verify()
   del self.m['inputs'][name]
 def test_unsupported_qemu_options_even_rehashed(self):
  (self.root/'qemu_options').write_text('-device edu -net user\n');self.m['artifacts']['qemu_options']=lab.sha(self.root/'qemu_options');self.save()
  with self.assertRaises(ValueError):self.verify()
 def test_changed_tools_after(self):
  self.m['tools_after']=copy.deepcopy(self.m['tools']);self.m['tools_after']['qcc']['sha256']='f'*64;self.save()
  with self.assertRaises(ValueError):self.verify()
 def test_symlink_and_traversal(self):
  link=self.base/'alias';link.symlink_to(self.root,target_is_directory=True)
  with self.assertRaises(ValueError):p.verify(link,owner_sha256=self.owner)
  with self.assertRaises(ValueError):p.external(str(self.base)+'/../escape')
 def test_no_sdk_or_native_on_missing_finalization(self):
  (self.root/'stock-owner.json').unlink()
  with patch.object(stock.subprocess,'Popen') as launch:
   with self.assertRaises((ValueError,OSError)):stock.stock_inputs(self.root,'independent-cooperative-v1',self.owner)
   launch.assert_not_called()
 def test_queue_preflight_does_not_delete_original(self):
  q=self.base/'guest/shared/queue';q.mkdir(parents=True);job=q/'original.sh';job.write_text('preserve')
  self.assertFalse(stock_lease.queue_clear(self.base/'guest'));self.assertTrue(job.exists())
 def test_finalization_checks_queue_after_sdk_stop(self):
  import stock_build_owner as owner
  case=self.base/'case';control=case/'sdk-control';control.mkdir(parents=True)
  (control/'sdk-owner.json').write_text(json.dumps(dict(status='REQUESTED_STOP',stopped_reaped=True,caps=owner.CAPS)))
  with patch.object(owner,'no_qemu',return_value=True),patch.object(owner.lease,'queue_clear',return_value=False),patch.object(owner.provenance,'verify') as verify:
   with self.assertRaisesRegex(ValueError,'queue changed'):owner.finalize(case,__import__('unittest').mock.Mock())
   verify.assert_not_called();self.assertFalse((case/'stock/stock-owner.json').exists())
 def test_export_inventory_rejects_omission_and_incomplete(self):
  import learner_session as notebook,learner_journey as journey
  work=self.base/'own';notebook.create(work);dest=self.base/'export';notebook.export(work,dest)
  pack=json.loads((dest/'pack.json').read_text());data=notebook.session(work)[1]
  self.assertTrue(journey.validate_export_inventory(work,data,dest,pack))
  corrupt=copy.deepcopy(pack);del corrupt['files']['step3/main.c']
  with self.assertRaises(ValueError):journey.validate_export_inventory(work,data,dest,corrupt)
  (dest/'INCOMPLETE.txt').write_text('failed')
  with self.assertRaisesRegex(ValueError,'incomplete'):journey.validate_export_inventory(work,data,dest,pack)
 def test_owner_integer_cannot_impersonate_boolean(self):
  owner=json.loads((self.root/'stock-owner.json').read_text());owner['stopped_reaped']=1
  (self.root/'stock-owner.json').write_text(json.dumps(owner));self.owner=lab.sha(self.root/'stock-owner.json')
  with self.assertRaises(ValueError):self.verify()
 def test_native_receipt_owner_identity_cannot_change(self):
  import learner_session as notebook
  folder=self.base/'attempt';folder.mkdir();work=self.base/'own'
  manifest=dict(kind=stock.kind('step3'),source_sha256='s')
  record=dict(stage='step3',source_sha256='s',started=10,command=['--stock',str(self.root),'--stock-admission','independent-cooperative-v1','--stock-owner-sha256',self.owner])
  prior=dict(action='build',stage='step3',status='PASS',route='stock-reuse-v1',source_sha256='s',started=1,id='build')
  receipt=dict(manifest,stock_admission='independent-cooperative-v1',stock_provenance=self.m)
  for forged in (None,'f'*64):
   if forged is None: receipt.pop('stock_owner_sha256',None)
   else:receipt['stock_owner_sha256']=forged
   (folder/'native.json').write_text(json.dumps(receipt))
   with patch.object(notebook,'session',return_value=(work,{'attempts':[prior]})),patch.object(stock,'verify_inputs',return_value=manifest),patch.object(stock,'stock_inputs',return_value={}):
    with self.assertRaisesRegex(ValueError,'provenance receipt mismatch'):notebook.validate_stock_native(work,record,folder)
if __name__=='__main__':unittest.main()
