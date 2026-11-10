#!/usr/bin/env python3
"""Learner-owned step3 and /dev/edu finish. No reference/saved-log input mode."""
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

def manifest_kind(stage):
    if stage not in ('step3', 'step6'):
        raise ValueError('unknown learner stage')
    return 'learner-step3-v1' if stage == 'step3' else 'learner-dev-edu-v1'

def observation_start(source_hash):
    # Installed image tools only. No mkifs additions or package/component setup.
    return ('trace_pid=\n'
        'if command -v tracelogger >/dev/null 2>&1 && command -v od >/dev/null 2>&1; then\n'
        '  tracelogger -s1 -S64K -k1 -b1 -A EDU_SOURCE='+source_hash+' -f /tmp/edu-slice.kev >/tmp/edu-trace.log 2>&1 &\n'
        '  trace_pid=$!\n'
        'else echo LEARNER_TRACE OMITTED tools_absent; fi\n')

def observation_finish():
    return ('echo LEARNER_SLOG2_BEGIN\n'
        'slog2info -b edu_learner\nslog_rc=$?\n'
        'echo LEARNER_SLOG2_END rc=$slog_rc\n'
        'if test -n "$trace_pid"; then\n'
        '  wait "$trace_pid"; trace_rc=$?\n'
        '  if test "$trace_rc" = 0 && test -s /tmp/edu-slice.kev; then\n'
        '    echo LEARNER_TRACE_BEGIN format=hex\n'
        '    od -An -tx1 -v /tmp/edu-slice.kev\n'
        '    echo LEARNER_TRACE_END rc=0\n'
        '  else echo LEARNER_TRACE UNVERIFIED rc=$trace_rc; cat /tmp/edu-trace.log; fi\n'
        'fi\n')

def startup(stage, source_hash, binary_hash):
    binding = f'echo LEARNER_BIND source={source_hash} binary={binary_hash}\n'
    begin = '#!/bin/sh\n'+binding+observation_start(source_hash)
    if stage == 'step3':
        return (begin+'/proc/boot/learner_bin\napp_rc=$?\n'+observation_finish()+
                'echo LEARNER_RC=$app_rc\n')
    manifest_kind(stage)
    return (begin+
        'echo "EDU TARGET $(uname -s) $(uname -r) $(uname -m)"\n'
        '/proc/boot/learner_bin &\nlearner_pid=$!\n'
        'if ! waitfor /dev/edu 30; then kill "$learner_pid"; wait "$learner_pid"; echo LEARNER_RC=2; exit 2; fi\n'
        'printf "10\\n" > /dev/edu\nwrite_rc=$?\n'
        'observed=$(cat /dev/edu)\nread_rc=$?\n'
        'echo "LEARNER_DEV_EDU write_rc=$write_rc read_rc=$read_rc result=$observed"\n'
        'result_rc=1\n'
        'if test "$write_rc" = 0 && test "$read_rc" = 0 && test "$observed" = 3628800; then result_rc=0; fi\n'+
        observation_finish()+
        'kill "$learner_pid"\nwait "$learner_pid"\necho LEARNER_DAEMON_EXIT=$?\n'
        'echo LEARNER_RC=$result_rc\n')

