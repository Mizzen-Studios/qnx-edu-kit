import hashlib,json,os,re,subprocess
from pathlib import Path
base=Path(__file__).resolve().parent
repo=base/'checkout'; cwd=base/'workdir'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
env=dict(os.environ,EDU_REPO=str(repo),EDU_WORK=str(base/'learner'),EDU_SDP_ENV=str(base/'legal-inputs/qnx800/qnxsdp-env.sh'),EDU_PLATFORM=str(base/'clean-platform'),EDU_ACTIVE=str(base/'learner-active'),EDU_QEMU='/usr/bin/qemu-system-x86_64',EDU_NATIVE_LOCK=str(base/'native-test.lock'),PYTHONDONTWRITEBYTECODE='1',EDU_LIVE_QTEST='0',CLAAT_TOOL_CACHE='')
route=(repo/'docs/learner-route.md').read_text();fence=chr(96)*3;blocks=re.findall(fence+r'sh\n(.*?)'+fence,route,re.S)
records=[]
def run(command,expected,scope):
 p=subprocess.run(['bash','-c',command],cwd=cwd,env=env,text=True,capture_output=True,timeout=180)
 records.append(dict(command=command,cwd=str(cwd),exit_code=p.returncode,expected_exit=expected,scope=scope,stdout=p.stdout,stderr=p.stderr))
 assert p.returncode==expected,records[-1]
for i,b in enumerate(blocks):
 p=subprocess.run(['bash','-n'],input=b,text=True,capture_output=True)
 assert p.returncode==0,p.stderr
run('python3 "$EDU_REPO/scripts/learner_lab.py" --help',0,'host-only CLI/path')
run('"$EDU_QEMU" --version',0,'version only; no guest')
for c in ['command -v flock','command -v systemd-run','systemctl --user show-environment >/dev/null']:
 run(c,0,'host-only utility/session presence; not effective caps')
run('python3 "$EDU_REPO/scripts/learner_clean_preflight.py" --sdp-env "$EDU_SDP_ENV" --fresh-work "$EDU_PLATFORM"',2,'BLOCKED legal setup; no installed SDP at supplied independent path')
for stage,path in [('step3','step3'),('step6','finish')]:
 run(f'python3 "$EDU_REPO/scripts/learner_lab.py" init --stage {stage} --work "$EDU_WORK/{path}"',0,'isolated host-only starter-copy command; not route progression past blocker')
 assert sha(base/'learner'/path/'main.c')==sha(repo/'steps'/stage/'starter/main.c')
run('cd "$EDU_REPO" && ./verify.sh --host-only',0,'existing host suite only; no target rerun')
for c in ['python3 "$EDU_REPO/tools/capability_ledger.py"','python3 "$EDU_REPO/scripts/render_site.py" --check','python3 "$EDU_REPO/docs/review/build_packet.py" --check','git -C "$EDU_REPO" diff --check']:
 run(c,0,'host-only existing gate')
result=dict(schema='edu-route-independent-paths.v1',tested_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),scope='host-only commands and path checks; NO guest, native build or rerun; not a fresh SDK installation or second-SDK portability proof',chosen_paths={k:v for k,v in env.items() if k.startswith('EDU_')},instructions={str(p.relative_to(repo)):sha(p) for p in [repo/'README.md',repo/'codelab/codelab.md',repo/'docs/learner-route.md',repo/'scripts/learner_lab.py',repo/'scripts/learner_clean_preflight.py',repo/'scripts/learner-step3.build.in']},shell_blocks=[dict(index=i,sha256=hashlib.sha256(b.encode()).hexdigest(),exact_text=b,syntax='PASS bash -n',execution='only individual host commands listed in records; legal build/native commands NOT_RUN') for i,b in enumerate(blocks)],records=records,legal_setup=dict(status='BLOCKED',missing=['supplied trusted licensed SDP environment at '+env['EDU_SDP_ENV'],'compatible legal stock Generic x86_64 BSP in this independent environment','matching generated output/build/ifs.build and output/disk-qemu'],existing_sdk='Existing licensed SDK is inside stopped private x86 SDK guest, deliberately not booted or copied; no installation, activation or licence changes.',consequence='qcc/mkqnximage/mkifs builds and step3 wrong/fix plus learner /dev/edu native runs NOT_RUN. Historical native receipts unchanged.'))
(base/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(tested_commit=result['tested_commit'],host_commands=len(records),syntax_blocks=len(blocks),legal_setup='BLOCKED',receipt=str(base/'receipt.json')),indent=2))
