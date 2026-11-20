import importlib.util, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('renderer',ROOT/'scripts/render_site.py')
renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
class RendererComments(unittest.TestCase):
    def test_metadata_hidden_code_preserved(self):
        text=renderer.render(ROOT/'codelab/codelab.md')
        self.assertNotIn('&lt;!-- BEGIN CANONICAL',text)
        self.assertNotIn('&lt;!-- END CANONICAL',text)
        self.assertIn('Start here</a>',text)
    def test_inline_multiline_comments_and_fences(self):
        from unittest.mock import patch
        source=ROOT/'docs/comment-fixture.md'
        content='before <!-- hidden --> after'+chr(10)+'<!-- multi'+chr(10)+'line --> visible'+chr(10)+'~~~'+chr(10)+'<!-- literal -->'+chr(10)+'~~~'+chr(10)
        with patch.object(Path,'read_text',return_value=content):
            result=renderer.render(source)
        self.assertNotIn('hidden',result)
        self.assertNotIn('multi',result)
        self.assertIn('visible',result)
        self.assertIn('&lt;!-- literal --&gt;',result)
