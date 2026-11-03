from pathlib import Path
import re
import subprocess
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set()
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag in ('a','img'):self.links.append(a.get('href',a.get('src','')))
class Packaging(unittest.TestCase):
    def test_render_current(self):
        subprocess.run(['python3',str(ROOT/'scripts/render_site.py'),'--check'],check=True,capture_output=True)
    def test_local_links(self):
        for page in (ROOT/'docs/site').rglob('*.html'):
            parser=Links();parser.feed(page.read_text())
            for link in parser.links:
                u=urlsplit(link)
                if u.scheme or u.netloc:continue
                dest=(page.parent/unquote(u.path)).resolve() if u.path else page
                with self.subTest(page=page,link=link):
                    self.assertTrue(dest.is_file(),str(dest))
                    if u.fragment:
                        p=Links();p.feed(dest.read_text());self.assertIn(u.fragment,p.ids)
    def test_eight_accessible_diagrams_and_sources(self):
        folder=ROOT/'docs/diagrams';svgs=list(folder.glob('*.svg'));self.assertEqual(len(svgs),8)
        for svg in svgs:
            node=ET.fromstring(svg.read_text());ns={'s':'http://www.w3.org/2000/svg'}
            self.assertIsNotNone(node.find('s:title',ns));self.assertIsNotNone(node.find('s:desc',ns))
            mmd=svg.with_suffix('.mmd').read_text();self.assertIn('flowchart TD',mmd)
            self.assertEqual(mmd.count('-->'),3)
            for label in re.findall(r'\["(.*?)"\]',mmd):self.assertIn(label,svg.read_text())
    def test_six_rich_folder_contracts(self):
        for n in range(1,7):
            for kind in ('starter','solution'):
                text=(ROOT/f'steps/step{n}/{kind}/README.md').read_text()
                self.assertGreater(len(text),700);self.assertIn('BLOCKED',text);self.assertIn('evidence',text)
    def test_codelab_structure(self):
        s=(ROOT/'codelab/codelab.md').read_text()
        for field in ('author:','summary:','id:','categories:','environments:','status:','feedback link:'):
            self.assertIn(field,s)
        self.assertEqual(len(re.findall(r'^## [1-6]\. ',s,re.M)),6)
        self.assertGreaterEqual(s.count('Duration:'),7)
        self.assertIn('Congratulations',s);self.assertEqual(s.count('Mini-map:'),7)
    def test_no_external_runtime_assets(self):
        for page in (ROOT/'docs/site').rglob('*.html'):
            text=page.read_text();self.assertNotIn('<script',text)
            self.assertNotRegex(text,r'(?:src|href)="https?://[^\"]+\.(?:js|css|woff)')
    def test_policy_not_fake_validation(self):
        self.assertIn('NOT validated', (ROOT/'docs/security-policy.md').read_text())
        self.assertIn('ZERO register rows',(ROOT/'docs/register-evidence.md').read_text())
