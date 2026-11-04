#!/usr/bin/env python3
"""Conservative redistribution guard; not a substitute for licence review."""
import os
from pathlib import Path
import re
import sys

BAD_PART = re.compile(r"^(qnxsdp.*|qnx[678][0-9]*|target-qnx.*|host-qnx.*|qnx-host|qnxsoftwarecenter.*|qsc|[.]qnx|[.]secrets)$", re.I)
BAD_SUFFIX = {'.ifs', '.qcow', '.qcow2', '.vmdk', '.vdi', '.img', '.iso', '.o', '.a', '.so', '.dll', '.exe', '.zip', '.tar', '.gz', '.xz', '.bz2', '.7z', '.deb', '.rpm', '.run'}
BAD_NAME = {'qcc', 'q++', 'mkifs', 'qnxsdp-env.sh', 'libc.so', 'procnto', 'procnto-smp', 'procnto-smp-instr'}
MAGICS = (b'\x7fELF', b'MZ', b'QFI\xfb', b'PK\x03\x04', b'\x1f\x8b', b'\xfd7zXZ\x00', b'BZh', b'7z\xbc\xaf\x27\x1c', b'vhdxfile', b'KDMV', b'\xcf\xfa\xed\xfe', b'\xfe\xed\xfa\xcf')
MARKERS = (b'QNX Software ' + b'Development Platform', b'QNX_' + b'TARGET=', b'QNX_' + b'HOST=', b'QNX Neutrino ' + b'RTOS')

def scan(root):
    errors = []
    for base, dirs, names in os.walk(root, followlinks=False):
        # Git object storage is not source; everything else, even ignored files, is scanned.
        dirs[:] = [d for d in dirs if d != '.git']
        for name in dirs + names:
            p = Path(base) / name
            rel = p.relative_to(root)
            if p.is_symlink():
                errors.append(f'{rel}: symlink not allowed (could hide external SDK)')
                continue
            if any(BAD_PART.match(part) for part in rel.parts) or name.lower() in BAD_NAME or p.suffix.lower() in BAD_SUFFIX or '.so.' in name.lower():
                errors.append(f'{rel}: SDK/image/binary/archive path excluded')
                continue
            if p.is_file():
                try:
                    with p.open('rb') as stream:
                        head = stream.read(512)
                        if head.startswith(MAGICS) or b'ustar' in head[257:263]:
                            errors.append(f'{rel}: executable/image/archive signature')
                            continue
                        # Scan markers incrementally; no file-size bypass.
                        tail = b''
                        stream.seek(0)
                        while True:
                            block = stream.read(65536)
                            if not block:
                                break
                            data = tail + block
                            if any(marker in data for marker in MARKERS):
                                errors.append(f'{rel}: possible proprietary SDK content; review required')
                                break
                            tail = data[-128:]
                except OSError as exc:
                    errors.append(f'{rel}: cannot inspect: {exc}')
    return errors

if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.exit('usage: check-no-sdk.sh [root]')
    root = Path(sys.argv[1] if len(sys.argv) == 2 else '.').resolve()
    if not root.is_dir():
        sys.exit('BLOCKED: scan root is not a directory')
    errors = scan(root)
    for error in errors:
        print('BLOCKED: ' + error, file=sys.stderr)
    print('FAIL: redistribution guard' if errors else 'PASS: redistribution guard only (not a QNX test)')
    sys.exit(1 if errors else 0)
