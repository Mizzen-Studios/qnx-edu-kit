#!/usr/bin/env python3
"""Read-only single-host plan; no SDK installation, activation, build or VM launch."""
import argparse
import json
import os
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import sys
import learner_lab as lab
import learner_clean_preflight as clean
ROOT = Path(__file__).resolve().parents[1]


def plan(env, bsp, qemu, work, probe=False):
    env, bsp, qemu, work = [Path(x).expanduser().resolve() for x in (env,bsp,qemu,work)]
    lab.external(work)
    checks = dict(linux_x86_64=platform.system()=='Linux' and platform.machine()=='x86_64',
                  trusted_sdk_env=env.is_file(), legal_bsp_path=bsp.is_dir(),
                  qemu_executable=qemu.is_file() and os.access(qemu,os.X_OK),
                  fresh_platform=not work.exists(),
                  snippet_safe=not any(c in str(work) for c in ' \t\n|&\\'),
                  host_utilities=all(shutil.which(x) for x in ('flock','systemd-run','systemctl','bash')))
    result=dict(kind='edu-singlehost-plan-v1',label='HOST',checks=checks,
                native_acceptance='NOT_RUN',portability='UNVERIFIED',
                note='BSP path existence is not compatibility or entitlement proof. Use an already installed compatible legal BSP. No licence prompts or installation.')
    if probe and checks['trusted_sdk_env']:
        result['sdk_preflight']=clean.probe(env,work/'platform')
        checks['sdk_preflight']=result['sdk_preflight']['ready_for_clean_build_attempt']
        service=subprocess.run(['systemctl','--user','show-environment'],capture_output=True,timeout=10)
        checks['user_scope_available']=service.returncode==0
    else:
        checks['sdk_preflight']=False
        result['next_gate']='Rerun with --probe-sdk only on your licensed host after trusting the supplied environment script.'
    quote=lambda x:shlex.quote(str(x))
    values=dict(EDU_REPO=ROOT,EDU_WORK=work,EDU_SDP_ENV=env,EDU_BSP=bsp,
                EDU_QEMU=qemu,EDU_PLATFORM=work/'platform',EDU_ACTIVE=work/'step3/bundle',
                EDU_SOURCE=work/'step3/main.c',EDU_SNIPPET=ROOT/'scripts/learner-step3.build.in',
                EDU_NATIVE_LOCK=work/'native.lock')
    commands=['export '+k+'='+quote(v) for k,v in values.items()]
    commands += ['export PATH="$(dirname "$EDU_QEMU"):$PATH"',
                 'python3 "$EDU_REPO/scripts/learner_session.py" init --work "$EDU_WORK"',
                 '# Open $EDU_WORK/cockpit.html; predict, download/import notes, and edit $EDU_SOURCE.',
                 '# Verify selected BSP is installed for mkqnximage; this helper does not select/install a BSP.',
                 'flock "$EDU_NATIVE_LOCK" bash "$EDU_REPO/scripts/learner_bootstrap.sh"',
                 '# Preseed is not completion. Use notebook source-bound build/run commands. Stop on any failure.']
    result['commands']=commands
    result['ready_for_attempt']=all(checks.values())
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('sdp-env','bsp','qemu','work'):p.add_argument('--'+name,required=True)
    p.add_argument('--probe-sdk',action='store_true',help='source your explicitly trusted SDK environment for existing read-only preflight')
    a=p.parse_args()
    try:
        result=plan(a.sdp_env,a.bsp,a.qemu,a.work,a.probe_sdk)
        print(json.dumps(result,indent=2));return 0 if result['ready_for_attempt'] else 2
    except (OSError,ValueError,subprocess.SubprocessError) as e:
        print(json.dumps(dict(label='HOST',blocked=str(e),native_acceptance='NOT_RUN')));return 2

if __name__=='__main__':sys.exit(main())
