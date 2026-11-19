#!/usr/bin/env python3
"""Controlled cooperative stock builder; not cryptographic SDK attestation."""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, time, uuid
from pathlib import Path
import learner_lab as lab
ROOT=Path(__file__).resolve().parents[1]
KIND='edu-independent-stock-build-v1'
COMMAND=['mkqnximage','--type=qemu','--arch=x86_64','--ram=512M','--cpu=1','--ssh-ident=none','--build']
ARTIFACTS=('ifs.bin','disk-qemu','disk-qemu.vmdk','qemu_options','options')
FIELDS=set('kind id recipe builder_sha256 repo_commit repo_tree tools tools_after artifacts inputs log_sha256 returncode eof started finished project stock environment_sha256 provenance'.split())
def external(value):
 p=Path(value)
 if not p.is_absolute() or '..' in p.parts or any(c.isspace() for c in str(p)): raise ValueError('absolute external path without traversal/whitespace required')
 if any(x.is_symlink() for x in [p,*p.parents]): raise ValueError('symlink path rejected')
 return lab.external(p)
def inventory(root):
 result={}
 for p in sorted(root.rglob('*')):
  if p.is_symlink(): raise ValueError('symlink input rejected')
  if p.is_file(): result[str(p.relative_to(root))]=lab.sha(p)
 return result
def tools():
 result={}
 for name in ('mkqnximage','mkifs','qcc'):
  p=Path(shutil.which(name) or '/missing').resolve(strict=True)
  v=subprocess.run([str(p),'-V'] if name=='qcc' else [str(p),'-?'],capture_output=True,timeout=20)
  result[name]=dict(path=str(p),sha256=lab.sha(p),version_rc=v.returncode,version_output_sha256=hashlib.sha256(v.stdout+v.stderr).hexdigest())
 return result
def check_project_inputs(m):
 # Tools and project stay inside SDK. Host checks a separate owner finalization.
 if not isinstance(m.get('inputs'),dict): raise ValueError('missing input measurement')

