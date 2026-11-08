import sys,os,time,json,subprocess,selectors,fcntl,hashlib
from pathlib import Path
p=Path("/home/ubuntu/.openclaw/workspace/.openclaw/tmp/qnx-probes-20261108")
lock=open("/home/ubuntu/qnx-host/native-test.lock","a");fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
sys.path.insert(0,"/home/ubuntu/.openclaw/workspace/apps/canopy-qnx/tools")
from native_can_three import assert_caps
report={"caps":assert_caps(),"success":False}
image=Path(sys.argv[1]);disk=Path("/home/ubuntu/qnx-host/guest/shared/qnx-native/disk-edu-libc")
report.update(image_sha256=hashlib.sha256(image.read_bytes()).hexdigest(),disk_sha256=hashlib.sha256(disk.read_bytes()).hexdigest())
r=subprocess.Popen(["qemu-system-x86_64","-machine","pc,accel=tcg","-cpu","max","-smp","1","-m","512","-display","none","-serial","stdio","-monitor","none","-no-reboot","-kernel",str(image),"-drive","file="+str(disk)+",format=raw,if=ide,snapshot=on","-nic","user,model=virtio-net-pci","-object","can-bus,id=canbus0","-device","kvaser_pci,canbus=canbus0","-device","edu,dma_mask=0xffffffff"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
sel=selectors.DefaultSelector();sel.register(r.stdout,selectors.EVENT_READ);raw=bytearray()
def until(marker,timeout=120):
 start=len(raw);end=time.monotonic()+timeout
 while time.monotonic()<end:
  if sel.select(.1):
   chunk=os.read(r.stdout.fileno(),65536)
   if not chunk:raise RuntimeError("guest exit")
   raw.extend(chunk);(p/"native-serial.log").write_bytes(raw)
  if marker.encode() in bytes(raw[start:]).replace(b"\r",b"").split(b"\n"):return bytes(raw[start:]).decode(errors="replace")
 raise TimeoutError(marker)
def cmd(line,marker):
 data=(line+"\n").encode()
 for offset in range(0,len(data),80):r.stdin.write(data[offset:offset+80]);r.stdin.flush();time.sleep(.03)
 return until(marker)
try:
 until("CANOPY_SLM_IMAGE_READY")
 report["inventory"]=cmd("uname -a; for n in secpolcompile secpolpush secpolgenerate secpolmonitor slog2info slogger2 slog2c; do command -v $n; done; pidin ar; ls /proc/boot/*secpol* /dev/secpol* /dev/shmem/slogger2*; echo INVENTORY_DONE","INVENTORY_DONE")
 if len(sys.argv)>2:
  report["probe_output"]=cmd("/proc/boot/prereq_ability deny; echo ABILITY_DENY_RC=$?; /proc/boot/prereq_ability; echo ABILITY_DEFAULT_RC=$?; /proc/boot/prereq_containment; echo CONTAINMENT_RC=$?; echo PROBES_DONE","PROBES_DONE")
  report["slog_output"]=cmd("/proc/boot/prereq_slog; echo SLOG_PRODUCER_RC=$?; /proc/boot/slog2info -b canopy_prereq -f -S -t; echo SLOG_CAPTURE_RC=$?; echo SLOG_DONE","SLOG_DONE")
 report["success"]=True
except Exception as e:report["error"]=str(e)
finally:
 r.terminate()
 try:r.wait(10)
 except subprocess.TimeoutExpired:r.kill();r.wait()
 report["stopped_reaped"]=True;(p/"native-receipt.json").write_text(json.dumps(report,indent=2));print(json.dumps(report))
