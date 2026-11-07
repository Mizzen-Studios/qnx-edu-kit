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
            # Corrupt a genuine output copy; validation must fail closed.
            next((folder / 'img').glob('*.svg')).write_text('<svg/>')
            with self.assertRaisesRegex(ValueError, 'byte-identical'):
                export.validate(folder, ROOT)


if __name__ == '__main__':
    unittest.main()
