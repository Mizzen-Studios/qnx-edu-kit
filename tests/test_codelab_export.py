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

    def test_dry_pack_preserves_original_native_pins(self):
        old=json.loads(subprocess.check_output(['git','show','21f583df0a5402953efe63344a5d23ec84798ceb:docs/proof-capture/pack.json'],cwd=ROOT,text=True))
        current=json.loads((ROOT/'docs/proof-capture/pack.json').read_text())
        self.assertEqual(current['frozen_commit'],old['frozen_commit'])
        for row in old['lines']:
            now=next(r for r in current['lines'] if r['id']==row['id'])
            for asset in row['assets']:self.assertIn(asset,now['assets'])
        self.assertFalse(current['recorded'])
        self.assertEqual(current['lines'][0]['id'],'L03')

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