def build(project,stock,environment):
 project=external(project);stock=external(stock);environment=Path(environment)
 if project.exists() or stock.exists(): raise ValueError('fresh project and stock output required')
 if not environment.is_file(): raise ValueError('existing SDK environment required')
 if os.environ.get('EDU_STOCK_BUILDER')!='sole-owner': raise ValueError('supervised sole owner required')
 # Obtain the environment from the named existing setup, not the caller shell.
 raw=subprocess.check_output(['bash','--noprofile','--norc','-c','set -e; source "$1" >/dev/null; env -0','stock-env',str(environment)],env={'HOME':os.environ.get('HOME','/home/qnx'),'PATH':'/usr/bin:/bin','LANG':'C'})
 sourced=dict(item.decode().split('=',1) for item in raw.split(bytes([0])) if item)
 os.environ.clear();os.environ.update(sourced)
 if len(Path('/proc/swaps').read_text().splitlines())!=1: raise ValueError('SDK guest swap active; no swap change authorized')
 measured=tools();started=time.time()
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 tree=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=ROOT,text=True).strip()
 if subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT): raise ValueError('builder checkout must be clean')
 project.mkdir(parents=True);stock.mkdir(parents=True)
 snippets=project/'local/snippets';snippets.mkdir(parents=True)
 (snippets/'qemu_options.edu').write_text('-device edu\n')
 env={k:v for k,v in os.environ.items() if k in ('HOME','PATH','QNX_HOST','QNX_TARGET','QNX_CONFIGURATION','QNX_LICENSE','LM_LICENSE_FILE','LD_LIBRARY_PATH','TMPDIR','LANG','LC_ALL')}
 env['LANG']='C';env['LC_ALL']='C'
 for k in list(env):
  if k.startswith(('OPT_','MKQNX','QEMU_')): del env[k]
 with (stock/'build.private.log').open('wb') as log:
  rc=subprocess.run(COMMAND,cwd=project,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
 after=tools()
 if rc!=0 or after!=measured: raise ValueError('stock tool failure/change; inspect private build log')
 if set(inventory(project/'local'))!={'options','snippets/qemu_options.edu'}: raise ValueError('unexpected generated local inventory')
 if {p.name for p in snippets.iterdir()}!={'qemu_options.edu'} or (snippets/'qemu_options.edu').read_text()!='-device edu\n': raise ValueError('custom snippet rejected')
 sources={'ifs.bin':project/'output/ifs.bin','disk-qemu':project/'output/disk-qemu','disk-qemu.vmdk':project/'output/disk-qemu.vmdk','qemu_options':project/'output/build/qemu_options','options':project/'local/options'}
 for name,p in sources.items():
  if not p.resolve().is_relative_to(project) or not p.is_file() or p.stat().st_size==0: raise ValueError('missing/unsafe generated artifact '+name)
  shutil.copyfile(p,stock/name)
 m=dict(kind=KIND,id=str(uuid.uuid4()),recipe=COMMAND,builder_sha256=lab.sha(__file__),repo_commit=commit,repo_tree=tree,tools=measured,tools_after=after,artifacts={n:lab.sha(stock/n) for n in ARTIFACTS},inputs=inventory(project/'local'),log_sha256=lab.sha(stock/'build.private.log'),returncode=rc,eof=True,started=started,finished=time.time(),project=str(project),stock=str(stock),environment_sha256=lab.sha(environment),provenance='cooperative controlled builder; NOT cryptographic stock attestation or licence certification')
 (stock/'stock-build.json').write_text(json.dumps(m,indent=2)+'\n');verify(stock,False)
 return m
def verify(stock, finalized=True, owner_sha256=None):
 stock=external(stock);p=stock/'stock-build.json'
 if p.is_symlink(): raise ValueError('symlink manifest')
 m=json.loads(p.read_text())
 if not isinstance(m,dict): raise ValueError('manifest object required')
 if set(m)!=FIELDS or m['kind']!=KIND or m['recipe']!=COMMAND: raise ValueError('unsupported stock provenance schema/recipe')
 if type(m['returncode']) is not int or m['returncode']!=0 or m['eof'] is not True: raise ValueError('incomplete stock build')
 if str(uuid.UUID(m['id']))!=m['id'] or any(not re.fullmatch('[0-9a-f]{40}',m[k]) for k in ('repo_commit','repo_tree')): raise ValueError('malformed build identity')
 if any(type(m[k]) not in (int,float) for k in ('started','finished')) or m['finished']<=m['started']: raise ValueError('invalid build times')
 if m['builder_sha256']!=lab.sha(__file__) or m['tools']!=m['tools_after'] or set(m['tools'])!={'mkqnximage','mkifs','qcc'}: raise ValueError('builder/tools changed')
 for t in m['tools'].values():
  if set(t)!=set('path sha256 version_rc version_output_sha256'.split()) or type(t['version_rc']) is not int or any(not re.fullmatch('[0-9a-f]{64}',t[k]) for k in ('sha256','version_output_sha256')): raise ValueError('malformed tool measurement')
 if set(m['artifacts'])!=set(ARTIFACTS) or not isinstance(m['stock'],str): raise ValueError('mixed stock bundle')
 for n,d in m['artifacts'].items():
  p=stock/n
  if p.is_symlink() or not re.fullmatch('[0-9a-f]{64}',d) or lab.sha(p)!=d: raise ValueError('changed stock artifact '+n)
 if (stock/'build.private.log').is_symlink(): raise ValueError('symlink build log')
 descriptor=(stock/'disk-qemu.vmdk').read_text()
 extents=re.findall(r'^RW ([0-9]+) FLAT "([^"]+)" 0$',descriptor,re.M)
 if len(extents)!=1 or extents[0][1]!='disk-qemu' or int(extents[0][0])*512>(stock/'disk-qemu').stat().st_size: raise ValueError('unsafe VMDK backing extent')
 if (stock/'qemu_options').read_text().split()!=['-device','edu']: raise ValueError('unsupported QEMU options')
 options=(stock/'options').read_text()
 for name,value in [('OPT_RAM','512M'),('OPT_CPU','1')]:
  if not any(line.split('=',1)[0]==name and line.split('=',1)[-1].strip(chr(34)+chr(39))==value for line in options.splitlines()): raise ValueError('unsupported stock target options')
 if not isinstance(m['inputs'],dict): raise ValueError('input object required')
 if m['inputs'].get('options')!=m['artifacts']['options']: raise ValueError('generated options input mismatch')
 if not isinstance(m['inputs'],dict) or set(m['inputs'])!={'options','snippets/qemu_options.edu'} or m['inputs'].get('snippets/qemu_options.edu')!=hashlib.sha256(b'-device edu\n').hexdigest() or any(k.startswith('snippets/') and k!='snippets/qemu_options.edu' for k in m['inputs']): raise ValueError('custom snippet provenance')
 if any('..' in Path(k).parts or Path(k).is_absolute() or not re.fullmatch('[0-9a-f]{64}',v) for k,v in m['inputs'].items()): raise ValueError('unsafe input inventory')
 check_project_inputs(m)
 if finalized:
  owner_path=stock/'stock-owner.json'
  if owner_path.is_symlink(): raise ValueError('symlink owner receipt')
  if not isinstance(owner_sha256,str) or not re.fullmatch('[0-9a-f]{64}',owner_sha256) or lab.sha(owner_path)!=owner_sha256: raise ValueError('explicit trusted owner receipt digest required')
  owner=json.loads(owner_path.read_text())
  expected={'kind':'edu-independent-stock-owner-v1','build_sha256':lab.sha(stock/'stock-build.json'),'stock':str(stock),'builder_sha256':lab.sha(__file__),'caps':{'cpu.max':'100000 100000','memory.max':'2147483648','memory.swap.max':'0'},'stopped_reaped':True,'queue_clear':True,'foreign_qemu':0}
  if json.dumps(owner,sort_keys=True)!=json.dumps(expected,sort_keys=True): raise ValueError('missing/mixed/forged typed owner completion')
 if lab.sha(stock/'build.private.log')!=m['log_sha256']: raise ValueError('changed build log')
 return m
def main():
 p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='action',required=True)
 b=s.add_parser('build')
 for n in ('project','stock','environment'): b.add_argument('--'+n,required=True)
 v=s.add_parser('verify');v.add_argument('--stock',required=True);v.add_argument('--owner-sha256',required=True);a=p.parse_args()
 try:
  m=build(a.project,a.stock,a.environment) if a.action=='build' else verify(a.stock,owner_sha256=a.owner_sha256)
  print(json.dumps(m,indent=2));return 0
 except (ValueError,OSError,KeyError,TypeError,subprocess.SubprocessError) as e: print('BLOCKED:',e,file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
