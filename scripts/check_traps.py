#!/usr/bin/env python3
"""Strict, bounded HOST reasoning checker. Never builds or executes learner input."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'codelab/qnx-traps/catalog.json'
LIMIT = 16384


def catalog():
    return json.loads(CATALOG.read_text())


def digest():
    return hashlib.sha256(CATALOG.read_bytes()).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def parse(raw):
    if len(raw) > LIMIT:
        raise ValueError('input exceeds 16384 bytes')
    return json.loads(raw, object_pairs_hook=unique)


def check(data, step=None):
    steps = catalog()['steps']
    ids = {s['id'] for s in steps}
    if step is not None and step not in ids:
        raise ValueError('unsupported step')
    if not isinstance(data, dict) or set(data) != {'version', 'catalog_sha256', 'answers'}:
        raise ValueError('expected exactly version, catalog_sha256, answers')
    if type(data['version']) is not int or data['version'] != 1:
        raise ValueError('unsupported version')
    if data['catalog_sha256'] != digest():
        raise ValueError('catalog binding mismatch; export a current worksheet')
    answers = data['answers']
    if not isinstance(answers, dict) or set(answers) - ids:
        raise ValueError('unsupported answers/step')
    for key, value in answers.items():
        s = next(s for s in steps if s['id'] == key)
        if not isinstance(value, str) or value not in s['options']:
            raise ValueError('unsupported choice for ' + key)
    rows = []
    for s in steps:
        if step and step != s['id']:
            continue
        value = answers.get(s['id'])
        state = 'MISSING' if value is None else 'CORRECT' if value == s['answer'] else 'RETRY'
        rows.append({'step': s['id'], 'status': state, 'observation': s['observation'],
                     'diagnosis': s['diagnosis'], 'fix': s['fix'], 'source': s['source']})
    return {'scope': 'HOST_STATIC_REASONING', 'native_validation': 'NOT_RUN',
            'catalog_sha256': digest(), 'complete': all(r['status'] == 'CORRECT' for r in rows),
            'steps': rows}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--answers', type=Path)
    p.add_argument('--step', choices=[s['id'] for s in catalog()['steps']])
    p.add_argument('--template', action='store_true')
    args = p.parse_args()
    if args.template:
        print(json.dumps({'version': 1, 'catalog_sha256': digest(), 'answers': {}}, indent=2))
        return 0
    if args.answers is None:
        p.error('--answers is required unless --template is used')
    try:
        # Bounded read also rejects large files without loading them all.
        with args.answers.open('rb') as f:
            data = parse(f.read(LIMIT + 1))
        report = check(data, args.step)
    except (OSError, ValueError, UnicodeError, RecursionError):
        print(json.dumps({'scope': 'HOST_STATIC_REASONING', 'native_validation': 'NOT_RUN',
                          'error': 'INVALID_INPUT: missing, malformed, unsupported or catalog mismatch'}))
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report['complete'] else 1


if __name__ == '__main__':
    sys.exit(main())