def observability_checks(output, manifest):
    mode = manifest.get('observability')
    if mode is None: return {} # Immutable historical manifests retain their scope.
    clean = output.replace('\r', '')
    sections = re.findall(r'^LEARNER_SLOG2_BEGIN\n(.*?)^LEARNER_SLOG2_END rc=0$', clean, re.M|re.S)
    logs = sections[0] if len(sections) == 1 else ''
    checks = {'finite_slog2':len(sections) == 1 and bool(logs.strip())}
    if mode == 'pulse-slog2-v1':
        checks.update(
            pulse_handoff=re.findall(r'^EDU RESMGR PULSE sequence=(\d+) input=(\d+) result=(\d+) sent=1 received=1 owner=same-thread$',clean,re.M) == [('1','10','3628800')],
            bounded_slog2_config=clean.splitlines().count('EDU RESMGR SLOG2 configured pages=1 limit=8') == 1,
            slog2_irq=re.findall(r'EDU_EVENT irq sequence=(\d+) input=(\d+) result=(\d+) ack=([0-9a-f]{8})$',logs,re.M) == [('1','10','3628800','00000000')],
            slog2_pulse=re.findall(r'EDU_EVENT pulse sequence=(\d+) input=(\d+) result=(\d+)$',logs,re.M) == [('1','10','3628800')])
    elif mode == 'slog2-v1':
        actual = re.findall(r'^LEARNER_MMIO id=([0-9a-f]{8}) write=([0-9a-f]{8}) read=([0-9a-f]{8})$',clean,re.M)
        logged = re.findall(r'EDU_EVENT mmio id=([0-9a-f]{8}) write=([0-9a-f]{8}) read=([0-9a-f]{8})$',logs,re.M)
        checks['slog2_actual_mmio'] = len(actual) == 1 and logged == actual
    else: checks['known_observability_mode'] = False
    return checks

def trace_observation(output):
    clean = output.replace('\r', '')
    parts = re.findall(r'^LEARNER_TRACE_BEGIN format=hex\n(.*?)^LEARNER_TRACE_END rc=0$',clean,re.M|re.S)
    if not parts:
        return {'status':'OMITTED' if 'LEARNER_TRACE OMITTED tools_absent' in clean else 'UNVERIFIED',
                'coverage':'UNVERIFIED; no timing/performance claim'}, None
    if len(parts) != 1 or not re.fullmatch(r'[0-9a-f\s]+',parts[0]):
        raise ValueError('ambiguous or corrupt optional trace envelope')
    try: data = bytes.fromhex(parts[0])
    except ValueError as error: raise ValueError('corrupt optional trace bytes') from error
    if not 0 < len(data) <= 65536: raise ValueError('optional trace outside64KiB bound')
    return {'status':'CAPTURED', 'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest(),
            'coverage':'UNVERIFIED; kernel slice not decoded, no timing/performance claim'}, data

def dev_edu_oracle(output, manifest):
    clean = output.replace('\r', '')
    binding = f"LEARNER_BIND source={manifest['source_sha256']} binary={manifest['binary_sha256']}"
    events = [line.split(' ',1)[0].split('=',1)[0] for line in clean.splitlines()
              if line.startswith(('LEARNER_BIND ', 'LEARNER_DEV_EDU ', 'LEARNER_RC='))]
    return {
        'binding':clean.splitlines().count(binding) == 1,
        'ordering':events == ['LEARNER_BIND','LEARNER_DEV_EDU','LEARNER_RC'],
        'qnx_target':bool(re.search(r'^EDU TARGET QNX 8[.]0(?:[.]\d+)? ',clean,re.M)),
        'normal_io':re.findall(r'^LEARNER_DEV_EDU write_rc=(\d+) read_rc=(\d+) result=(\d+)$',clean,re.M) == [('0','0','3628800')],
        'irq_completion':re.findall(r'^EDU RESMGR IRQ completion=(\d+) input=(\d+) result=(\d+) ack=([0-9a-f]{8})$',clean,re.M) == [('1','10','3628800','00000000')],
        'exit_zero':re.findall(r'^LEARNER_RC=(\d+)$',clean,re.M) == ['0'],
        **observability_checks(clean, manifest)}

def init(work, stage="step3"):
    manifest_kind(stage)
    if not REPO_COPY:
        raise ValueError('init requires the repository copy; standalone SDK copy supports build/run')
    work = external(work)
    work.mkdir(parents=True, exist_ok=True)
    source = work / 'main.c'
    if source.exists():
        raise ValueError('refusing to overwrite learner source')
    source.write_text((ROOT/'steps'/stage/'starter/main.c').read_text())
    return source

