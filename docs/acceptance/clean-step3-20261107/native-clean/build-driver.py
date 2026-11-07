#!/usr/bin/env python3
"""Learner-owned step3 only. No reference receipt or saved-log input mode."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
REPO_COPY = (ROOT/'steps/step3/starter/main.c').is_file()

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def external(path):
    path = Path(path).resolve()
    if REPO_COPY and (path == ROOT or ROOT in path.parents):
        raise ValueError('licensed build artifacts must be outside checkout')
    return path

def init(work):
    if not REPO_COPY:
        raise ValueError('init requires the repository copy; standalone SDK copy supports build/run')
    work = external(work)
    work.mkdir(parents=True, exist_ok=True)
    source = work / 'main.c'
    if source.exists():
        raise ValueError('refusing to overwrite learner source')
    source.write_text((ROOT/'steps/step3/starter/main.c').read_text())
    return source

def build(source, out, env, buildfile, cwd):
    """Run inside learner licensed SDK environment; no private bundle needed.

    Learner BSP buildfile must install learner_bin and learner-start.sh from out.
    It must invoke /proc/boot/learner-start.sh after PCI server startup.
    """
    source = Path(source).resolve()
    out = external(out)
    out.mkdir(parents=True, exist_ok=True)
    snapshot = out/'learner-source.c'
    if source == snapshot:
        raise ValueError('edit main.c, not the generated source snapshot')
    (out/'manifest.json').unlink(missing_ok=True)
    for stale in ['learner_bin','learner.ifs']:
        (out/stale).unlink(missing_ok=True)
    snapshot.write_bytes(source.read_bytes())
    binary = out/'learner_bin'
    image = out/'learner.ifs'
    script = out/'learner-start.sh'
    build_hash = sha(buildfile)
    command = ['bash', '-c',
        'set -eo pipefail; source "$1"; qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -Wno-unused-variable -o "$2" "$3" -lpci',
        'learner-build', str(Path(env).resolve()), str(binary), str(snapshot)]
    subprocess.run(command, check=True)
    if not binary.read_bytes().startswith(b'\x7fELF'):
        raise ValueError('qcc did not produce an ELF binary')
    binary_hash = sha(binary)
    source_hash = sha(snapshot)
    script.write_text('#!/bin/sh\n'
        + f'echo LEARNER_BIND source={source_hash} binary={binary_hash}\n'
        + '/proc/boot/learner_bin\n'
        + 'echo LEARNER_RC=$?\n')
    subprocess.run(['bash', '-c', 'set -eo pipefail; source "$1"; mkifs "$2" "$3"',
        'learner-image', str(Path(env).resolve()), str(Path(buildfile).resolve()), str(image)], cwd=cwd, check=True)
    if not image.is_file() or image.stat().st_size == 0:
        raise ValueError('mkifs did not produce a nonempty image')
    if sha(source) != source_hash or sha(buildfile) != build_hash:
        raise ValueError('inputs changed during build')
    manifest = {'kind':'learner-step3-v1', 'source_sha256':source_hash,
        'binary_sha256':binary_hash, 'image_sha256':sha(image),
        'buildfile_sha256':build_hash, 'startup_sha256':sha(script),
        'source_path':str(source), 'built_at':time.time(),
        'build_driver_sha256':sha(Path(__file__)),
        'target_provenance':'learner supplied licensed SDP/BSP; QSTI unverified'}
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest

def oracle(output, manifest):
    clean = output.replace('\r', '')
    binding = f"LEARNER_BIND source={manifest['source_sha256']} binary={manifest['binary_sha256']}"
    rows = re.findall(r'^LEARNER_MMIO id=([0-9a-f]{8}) write=([0-9a-f]{8}) read=([0-9a-f]{8})$', clean, re.M)
    events = [line.split(' ',1)[0].split('=',1)[0] for line in clean.splitlines()
              if line.startswith(('LEARNER_BIND ', 'LEARNER_MMIO ', 'LEARNER_RC='))]
    checks = {'binding':clean.splitlines().count(binding) == 1,
        'ordering':events == ['LEARNER_BIND','LEARNER_MMIO','LEARNER_RC'],
        'qnx_target':bool(re.search(r'^EDU TARGET QNX 8[.]0(?:[.]\d+)? ', clean, re.M)),
        'device_readback':rows == [('010000ed','12345678','edcba987')],
        'exit_zero':re.findall(r'^LEARNER_RC=(\d+)$', clean, re.M) == ['0']}
    return checks

def verify_inputs(source, bundle):
    bundle = external(bundle)
    m = json.loads((bundle/'manifest.json').read_text())
    if m.get('kind') != 'learner-step3-v1':
        raise ValueError('not a learner build manifest; reference receipts cannot satisfy this stage')
    for path, key in [(Path(source),'source_sha256'),(bundle/'learner-source.c','source_sha256'),
                      (bundle/'learner_bin','binary_sha256'),(bundle/'learner.ifs','image_sha256'),
                      (bundle/'learner-start.sh','startup_sha256')]:
        if sha(path) != m[key]:
            raise ValueError(f'{key} mismatch: rebuild your edited source')
    return m

def caps(pid):
    proc = Path('/proc')/str(pid)
    rel = next(x.split(':',2)[2] for x in (proc/'cgroup').read_text().splitlines() if x.startswith('0::'))
    cg = Path('/sys/fs/cgroup')/rel.lstrip('/')
    cap = {'pid':pid, 'cpu':(cg/'cpu.max').read_text().strip(),
           'memory':(cg/'memory.max').read_text().strip(), 'nice':os.getpriority(os.PRIO_PROCESS,pid)}
    q,p = cap['cpu'].split()
    if q == 'max' or int(q)>int(p) or cap['memory']=='max' or int(cap['memory'])>1073741824 or cap['nice']<15:
        raise ValueError('effective QEMU cap invalid')
    return cap

def run(source, bundle, disk, receipt, timeout=180):
    bundle = external(bundle)
    m = verify_inputs(source, bundle)
    if not Path(disk).is_file():
        raise ValueError('learner BSP external boot disk absent')
    if os.environ.get('EDU_NATIVE_LEASE') != 'granted':
        raise ValueError('exclusive serialized SDK/native lease required')
    lock = Path(os.environ.get('EDU_NATIVE_LOCK','/home/ubuntu/qnx-host/native-test.lock'))
    with lock.open('a') as lease:
        try:
            fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            pass  # caller must own this held lock across SDK and native phases
        else:
            fcntl.flock(lease, fcntl.LOCK_UN)
            raise ValueError('serialization lock is free: hold flock across SDK/native work')
    if subprocess.run(['pgrep','-f','^qemu-system-'],capture_output=True).returncode == 0:
        raise ValueError('another QEMU is running; stop/reap SDK guest first')
    command = ['systemd-run','--user','--scope','--quiet','-p','CPUQuota=100%','-p','MemoryMax=1G',
        'nice','-n','15','qemu-system-x86_64','-machine','pc,accel=tcg','-cpu','max','-smp','1','-m','512',
        '-display','none','-serial','stdio','-monitor','none','-no-reboot','-kernel',str(Path(bundle)/'learner.ifs'),
        '-drive',f'file={Path(disk).resolve()},format=raw,if=ide,snapshot=on',
        '-nic','user,model=virtio-net-pci','-device','edu,dma_mask=0xffffffff']
    start = time.time()
    disk_hash = sha(disk)
    proc = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    selector = selectors.DefaultSelector()
    selector.register(proc.stdout,selectors.EVENT_READ)
    data = b''
    cap = None
    owned_pid = None
    stop_reason = 'timeout'
    try:
        end = time.monotonic()+timeout
        while time.monotonic()<end:
            if cap is None:
                todo = [proc.pid]
                while todo:
                    pid = todo.pop()
                    try:
                        cmd = (Path('/proc')/str(pid)/'cmdline').read_bytes().split(b'\0')[0]
                        if cmd.endswith(b'/qemu-system-x86_64') or cmd == b'qemu-system-x86_64':
                            owned_pid = pid
                            cap = caps(pid)
                        else:
                            todo += [int(p) for p in subprocess.run(['pgrep','-P',str(pid)],capture_output=True,text=True).stdout.split()]
                    except FileNotFoundError:
                        pass
            if selector.select(.1):
                chunk = os.read(proc.stdout.fileno(),65536)
                if not chunk:
                    stop_reason = 'stdout closed'; break
                remaining = 2*1024*1024-len(data)
                data += chunk[:remaining]
                if len(chunk)>remaining:
                    stop_reason = 'output exceeded 2 MiB'; break
                if re.search(rb'LEARNER_RC=\d+\r?\n',data):
                    stop_reason = 'target completed'; break
            if proc.poll() is not None:
                stop_reason = 'QEMU exited before completion'; break
    finally:
        if owned_pid:
            try: os.kill(owned_pid,signal.SIGTERM)
            except ProcessLookupError: pass
        try: proc.wait(10)
        except subprocess.TimeoutExpired:
            if owned_pid:
                try: os.kill(owned_pid,signal.SIGKILL)
                except ProcessLookupError: pass
            proc.terminate()
            proc.wait(10)
        selector.close()
    output = data.decode(errors='replace')
    checks = oracle(output,m)
    checks['bounded_completion'] = stop_reason == 'target completed'
    checks['inputs_unchanged_after_boot'] = verify_inputs(source, bundle) == m
    checks['disk_unchanged'] = sha(disk) == disk_hash
    checks['qemu_reaped'] = owned_pid is not None and not (Path('/proc')/str(owned_pid)).exists()
    success = bool(cap) and all(checks.values())
    evidence = dict(m, started=start, finished=time.time(), caps=cap, checks=checks,
                    success=success, qemu_wrapper_returncode=proc.returncode,
                    disk_sha256=disk_hash, stop_reason=stop_reason,
                    serialization_lock=str(lock), lease='caller-held flock observed locked',
                    run_driver_sha256=sha(Path(__file__)),
                    target_returncode=re.findall(r'LEARNER_RC=(\d+)',output),
                    observation='fresh custom QNX boot, not QSTI or hardware qualification',
                    substrate_note=os.environ.get('EDU_LEARNER_SUBSTRATE','learner supplied BSP; portability not inferred'))
    receipt = Path(receipt)
    receipt.parent.mkdir(parents=True,exist_ok=True)
    receipt.with_suffix('.log').write_text(output)
    receipt.with_suffix('.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(output)
    if not success:
        print('FAIL: '+stop_reason+'; inspect target exit and MMIO read-back; expected ID 010000ed, write 12345678, complement edcba987. Rebuild after edits.')
    else:
        print('PASS: learner step3 source-bound native BAR read-back')
    return 0 if success else 1

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='action',required=True)
    i = sub.add_parser('init'); i.add_argument('--work',required=True)
    b = sub.add_parser('build')
    for arg in ['source','out','sdp-env','buildfile','bsp-cwd']: b.add_argument('--'+arg,required=True)
    r = sub.add_parser('run')
    for arg in ['source','bundle','disk','receipt']: r.add_argument('--'+arg,required=True)
    a = p.parse_args()
    try:
        if a.action=='init': print(init(a.work)); return 0
        if a.action=='build': print(json.dumps(build(a.source,a.out,a.sdp_env,a.buildfile,a.bsp_cwd),indent=2)); return 0
        return run(a.source,a.bundle,a.disk,a.receipt)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as e:
        print('BLOCKED:',e,file=sys.stderr); return 2

if __name__=='__main__': sys.exit(main())
