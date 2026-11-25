"""HOST reasoning, boundary and negative checks. No native execution."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import check_traps as c
import render_traps as r


class Traps(unittest.TestCase):
    def worksheet(self):
        return {'version': 1, 'catalog_sha256': c.digest(),
                'answers': {s['id']: s['answer'] for s in c.catalog()['steps']}}

    def test_correct_each_step_and_all(self):
        for step in [None]+[s['id'] for s in c.catalog()['steps']]:
            report=c.check(self.worksheet(),step)
            self.assertTrue(report['complete'])
            self.assertEqual(report['native_validation'],'NOT_RUN')
            self.assertEqual(report['scope'],'HOST_STATIC_REASONING')

    def test_each_wrong_choice_gives_diagnosis_fix_and_source(self):
        for s in c.catalog()['steps']:
            for key in s['options']:
                if key==s['answer']:continue
                data=self.worksheet();data['answers'][s['id']]=key
                report=c.check(data,s['id']);row=report['steps'][0]
                self.assertFalse(report['complete']);self.assertEqual(row['status'],'RETRY')
                for field in ['observation','diagnosis','fix','source']:self.assertTrue(row[field])

    def test_missing_all_and_one(self):
        data=self.worksheet();data['answers']={}
        self.assertEqual({s['status'] for s in c.check(data)['steps']},{'MISSING'})
        self.assertFalse(c.check(data)['complete'])
        data=self.worksheet();del data['answers']['read']
        self.assertFalse(c.check(data)['complete']);self.assertTrue(c.check(data,'receive')['complete'])

    def test_invalid_shape_version_binding_and_unknowns(self):
        invalid=[None,[],{},'PASS']
        for key,value in [('version',True),('version',2),('catalog_sha256','0'*64),('answers',[]),('answers',{'unknown':'yes'}),('answers',{'receive':'$(touch /tmp/no)'}),('answers',{'receive':{}})]:
            data=self.worksheet();data[key]=value;invalid.append(data)
        data=self.worksheet();data['native_validation']='PASS';invalid.append(data)
        for data in invalid:
            with self.subTest(data=data),self.assertRaises(ValueError):c.check(data)
        with self.assertRaises(ValueError):c.check(self.worksheet(),'unsupported')

    def test_duplicate_json_and_malformed_oversize_utf8(self):
        for raw in [b'{"version":1,"version":1}',b'{"answers":{"read":"eof","read":"eof"}}',b'x',b'[] '*6000,bytes([255])]:
            with self.assertRaises((ValueError,UnicodeError)):c.parse(raw)

    def test_cli_statuses(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'answers.json'
            def call(*args):return subprocess.run([sys.executable,str(ROOT/'scripts/check_traps.py'),*args],capture_output=True,text=True)
            self.assertEqual(call('--answers',str(p)).returncode,2)
            data=self.worksheet();p.write_text(json.dumps(data));self.assertEqual(call('--answers',str(p)).returncode,0)
            data['answers']['receive']='error';p.write_text(json.dumps(data));self.assertEqual(call('--answers',str(p)).returncode,1)
            self.assertEqual(call('--answers',str(p),'--step','read').returncode,0)
            p.write_text('{}');self.assertEqual(call('--answers',str(p)).returncode,2)
            p.write_bytes(b' '*17000);self.assertEqual(call('--answers',str(p)).returncode,2)
            self.assertEqual(call('--step','evil').returncode,2)
            self.assertEqual(json.loads(call('--template').stdout)['answers'],{})

    def test_no_learner_execution_routes(self):
        source=(ROOT/'scripts/check_traps.py').read_text()
        for forbidden in ['subprocess','os.system','eval(','exec(','pickle']:self.assertNotIn(forbidden,source)
        js=(ROOT/'codelab/qnx-traps/lab.js').read_text()
        for forbidden in ['innerHTML','eval(','fetch(','localStorage','XMLHttpRequest']:self.assertNotIn(forbidden,js)

    def test_generated_outputs_current_and_script_inert(self):
        for path,content in r.outputs().items():self.assertEqual(path.read_text(),content)
        page=next(content for path,content in r.outputs().items() if path.suffix=='.html')
        self.assertIn('connect-src',page);self.assertIn('application/json',page)
        self.assertIn('Native validation: NOT_RUN',page)

    def test_sources_and_metadata(self):
        steps=c.catalog()['steps'];self.assertEqual(len({s['id'] for s in steps}),5)
        for s in steps:self.assertIn(s['answer'],s['options'])
        doc=(ROOT/'codelab/qnx-traps/qnx-traps.md').read_text()
        for value in ['status: draft','Duration:','NativeLab validation **NOT_RUN**','eaddbfbcb271db18645fc760ee411c0293a30d6a']:self.assertIn(value,doc)