def measured_shell(action):
    # Read-only guest diagnostics, before/after each already-serialized phase.
    probe = ('echo "BUILD_RESOURCE phase=$0 point=$1"; free -m; '
             "ps -eo pid,comm,rss,stat --sort=-rss | sed -n '1,12p'")
    # Preserve positional SDK/build paths while the probe uses its own $1.
    return ('set -eo pipefail; source "$1"; resource_probe() { '+probe+'; }; '
            'resource_probe before; '+action+'; resource_probe after')

def build(source, out, env, buildfile, cwd, stage="step3"):
    """Run inside learner licensed SDK environment; no private bundle needed.

    Learner BSP buildfile must install learner_bin and learner-start.sh from out.
    It must invoke /proc/boot/learner-start.sh after PCI server startup.
    """
    kind = manifest_kind(stage)
    source = Path(source).resolve()
    out = external(out)
    out.mkdir(parents=True, exist_ok=True)
    snapshot = out/'learner-source.c'
    if source == snapshot:
        raise ValueError('edit main.c, not the generated source snapshot')
    (out/'manifest.json').unlink(missing_ok=True)
    for stale in ['learner.o','learner_bin','learner.ifs']:
        (out/stale).unlink(missing_ok=True)
    snapshot.write_bytes(source.read_bytes())
    binary = out/'learner_bin'
    image = out/'learner.ifs'
    script = out/'learner-start.sh'
    build_hash = sha(buildfile)
    obj = out/'learner.o'
    # One compiler, then one linker, then mkifs. No -g3 or parallel build jobs.
    subprocess.run(['bash', '-c',
        measured_shell('qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g0 -Wall -Wextra -Wno-unused-variable -c "$3" -o "$2"'),
        'learner-compile', str(Path(env).resolve()), str(obj), str(snapshot)], check=True)
    subprocess.run(['bash', '-c',
        measured_shell('qcc -Vgcc_ntox86_64 -o "$2" "$3" -lpci -lslog2'),
        'learner-link', str(Path(env).resolve()), str(binary), str(obj)], check=True)
    if not binary.read_bytes().startswith(b'\x7fELF'):
        raise ValueError('qcc did not produce an ELF binary')
    binary_hash = sha(binary)
    source_hash = sha(snapshot)
    script.write_text(startup(stage, source_hash, binary_hash))
    subprocess.run(['bash', '-c', measured_shell('mkifs "$2" "$3"'),
        'learner-image', str(Path(env).resolve()), str(Path(buildfile).resolve()), str(image)], cwd=cwd, check=True)
    if not image.is_file() or image.stat().st_size == 0:
        raise ValueError('mkifs did not produce a nonempty image')
    if sha(source) != source_hash or sha(buildfile) != build_hash:
        raise ValueError('inputs changed during build')
    manifest = {'kind':kind, 'observability':'pulse-slog2-v1' if stage == 'step6' else 'slog2-v1', 'source_sha256':source_hash,
        'object_sha256':sha(obj), 'binary_sha256':binary_hash, 'image_sha256':sha(image),
        'build_sequence':['compile -O0 -g0','link','mkifs'],
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
        'exit_zero':re.findall(r'^LEARNER_RC=(\d+)$', clean, re.M) == ['0'],
        **observability_checks(clean, manifest)}
    return checks

def verify_inputs(source, bundle, stage="step3"):
    bundle = external(bundle)
    m = json.loads((bundle/'manifest.json').read_text())
    if m.get('kind') != manifest_kind(stage):
        raise ValueError('not a learner build manifest; reference receipts cannot satisfy this stage')
    for path, key in [(Path(source),'source_sha256'),(bundle/'learner-source.c','source_sha256'),
                      (bundle/'learner_bin','binary_sha256'),(bundle/'learner.ifs','image_sha256'),
                      (bundle/'learner-start.sh','startup_sha256')]:
        if sha(path) != m[key]:
            raise ValueError(f'{key} mismatch: rebuild your edited source')
    if 'object_sha256' in m and sha(bundle/'learner.o') != m['object_sha256']:
        raise ValueError('object_sha256 mismatch: rebuild your edited source')
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

