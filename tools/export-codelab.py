#!/usr/bin/env python3
"""Export via checksum-pinned upstream claat; never synthesize its HTML/JSON."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
from urllib.parse import unquote, urlsplit
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
VERSION = 'v2.2.6'
SHA256 = 'b7415471bd823562ebd9e6015e267a12fbf9340dfe839f8e2a175b6c7c0f397a'
REPORTED_VERSION = '2.2.5-2023-06-15T18:32:06Z-872cbcf'
URL = 'https://github.com/googlecodelabs/tools/releases/download/' + VERSION + '/claat-linux-amd64'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(path, parent):
    return path == parent or parent in path.parents


def local_target(base, link, boundary):
    u = urlsplit(link)
    if u.scheme or u.netloc:
        return None
    target = (base / unquote(u.path)).resolve()
    if not inside(target, boundary):
        raise ValueError('link escapes boundary: ' + link)
    if not target.is_file():
        raise ValueError('missing local link: ' + str(target))
    return target


def prepare(root, stage):
    source = (root / 'codelab/codelab.md').read_text()
    # Upstream refuses images outside its source directory. Relocate only paths,
    # leaving all teaching content, metadata, durations and status unchanged.
    def relocate(match):
        link = match.group(1)
        target = local_target(root / 'codelab', link, root)
        u = urlsplit(link)
        suffix = ('?' + u.query if u.query else '') + ('#' + u.fragment if u.fragment else '')
        return '](' + (target.relative_to(root).as_posix() + suffix if target else link) + ')'
    source = re.sub(r'\]\(([^)\s]+)\)', relocate, source)
    (stage / 'codelab.md').write_text(source)
    # Only repository-authored text/diagrams, never native build outputs or SDKs.
    for folder in ('docs', 'steps', 'native'):
        for path in (root / folder).rglob('*'):
            if not path.is_file() or 'site' in path.relative_to(root).parts:
                continue
            if path.suffix not in ('.md', '.svg', '.mmd', '.txt', '.json', '.c', '.h') and path.relative_to(root).as_posix() not in {'docs/acceptance/wrapper-20261108/'+name for name in ('wrong-native.log', 'correct-native.log', 'finish-native.log')}:
                continue
            if path.is_symlink() or not inside(path.resolve(), root):
                raise ValueError('unsafe source asset: ' + str(path))
            dest = stage / path.relative_to(root)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, dest)
    return source


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.images, self.steps = [], [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ('src', 'href'):
            if key in a:
                self.links.append(a[key])
        if tag == 'img':
            self.images.append(a.get('src', ''))
        if tag == 'google-codelab-step':
            self.steps.append(a.get('label', ''))


def validate(folder, root):
    metadata = json.loads((folder / 'codelab.json').read_text())
    if metadata['id'] != 'qnx-edu-kit' or metadata['format'] != 'html':
        raise ValueError('unexpected upstream metadata')
    parser = References()
    parser.feed((folder / 'index.html').read_text())
    for n in range(1, 7):
        if not any(label.startswith(str(n) + '. ') for label in parser.steps):
            raise ValueError('missing core step ' + str(n))
        for kind in ('starter', 'solution'):
            link = 'steps/step%d/%s/README.md' % (n, kind)
            if link not in parser.links:
                raise ValueError('missing scaffold link: ' + link)
            if (folder / link).read_bytes() != (root / link).read_bytes():
                raise ValueError('scaffold content changed: ' + link)
    for n in range(1, 7):
        for kind in ('starter', 'solution'):
            link = 'steps/step%d/%s/main.c' % (n, kind)
            if link not in parser.links or (folder / link).read_bytes() != (root / link).read_bytes():
                raise ValueError('missing or changed source snapshot: ' + link)
    first_step = (folder / 'index.html').read_text().split('<google-codelab-step', 2)[1]
    if 'Deliberately fail your own edit despite exit 0, correct it, then implement normal /dev/edu I/O on QNX 8.0. Advanced lab: needs an existing QNX SDP 8.0 install and QEMU.' not in first_step:
        raise ValueError('essential first-step warnings omitted by upstream')
    external = []
    for link in parser.links:
        if local_target(folder, link, folder) is None:
            external.append(link)
    originals = sorted(digest(p) for p in (root / 'docs/diagrams').glob('*.svg'))
    exported = sorted(digest(local_target(folder, link, folder)) for link in parser.images)
    if len(originals) != 8 or exported != originals:
        raise ValueError('eight byte-identical SVG diagrams required')
    return {'core_steps': 6, 'starter_solution_folders': 12, 'svg_assets': 8, 'source_snapshots': 12, 'first_step_warnings': 'PASS',
            'local_links': 'PASS', 'external_runtime_references': sorted(set(external))}


def tool_command(cache, download):
    binary = cache / 'claat-linux-amd64'
    if not binary.exists():
        if not download:
            raise ValueError('claat missing: pass --download to fetch pinned official release')
        cache.mkdir(parents=True, exist_ok=True)
        with urlopen(URL, timeout=60) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != SHA256:
            raise ValueError('download checksum mismatch')
        binary.write_bytes(data)
    if digest(binary) != SHA256:
        raise ValueError('claat checksum mismatch')
    binary.chmod(0o755)
    if platform.system() != 'Linux':
        raise ValueError('this pin supports Linux amd64, or Linux ARM64 with qemu-user-static')
    command = [str(binary)]
    if platform.machine() not in ('x86_64', 'AMD64'):
        emulator = shutil.which('qemu-x86_64-static')
        if not emulator:
            raise ValueError('ARM64 requires distro qemu-x86_64-static (not a guest VM)')
        command.insert(0, emulator)
    actual = subprocess.check_output(command + ['version'], text=True).strip()
    if actual != REPORTED_VERSION:
        raise ValueError('unexpected embedded claat version: ' + actual)
    return command


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True, help='new external directory (must not exist)')
    ap.add_argument('--tool-cache', type=Path, required=True, help='external tool cache')
    ap.add_argument('--download', action='store_true')
    args = ap.parse_args()
    output, cache = args.output.resolve(), args.tool_cache.resolve()
    if inside(output, ROOT) or inside(cache, ROOT):
        ap.error('output and tool cache must remain outside checkout')
    if inside(cache, output):
        ap.error('tool cache must not be inside the export output')
    if output.exists():
        ap.error('output exists; use a fresh directory (never overwritten)')
    command = tool_command(cache, args.download)
    output.mkdir(parents=True)
    # Retain prepared input: upstream metadata source must not point to a deleted temp file.
    stage = output / '_source'
    stage.mkdir()
    source = prepare(ROOT, stage)
    subprocess.run(command + ['export', '-ga', '', '-o', str(output), str(stage / 'codelab.md')], check=True)
    folder = output / 'qnx-edu-kit'
    for name in ('docs', 'steps', 'native'):
        shutil.copytree(stage / name, folder / name)
    # Canonical route links its historical codelab source; include authored source.
    (folder / 'codelab').mkdir(exist_ok=True)
    shutil.copyfile(ROOT / 'codelab/codelab.md', folder / 'codelab/codelab.md')
    shutil.copyfile(ROOT / 'REVIEW.md', folder / 'REVIEW.md')
    checks = validate(folder, ROOT)
    receipt = {'tool_release': VERSION, 'tool_url': URL, 'tool_sha256': SHA256,
               'embedded_version': REPORTED_VERSION, 'runner': command[:-1],
               'source_sha256': digest(ROOT / 'codelab/codelab.md'),
               'prepared_source_sha256': hashlib.sha256(source.encode()).hexdigest(),
               'checks': checks, 'scope': 'host export only; NOT full fresh-learner QNX acceptance'}
    (output / 'export-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit('BLOCKED: ' + str(exc))
