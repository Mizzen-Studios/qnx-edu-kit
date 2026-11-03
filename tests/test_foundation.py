import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('guard', ROOT / 'scripts/check_no_sdk.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

class RedistributionGuard(unittest.TestCase):
    def fixture(self, name, content=b'text'):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            root = Path(tmp)
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            return guard.scan(root)

    def test_plain_source_allowed(self):
        self.assertEqual(self.fixture('driver.c', b'/* original source */'), [])

    def test_forbidden_paths(self):
        for name in ('qnxsdp800/header.h', 'qnx800/a.h', 'disk.IMG', 'boot.ifs', 'lib.so.2', 'qcc', 'sdk.zip', '.local/hidden.qcow2', 'object.o', 'sdk.tar.xz'):
            with self.subTest(name=name):
                self.assertTrue(self.fixture(name))

    def test_renamed_binaries_and_archives(self):
        for magic in guard.MAGICS:
            with self.subTest(magic=magic):
                self.assertTrue(self.fixture('innocent.txt', magic + b'payload'))
        self.assertTrue(self.fixture('archive', b'0' * 257 + b'ustar'))

    def test_markers_beyond_prefix_and_across_chunks(self):
        for marker in guard.MARKERS:
            self.assertTrue(self.fixture('copied.h', b'x' * 65530 + marker))

    def test_external_symlink_blocked(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            root = Path(tmp)
            (root / 'external').symlink_to('/not/a/real/sdk', target_is_directory=True)
            self.assertTrue(guard.scan(root))

    def test_ignored_untracked_files_still_blocked(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            root = Path(tmp)
            (root / '.gitignore').write_text('hidden.*\n')
            (root / 'hidden.img').write_text('not tracked')
            result = subprocess.run([str(ROOT / 'scripts/check-no-sdk.sh'), str(root)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('hidden.img', result.stderr)

    def test_invalid_root_fails(self):
        result = subprocess.run([str(ROOT / 'scripts/check-no-sdk.sh'), '/nonexistent/sdk-scan-root'], capture_output=True)
        self.assertNotEqual(result.returncode, 0)

class LiveGate(unittest.TestCase):
    def test_all_steps_block_even_with_environment_claims(self):
        import os
        for step in range(1, 7):
            with self.subTest(step=step):
                result = subprocess.run([str(ROOT / 'scripts/check-step.sh'), str(step)], capture_output=True, text=True,
                                        env={**os.environ, 'QNX_TARGET': '/made/up', 'QNX_HOST': '/made/up', 'LIVE_VERIFIED': '1'})
                self.assertEqual(result.returncode, 2)
                self.assertIn('BLOCKED:', result.stdout)
                self.assertNotIn('PASS', result.stdout)

    def test_invalid_step_rejected(self):
        for step in ('0', '7', 'step1', ''):
            self.assertEqual(subprocess.run([str(ROOT / 'scripts/check-step.sh'), step], capture_output=True).returncode, 64)

    def test_step_layout(self):
        for step in range(1, 7):
            for kind in ('starter', 'solution'):
                self.assertTrue((ROOT / f'steps/step{step}/{kind}/README.md').is_file())

    def test_license(self):
        self.assertIn('Apache License', (ROOT / 'LICENSE').read_text())
        self.assertIn('Version 2.0', (ROOT / 'LICENSE').read_text())