def run(source, bundle, disk, receipt, timeout=180, stage="step3"):
    if type(timeout) is not int or not 1 <= timeout <= 900:
        raise ValueError("native timeout must be 1..900 seconds; caps are unchanged")
    bundle = external(bundle)
    m = verify_inputs(source, bundle, stage)
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
        '-nic','user,model=virtio-net-pci','-device','edu,addr=05.0,dma_mask=0xffffffff']
    # Fixed EDU topology; slot5 PIRQ0 was observed routed to target IRQ10.
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
    checks = oracle(output,m) if stage == "step3" else dev_edu_oracle(output,m)
    checks['bounded_completion'] = stop_reason == 'target completed'
    checks['inputs_unchanged_after_boot'] = verify_inputs(source, bundle, stage) == m
    checks['disk_unchanged'] = sha(disk) == disk_hash
    checks['qemu_reaped'] = owned_pid is not None and not (Path('/proc')/str(owned_pid)).exists()
    try:
        trace, trace_bytes = trace_observation(output)
    except ValueError as error:
        trace, trace_bytes = {'status':'UNVERIFIED','error':str(error)}, None
        checks['optional_trace_envelope'] = False
    success = bool(cap) and all(checks.values())
    evidence = dict(m, started=start, finished=time.time(), caps=cap, checks=checks,
                    success=success, qemu_wrapper_returncode=proc.returncode,
                    qemu_command=command, edu_pci_address="05.0",
                    disk_sha256=disk_hash, stop_reason=stop_reason, optional_trace=trace,
                    serialization_lock=str(lock), lease='caller-held flock observed locked',
                    run_driver_sha256=sha(Path(__file__)), timeout_seconds=timeout,
                    target_returncode=re.findall(r'LEARNER_RC=(\d+)',output),
                    observation='fresh custom QNX boot, not QSTI or hardware qualification',
                    substrate_note=os.environ.get('EDU_LEARNER_SUBSTRATE','learner supplied BSP; portability not inferred'))
    receipt = Path(receipt)
    receipt.parent.mkdir(parents=True,exist_ok=True)
    receipt.with_suffix('.log').write_text(output)
    if trace_bytes is not None:
        receipt.with_suffix('.trace.kev').write_bytes(trace_bytes)
    receipt.with_suffix('.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(output)
    if not success:
        print('FAIL: '+stop_reason+'; inspect target exit and MMIO read-back; expected ID 010000ed, write 12345678, complement edcba987. Rebuild after edits.' if stage == 'step3' else 'FAIL: '+stop_reason+'; inspect /dev/edu normal I/O and IRQ completion.')
    else:
        print('PASS: learner step3 source-bound native BAR read-back' if stage == 'step3' else 'PASS: learner /dev/edu source-bound native normal I/O')
    return 0 if success else 1

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='action',required=True)
    i = sub.add_parser('init'); i.add_argument('--work',required=True)
    b = sub.add_parser('build')
    for arg in ['source','out','sdp-env','buildfile','bsp-cwd']: b.add_argument('--'+arg,required=True)
    r = sub.add_parser('run'); r.add_argument('--timeout', type=int, default=180)
    for arg in ['source','bundle','disk','receipt']: r.add_argument('--'+arg,required=True)
    for command_parser in (i,b,r):
        command_parser.add_argument('--stage', choices=('step3','step6'), default='step3')
    a = p.parse_args()
    try:
        if a.action=='init': print(init(a.work,a.stage)); return 0
        if a.action=='build': print(json.dumps(build(a.source,a.out,a.sdp_env,a.buildfile,a.bsp_cwd,a.stage),indent=2)); return 0
        return run(a.source,a.bundle,a.disk,a.receipt,timeout=a.timeout,stage=a.stage)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as e:
        print('BLOCKED:',e,file=sys.stderr); return 2

if __name__=='__main__': sys.exit(main())
