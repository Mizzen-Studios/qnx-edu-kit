#!/usr/bin/env python3
"""Read-only prerequisite probe; run inside the learner's licensed Linux SDK host.
No downloads, activation, BSP modifications or QEMU launch. Never a native PASS.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def probe(env, work):
    env, work = Path(env).resolve(), Path(work).resolve()
    checks = {'sdp_env_exists': env.is_file(), 'fresh_workspace': not work.exists()}
    result = {'kind': 'clean-step3-preflight-v1', 'platform': 'QNX 8 x86_64 / QEMU pc TCG',
              'checks': checks, 'portability': 'UNVERIFIED', 'native_acceptance': 'NOT_RUN'}
    if env.is_file():
        # Source the explicitly supplied trusted SDK environment, never eval tool output.
        command = ['bash', '-c', 'set -e; source "$1" >/dev/null; command -v qcc; command -v mkifs; command -v mkqnximage; printf "%s\n" "$QNX_TARGET"', 'preflight', str(env)]
        p = subprocess.run(command, capture_output=True, text=True, timeout=30)
        result['environment_returncode'] = p.returncode
        lines = p.stdout.splitlines()
        checks['sdk_tools_present'] = p.returncode == 0 and len(lines) == 4
        if checks['sdk_tools_present']:
            result['tools'] = dict(zip(['qcc', 'mkifs', 'mkqnximage'], lines[:3]))
            target = Path(lines[3])
            required = ['x86_64/boot/sys/startup-x86', 'x86_64/boot/sys/procnto-smp-instr',
                        'x86_64/usr/sbin/pci-server', 'x86_64/usr/lib/libpci.so']
            result['licensed_components'] = {name: (target/name).exists() for name in required}
            checks['licensed_components_present'] = all(result['licensed_components'].values())
            result['sdp_env_sha256'] = hashlib.sha256(env.read_bytes()).hexdigest()
        else:
            result['diagnostic'] = p.stderr[-2000:]
    checks['python3'] = shutil.which('python3') is not None
    result['ready_for_clean_build_attempt'] = all(checks.values())
    result['limits'] = 'all SDK/native QEMU: shared flock; CPU 100%; memory 1 GiB; nice 15; 1 vCPU; 512 MiB guest'
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sdp-env', required=True)
    p.add_argument('--fresh-work', required=True)
    a = p.parse_args()
    try:
        result = probe(a.sdp_env, a.fresh_work)
    except (OSError, subprocess.TimeoutExpired) as e:
        print(json.dumps({'portability':'UNVERIFIED', 'blocked':str(e)})); return 2
    print(json.dumps(result, indent=2))
    return 0 if result['ready_for_clean_build_attempt'] else 2

if __name__ == '__main__':
    sys.exit(main())
