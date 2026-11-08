"""Host-only validation; arguments: repository, original pack, own session, new export."""
import json
from pathlib import Path
import sys
root, old, work, out = map(Path, sys.argv[1:])
sys.path.insert(0, str(root/'scripts'))
import learner_session as c
m = json.loads((old/'pack.json').read_text())
assert len(m['files']) == 55
assert all(c.lab.sha(old/p) == h for p,h in m['files'].items())
assert c.lab.sha(old/'pack.json') == '93da42cf3ffeadea342ea9da4585b35b8e62e0a8b2e446ac8be3fc51f130173c'
_, data = c.session(work)
attempts = []
for r in data['attempts']:
    disk = c.validate_attempt(work, r, work/'attempts'/r['id'])
    attempts.append(dict(id=r['id'], status=r['status'], validation='PASS', disk_bound=disk is not None))
pack = c.export(work, out)
new = json.loads(pack.read_text())
assert len(new['files']) == 55
assert all(c.lab.sha(out/p) == h for p,h in new['files'].items())
print(json.dumps(dict(original_pack=str(old), original_manifest_sha256=c.lab.sha(old/'pack.json'), original_files=55,
    original_all_hashes_match=True, attempts=attempts, new_export=str(out), new_manifest_sha256=c.lab.sha(pack),
    new_files=55, new_all_hashes_match=True, current_sources=new['current_sources'], native_rerun=False), indent=2))
