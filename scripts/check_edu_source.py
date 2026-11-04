#!/usr/bin/env python3
"""Explicit online upstream source checksum check; downloads only into memory."""
import hashlib
from urllib.request import urlopen
from edu_qtest import PIN,SOURCE_HASH
for name,expected in [('hw/misc/edu.c',SOURCE_HASH),('docs/specs/edu.rst','fedc8a6b4dc2f3d6d127c5390f7c3580eb8a3ff24d0846bf1674d42a0c420d3c')]:
    url='https://raw.githubusercontent.com/qemu/qemu/'+PIN+'/'+name
    with urlopen(url,timeout=20) as response: data=response.read()
    actual=hashlib.sha256(data).hexdigest()
    if actual!=expected: raise SystemExit('FAIL checksum '+name+' '+actual)
    print('PASS upstream pin',PIN,name,'SHA256',actual)
