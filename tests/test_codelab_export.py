import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('export_codelab', ROOT / 'tools/export-codelab.py')
export = importlib.util.module_from_spec(spec)
spec.loader.exec_module(export)


class CodelabExport(unittest.TestCase):
    def test_canonical_tutorial_copy_and_receipt_filenames(self):
        subprocess.run(['python3', str(ROOT/'tools/tutorial_copy.py')], check=True, capture_output=True)
        text=(ROOT/'codelab/codelab.md').read_text()
        for marker in ['FAIL despite application exit0', 'STOP/REAP', 'EDU_GUEST_SOURCE', 'EDU_HOST_SOURCE', 'BLOCKED_NATIVE_TIMEOUT', 'wrong-native.log', 'correct-native.log', 'finish-native.log', 'PREFIX.json and PREFIX.log']:
            self.assertIn(marker,text)
        self.assertNotIn('PREFIX.native.json',text)

    def test_trap_result_before_existing_sdk_gate(self):
        route=(ROOT/'docs/learner-route.md').read_text()
        self.assertLess(route.index('FAIL despite application exit0'),route.index('## Prerequisite gate'))
        self.assertLess(route.index('10→3628800'),route.index('## Prerequisite gate'))
        self.assertIn('stop: BLOCKED',route)
        self.assertIn('not a second IST or worker',route)
        self.assertIn('Working stock recipe',route)
        self.assertIn('--pci-line',route)
        self.assertIn('REUSES',route)
        self.assertIn('STOP/REAP',route)
        self.assertIn('BLOCKED_STOCK_MKIFS_OOM',route)
        self.assertIn('Do not activate/create/resize swap',route)
        self.assertNotIn('then swapon',route)
        # Keep the actual serialization commands, not just the prose marker.
        ready = route.index('test -f "$EDU_BASE/sdk-control/SDK_READY"\npython3')
        build = route.index('python3 "$EDU_CONTROLLER" exec "$EDU_BASE/build.sh" 600')
        stop = route.index('touch "$EDU_BASE/sdk-control/STOP"', build)
        reap = route.index('wait "$SDK_OWNER"', stop)
        free = route.index('flock -n /home/ubuntu/qnx-host/native-test.lock true', reap)
        native = route.index('env EDU_NATIVE_LEASE=granted python3')
        self.assertLess(ready, build)
        self.assertLess(build, stop)
        self.assertLess(stop, reap)
        self.assertLess(reap, free)
        self.assertLess(free, native)

    def test_stock_draft_first_without_modifying_advanced_bytes(self):
        text=(ROOT/'docs/learner-route-custom-legacy.md').read_text()
        old=subprocess.check_output(['git','show','e2c247d055ddb949d801a48bd809b913ff11721d:docs/learner-route.md'],cwd=ROOT,text=True)
        begin=text.index('<!-- BEGIN STOCK ROUTE DRAFT:')
        end=text.index('<!-- END STOCK ROUTE DRAFT -->')+len('<!-- END STOCK ROUTE DRAFT -->')
        # Removing the inserted section recovers the advanced tutorial exactly.
        self.assertEqual(text[:begin].rstrip('\n')+'\n'+text[end+1:],old)
        self.assertLess(begin,text.index('## Start with the trap'))
        self.assertIn('DRAFT / UNVERIFIED',text)
        self.assertIn('NOT_RUN for this stock route',text)
        self.assertIn("Do not invent --run='-device edu'",text)
        self.assertIn('do not build an image or start SDK/QEMU',text)
        self.assertIn('No768MiB retry',text)
        page=(ROOT/'codelab/codelab.md').read_text()
        self.assertIn('](../docs/learner-route-custom-legacy.md)',page)

    def test_stock_draft_only_rebinds_instruction_copy(self):
        old=json.loads(subprocess.check_output(['git','show','e2c247d055ddb949d801a48bd809b913ff11721d:docs/proof-capture/pack.json'],cwd=ROOT,text=True))
        now=json.loads((ROOT/'docs/proof-capture/pack.json').read_text())
        self.assertFalse(now['recorded'])
        for row in old['lines']:
            current=next(r for r in now['lines'] if r['id']==row['id'])
            if row['id']!='T01':self.assertEqual(current,row)
        draft=next(r for r in now['lines'] if r['id']=='T01')
        self.assertIn('Working stock recipe',draft['claim'])
        self.assertIn('cold-reader run pending',draft['narration'])
        self.assertIn('instruction copy',draft['label'])

    def test_stock_research_has_no_fresh_native_proof(self):
        data=json.loads((ROOT/'docs/stock-route-research.json').read_text())
        self.assertEqual(data['status'],'DRAFT_UNVERIFIED_BLOCKED_CLEAN_STOCK_IFS_OOM')
        self.assertEqual(data['prior_measured_block']['ifs_bytes'],0)
        self.assertIn('VERIFIED',data['installed_current_inventory'])
        self.assertIn('native QNX test',data['actions_not_performed'])

    def test_dry_pack_preserves_original_native_pins(self):
        old=json.loads(subprocess.check_output(['git','show','21f583df0a5402953efe63344a5d23ec84798ceb:docs/proof-capture/pack.json'],cwd=ROOT,text=True))
        current=json.loads((ROOT/'docs/proof-capture/pack.json').read_text())
        self.assertEqual(current['frozen_commit'],old['frozen_commit'])
        for row in old['lines']:
            now=next(r for r in current['lines'] if r['id']==row['id'])
            for asset in row['assets']:self.assertIn(asset,now['assets'])
        self.assertFalse(current['recorded'])
        self.assertEqual(current['lines'][0]['id'],'L03')

    def test_new_gate_receipt_never_promotes_native_and_keeps_evidence_hashes(self):
        import hashlib
        base=ROOT/'docs/acceptance/features-20261110'
        receipt=json.loads((base/'receipt.json').read_text())
        self.assertEqual(receipt['outcome'],'BLOCKED_STOCK_MKIFS_OOM')
        self.assertFalse(receipt['image_is_valid'])
        self.assertEqual(receipt['image_bytes'],0)
        self.assertEqual(receipt['attempts'],1)
        self.assertTrue(all(v.startswith('NOT_RUN') for v in receipt['native'].values()))
        self.assertTrue(receipt['cleanup']['qemu_reaped'])
        self.assertTrue(receipt['cleanup']['lease_free'])
        for name,digest in receipt['evidence'].items():
            self.assertEqual(hashlib.sha256((base/name).read_bytes()).hexdigest(),digest,name)
        old=json.loads(subprocess.check_output(['git','show','a4189e8e5262bc717b5b10ad876c38dd8629a5aa:docs/proof-capture/pack.json'],cwd=ROOT,text=True))
        current=json.loads((ROOT/'docs/proof-capture/pack.json').read_text())
        for row in old['lines']:
            if row['id']=='T01': continue  # instruction-copy freeze, never runtime
            now=next(r for r in current['lines'] if r['id']==row['id'])
            for asset in row['assets']:self.assertIn(asset,now['assets'])

    def test_clean_stock_block_binds_evidence_without_native_promotion(self):
        import hashlib
        base=ROOT/'docs/acceptance/stock-20261113'
        r=json.loads((base/'receipt.json').read_text())
        self.assertEqual(r['outcome'],'BLOCKED_CLEAN_STOCK_IFS_OOM')
        self.assertEqual(r['sdk_boots'],1)
        self.assertEqual(r['stock_build_attempts'],1)
        self.assertFalse(r['image']['valid'])
        self.assertEqual(r['image']['ifs_bytes'],0)
        self.assertIsNone(r['image']['disk_sha256'])
        self.assertEqual(r['guest_oom']['anon_rss_kib'],329384)
        self.assertLess(r['host_measurement']['monitored_peak_cgroup_bytes'],2147483648)
        self.assertEqual(r['host_measurement']['sampled_oom_kill_max'],0)
        self.assertEqual(r['host_measurement']['maximum_swap_bytes'],0)
        self.assertEqual((base/'qemu_options').read_text().strip(),'-device edu')
        self.assertTrue(r['qemu_options']['generated_equals_authored'])
        self.assertEqual(r['native']['corrected_source'],'NOT_CREATED')
        self.assertTrue(all(v.startswith('NOT_RUN') for k,v in r['native'].items() if k!='corrected_source'))
        cleanup=json.loads((base/'cleanup.json').read_text())
        self.assertTrue(cleanup['qemu_absent'] and cleanup['lease_free'] and cleanup['sdk_owner_reaped'])
        for name,digest in r['evidence'].items():
            self.assertEqual(hashlib.sha256((base/name).read_bytes()).hexdigest(),digest,name)

    def test_prepare_preserves_content_except_relative_paths(self):
        original = (ROOT / 'codelab/codelab.md').read_text()
        with tempfile.TemporaryDirectory() as tmp:
            stage = Path(tmp)
            prepared = export.prepare(ROOT, stage)
            self.assertEqual(prepared, original.replace('](../', ']('))
            for n in range(1, 7):
                for kind in ('starter', 'solution'):
                    rel = Path('steps') / ('step%d' % n) / kind / 'README.md'
                    self.assertEqual((stage / rel).read_bytes(), (ROOT / rel).read_bytes())
            self.assertEqual(len(list((stage / 'docs/diagrams').glob('*.svg'))), 8)
            for n in range(1, 7):
                for kind in ('starter', 'solution'):
                    rel = Path('steps') / ('step%d' % n) / kind / 'main.c'
                    self.assertEqual((stage / rel).read_bytes(), (ROOT / rel).read_bytes())
            self.assertEqual((stage/'native/edu_dma.h').read_bytes(), (ROOT/'native/edu_dma.h').read_bytes())
            self.assertFalse((stage / 'docs/site').exists())
            self.assertFalse(list(stage.rglob('*.ifs')))

    def test_escape_missing_and_external_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for link in ('../outside.md', '%2e%2e/outside.md', 'missing.svg'):
                with self.subTest(link=link), self.assertRaises(ValueError):
                    export.local_target(root, link, root)
            self.assertIsNone(export.local_target(root, 'https://example.org/a', root))
            self.assertIsNone(export.local_target(root, '//fonts.googleapis.com/a', root))

    def test_bad_binary_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp)
            (cache / 'claat-linux-amd64').write_text('not the official tool')
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                export.tool_command(cache, False)

    def test_missing_binary_does_not_download_implicitly(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'pass --download'):
                export.tool_command(Path(tmp), False)

    def test_output_inside_checkout_refused(self):
        p = subprocess.run(['python3', str(ROOT / 'tools/export-codelab.py'),
                            '--output', str(ROOT / '.tmp/export'),
                            '--tool-cache', '/nonexistent/claat-cache'],
                           capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn('outside checkout', p.stderr)

    @unittest.skipUnless(os.environ.get('CLAAT_TOOL_CACHE'), 'opt-in: pinned official claat cache required')
    def test_actual_official_claat_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'export'
            subprocess.run(['python3', str(ROOT / 'tools/export-codelab.py'),
                            '--tool-cache', os.environ['CLAAT_TOOL_CACHE'],
                            '--output', str(output)], check=True, capture_output=True, text=True)
            receipt = json.loads((output / 'export-receipt.json').read_text())
            self.assertEqual(receipt['tool_sha256'], export.SHA256)
            self.assertEqual(receipt['checks']['starter_solution_folders'], 12)
            folder = output / 'qnx-edu-kit'
            self.assertEqual(export.validate(folder, ROOT)['svg_assets'], 8)
            self.assertEqual(receipt['checks']['source_snapshots'], 12)
            self.assertEqual(receipt['checks']['first_step_warnings'], 'PASS')
            source = folder/'steps/step4/solution/main.c'
            original = source.read_bytes()
            source.write_bytes(original + b'/* drift */')
            with self.assertRaisesRegex(ValueError, 'source snapshot'):
                export.validate(folder, ROOT)
            source.write_bytes(original)
            page = folder/'index.html'
            original = page.read_text()
            page.write_text(original.replace('PRIVATE DRAFT', 'REMOVED WARNING'))
            with self.assertRaisesRegex(ValueError, 'first-step warnings'):
                export.validate(folder, ROOT)
            page.write_text(original)
            # Corrupt a genuine output copy; validation must fail closed.
            next((folder / 'img').glob('*.svg')).write_text('<svg/>')
            with self.assertRaisesRegex(ValueError, 'byte-identical'):
                export.validate(folder, ROOT)


if __name__ == '__main__':
    unittest.main()
