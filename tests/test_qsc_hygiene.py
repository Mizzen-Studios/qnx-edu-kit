import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('guard_qsc',ROOT/'scripts/check_no_sdk.py')
guard=importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

class QSCHygiene(unittest.TestCase):
    def test_qsc_credential_paths_and_installer(self):
        for name in ('qnxsoftwarecenter/data.txt','QNXSoftwareCenter/data.txt','qsc/index.txt','.qnx/key.txt','.secrets/myqnx','qnx-host/home/config.txt','install.run'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as folder:
                path=Path(folder)/name
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(b'placeholder without credential')
                issue=guard.problem(name,path.read_bytes()) if hasattr(guard,'problem') else guard.scan(Path(folder))
                self.assertTrue(issue)
    def test_actual_elf_bytes_not_only_escaped_markers(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'renamed.txt'
            path.write_bytes(bytes([127])+b'ELF'+bytes([2,1,1,0]))
            issue=guard.problem(path.name,path.read_bytes()) if hasattr(guard,'problem') else guard.scan(Path(folder))
            self.assertTrue(issue)
