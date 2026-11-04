#!/usr/bin/env python3
"""Real QEMU EDU probe. No SDK/model/guest. QMP advances TCG virtual time."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import resource
import shutil
import select
import socket
import subprocess
import tempfile
import time
ROOT = Path(__file__).resolve().parents[1]
PIN = '11aa0b1ff115b86160c4d37e7c37e6a6b13b77ea'
SOURCE_HASH = '198754be868d35d72dd7f83c91491856cbd76cf5d9fc4ad71bf950ab761d7ad6'
class Probe:
    def __init__(self, directory, mask=None):
        self.directory = Path(directory)
        self.irq = {}
        self.events = []
        path = str(self.directory/'qmp.sock')
        self.args = ['qemu-system-x86_64','-machine','pc','-accel','tcg,thread=single',
                     '-S','-display','none','-nodefaults','-m','512M','-nic','none',
                     '-device','edu,addr=04.0'+('' if mask is None else ',dma_mask='+hex(mask)),
                     '-qtest','stdio','-qtest-log',str(self.directory/'protocol.txt'),
                     '-qmp','unix:'+path+',server=on,wait=off']
        bios=self.directory/'halt-bios.txt'
        bios.write_bytes(bytes(65520)+bytes.fromhex('faf4ebfd')+bytes(12))
        self.args += ['-bios',str(bios)]
        self.err = (self.directory/'stderr.txt').open('w+')
        self.p = subprocess.Popen(self.args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,bufsize=0,preexec_fn=lambda:resource.setrlimit(resource.RLIMIT_CORE,(0,0)))
        self.buffer = b''
        self.sock = socket.socket(socket.AF_UNIX)
        self.sock.settimeout(5)
        deadline = time.monotonic()+5
        while True:
            try:
                self.sock.connect(path)
                break
            except (FileNotFoundError,ConnectionRefusedError):
                if time.monotonic()>deadline:
                    self.p.terminate(); self.p.wait(timeout=3)
                    raise TimeoutError('QMP startup')
                time.sleep(.01)
        self.qmp = self.sock.makefile('rwb',buffering=0)
        self.qmp.readline()
        self.monitor('qmp_capabilities')
        print('COMMAND',' '.join(self.args).replace(str(self.directory),'<workspace-temp>'))
    def monitor(self,name,arguments=None):
        self.qmp.write((json.dumps({'execute':name,'arguments':arguments or {}})+'\n').encode())
        while True:
            if not select.select([self.sock],[],[],5)[0]: raise TimeoutError('QMP '+name)
            value=json.loads(self.qmp.readline())
            if 'error' in value: raise RuntimeError(value)
            if 'return' in value: return value['return']
    def command(self,text):
        self.p.stdin.write((text+'\n').encode())
        deadline=time.monotonic()+5
        while time.monotonic()<deadline:
            if b'\n' not in self.buffer:
                if not select.select([self.p.stdout],[],[],5)[0]: raise TimeoutError(text)
                data=os.read(self.p.stdout.fileno(),65536)
                if not data: raise RuntimeError('QEMU exited: '+text)
                self.buffer+=data
                continue
            line,self.buffer=self.buffer.split(b'\n',1)
            line=line.decode()
            if line.startswith('EDU: clamping DMA '):
                print('DEVICE',line)
                continue
            if line.startswith('IRQ '):
                _,edge,number=line.split()
                self.irq[int(number)]=edge=='raise'
                self.events.append(line)
                continue
            if not line.startswith('OK'): raise RuntimeError(text+': '+line)
            return line[2:].strip()
        raise TimeoutError(text)
    def cfg(self,offset,value=None):
        self.command('outl 0xcf8 '+hex(0x80002000+offset))
        if value is None: return int(self.command('inl 0xcfc'),16)
        self.command('outl 0xcfc '+hex(value))
    def read(self,offset,width='l'):
        return int(self.command('read'+width+' '+hex(0xe0000000+offset)),16)
    def write(self,offset,value,width='l'):
        self.command('write'+width+' '+hex(0xe0000000+offset)+' '+hex(value))
    def setup(self):
        assert self.cfg(0)==0x11e81234
        self.cfg(0x10,0xffffffff)
        assert self.cfg(0x10)==0xfff00000
        self.cfg(0x10,0xe0000000); self.cfg(4,6)
        assert self.cfg(4)&6==6
        self.command('outl 0xcf8 0x80000860'); self.command('outl 0xcfc 0x0b0b0b0b')
        self.command('irq_intercept_in ioapic')
        print('PASS PCI 1234:11e8 BAR0=0xe0000000 size=0x100000 memory MEM+MASTER PIRQ->11')
    def advance(self):
        self.monitor('cont'); time.sleep(.15); self.monitor('stop')
    def wait(self,predicate,label):
        deadline=time.monotonic()+3
        while time.monotonic()<deadline:
            if predicate(): return
            time.sleep(.001)
        raise TimeoutError(label)
    def close(self):
        if self.p.poll() is None:
            self.p.terminate()
            try: self.p.wait(timeout=3)
            except subprocess.TimeoutExpired: self.p.kill(); self.p.wait(timeout=3)
        self.qmp.close(); self.sock.close(); self.err.close()
        self.p.stdin.close(); self.p.stdout.close()
    def dma(self,source,dest,count,cmd,width='q'):
        for offset,value in ((0x80,source),(0x88,dest),(0x90,count)):
            self.write(offset,value,'q'); assert self.read(offset,'q')==value
        self.write(0x98,cmd,width); assert self.read(0x98,'q')==cmd
        self.advance(); assert self.read(0x98,'q')==cmd&~1

def exercise(p,mask):
    p.setup()
    assert p.read(0)==0x010000ed
    assert p.command('read 0xe0000000 4')=='0xed000001'
    p.write(0,0); assert p.read(0)==0x010000ed
    assert p.read(0,'b')==0 and p.read(0,'w')==0
    assert p.read(0,'q')==0xffffffffffffffff
    print('PASS ID offset=0 width=32 value=0x010000ed bytes=ed000001; RO; qtest subword returns zero; 64-bit rejected')
    for value in (0,0xffffffff,0xaaaaaaaa,0x55555555,0x12345678):
        p.write(4,value); assert p.read(4)==value^0xffffffff
    p.write(4,0,'q')
    assert p.read(4)==0xffffffff
    p.wait(lambda:not p.read(0x20)&1,'split factorial write')
    print('PASS liveness offset=4 width=32 five inverse patterns; unaligned64 splits into 32-bit accesses; avoid; subword writes not claimed')
    p.write(0x20,1); assert p.read(0x20)==0
    for value in range(14):
        p.write(8,value)
        p.wait(lambda: not p.read(0x20)&1,'factorial')
        assert p.read(8)==math.factorial(value)&0xffffffff
    # Large input forces an observable busy interval, then bounded drain.
    p.write(8,10000000)
    assert p.read(0x20)&1
    p.write(8,5); p.write(0x20,0)
    assert p.read(0x20)&1
    p.wait(lambda: not p.read(0x20)&1,'large factorial')
    assert p.read(8)==0
    p.write(0x20,0x80); assert p.read(0x20)==0x80
    p.write(8,5)
    p.wait(lambda:p.read(0x24)==1,'factorial IRQ')
    assert p.read(8)==120 and p.irq.get(11)
    p.write(0x64,1); assert p.read(0x24)==0 and not p.irq[11]
    p.write(0x20,0); assert p.read(0x20)==0
    print('PASS factorial offset=8 0..13 modulo32; 10M busy, ignored resubmit; status 0x20 RO busy / RW bit0x80; IRQ bit1')
    p.write(0x60,0x101); assert p.read(0x24)==0x101 and p.irq[11]
    p.write(0x24,0); assert p.read(0x24)==0x101
    p.write(0x64,1); assert p.read(0x24)==0x100 and p.irq[11]
    p.write(0x64,0x100); assert p.read(0x24)==0 and not p.irq[11]
    p.write(0x60,1); assert p.read(0x24)==1 and p.irq[11]
    p.write(0x64,1); assert p.read(0x24)==0 and not p.irq[11]
    print('PASS INTx IOAPIC IRQ11 raise/partial ack/full ack/retrigger; status0x24 raise0x60 ack0x64 width32')
    for off in (0x80,0x88,0x90):
        p.write(off,0x123456789abcdef0,'q'); assert p.read(off,'q')==0x123456789abcdef0
        p.write(off,0x76543210); assert p.read(off,'q')==0x76543210
        assert p.read(off,'b')==0 and p.read(off,'w')==0
    print('PASS DMA src0x80 dst0x88 count0x90 32/64-bit storage; 32-bit write replaces full value')
    for count,offset in ((1,4095),(100,17),(4096,0)):
        payload=bytes((i*37+11)&255 for i in range(count))
        p.command('write 0x100000 '+hex(count)+' 0x'+payload.hex())
        p.dma(0x100000,0x40000+offset,count,1,'l')
        assert p.read(0x24)==0
        p.command('memset 0x200000 '+hex(count)+' 0')
        p.dma(0x40000+offset,0x200000,count,7)
        assert p.command('read 0x200000 '+hex(count))=='0x'+payload.hex()
        assert p.read(0x24)==0x100 and p.irq[11]
        p.write(0x64,0x100); assert p.read(0x24)==0 and not p.irq[11]
        print('PASS DMA roundtrip bytes='+str(count)+' device-offset='+str(offset)+' commands1(width32)/7(width64) completion RUN cleared IRQ0x100')
    # Mask acts on host address, not stored source register.
    high=(mask+1)|0x100000
    payload=b'mask-live-qemu'
    p.command('write 0x100000 '+hex(len(payload))+' 0x'+payload.hex())
    p.dma(high,0x40000,len(payload),1)
    p.dma(0x40000,(mask+1)|0x200000,len(payload),3)
    assert p.command('read 0x200000 '+hex(len(payload)))=='0x'+payload.hex()
    # Last two valid masked bytes, then first address above mask wraps to zero.
    edge=mask-1
    p.dma(0x40000,edge,2,3)
    assert p.command('read '+hex(edge)+' 2')=='0x'+payload[:2].hex()
    p.dma(0x40000,mask+1,2,3)
    assert p.command('read 0 2')=='0x'+payload[:2].hex()
    print('PASS mask boundary last-two bytes and first-above wraps to zero')
    print('PASS dma_mask='+hex(mask)+' high source/dest alias low RAM; property '+('default' if mask==0xfffffff else 'override'))
    p.write(0x98,0,'q'); assert p.read(0x98,'q')==2
    # Running timer prevents parameter changes until completion.
    p.write(0x80,0x100000,'q'); p.write(0x88,0x40000,'q'); p.write(0x90,1,'q'); p.write(0x98,1,'q')
    p.write(0x80,0x300000,'q'); p.write(0x90,2,'q'); p.write(0x98,7,'q')
    assert p.read(0x80,'q')==0x100000 and p.read(0x90,'q')==1 and p.read(0x98,'q')==1
    p.advance(); assert p.read(0x98,'q')==0
    print('PASS DMA busy parameter/command writes ignored; command without RUN ignored')
    print('IRQ11 EVENTS',','.join(e for e in p.events if e.endswith(' 11')))

def invalid_dma(p,count,address):
    p.setup()
    p.write(0x80,0x100000,'q'); p.write(0x88,address,'q')
    p.write(0x90,count,'q'); p.write(0x98,1,'q')
    p.monitor('cont')
    try: p.p.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        p.err.flush(); p.err.seek(0); print('INVALID_DIAGNOSTIC',p.err.read())
        raise
    p.err.flush(); p.err.seek(0)
    error=p.err.read()
    assert p.p.returncode!=0 and 'EDU: DMA range' in error and 'out of bounds' in error
    print('PASS expected QEMU fatal DMA count='+str(count)+' device-address='+hex(address)+' exit='+str(p.p.returncode))
    print('DEVICE',next(line for line in error.splitlines() if 'EDU: DMA range' in line))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',action='store_true',help='explicit opt-in: launch actual QEMU')
    args=parser.parse_args()
    if not args.run: parser.error('--run required; this is not a model test')
    print('LIVE QEMU DEVICE ONLY — NOT QNX',flush=True)
    print('HOST',platform.platform(),platform.machine())
    print('EXECUTABLE_SHA256',hashlib.sha256(Path(shutil.which('qemu-system-x86_64')).read_bytes()).hexdigest())
    print('BASE',subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip())
    print(subprocess.check_output(['qemu-system-x86_64','--version'],text=True).splitlines()[0])
    print('UPSTREAM',PIN,'hw/misc/edu.c SHA256',SOURCE_HASH)
    print('PROBE_SHA256',hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    temp=ROOT/'.tmp'; temp.mkdir(exist_ok=True)
    for mask in (None,0xffffff):
        # Unix socket paths must stay below sockaddr_un limit.
        with tempfile.TemporaryDirectory(prefix='qt-',dir=temp) as directory:
            # Use a short relative path (cwd is repository root).
            p=Probe(Path(directory).relative_to(ROOT),mask)
            try: exercise(p,0xfffffff if mask is None else mask)
            finally: p.close()
    for count,address in ((0,0x40000),(4097,0x40000),(1,0x41000),(2,0x40fff)):
        with tempfile.TemporaryDirectory(prefix='qt-',dir=temp) as directory:
            p=Probe(Path(directory).relative_to(ROOT))
            try: invalid_dma(p,count,address)
            finally: p.close()
    print('PASS live register suite including isolated fatal DMA bounds; QNX and MSI NOT TESTED')
if __name__=='__main__': main()
