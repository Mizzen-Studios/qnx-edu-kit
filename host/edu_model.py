"""Source-derived teaching model, NOT QNX, not an emulator or live device proof.
Reference: qemu/qemu 11aa0b1ff115b86160c4d37e7c37e6a6b13b77ea hw/misc/edu.c.
Source SHA256: 198754be868d35d72dd7f83c91491856cbd76cf5d9fc4ad71bf950ab761d7ad6.
Explicit completion replaces QEMU threads/timers. Driver contracts are stricter
than hardware (0..12 factorial, bounded DMA) to reject unsafe teaching inputs.
"""
import math

SOURCE = 'source-derived host model; NOT QNX; not live evidence'
class EduModel:
    def __init__(self, dma_mask=(1 << 28)-1):
        self.dma_mask = dma_mask
        self.liveness = 0
        self.result = 0
        self.busy = False
        self.irq_enabled = False
        self.irq = 0
        self.device_buffer = bytearray(4096)

    def echo(self, value):
        self.liveness = ~value & 0xffffffff
        return self.liveness

    def submit(self, value):
        if self.busy:
            raise BlockingIOError('request in progress')
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 12:
            raise ValueError('driver contract requires integer 0..12')
        self.result = value
        self.busy = True

    def complete(self):
        if not self.busy:
            raise RuntimeError('no pending request')
        self.result = math.factorial(self.result)
        self.busy = False
        if self.irq_enabled:
            self.irq |= 1
        return self.result

    def raise_irq(self, bits):
        self.irq |= bits & 0xffffffff

    def acknowledge(self, bits):
        self.irq &= ~bits & 0xffffffff

    def dma_address(self, address, count):
        # Fail closed instead of QEMU's address clamping. No physical DMA occurs.
        if (not isinstance(address, int) or isinstance(address, bool)
                or not isinstance(count, int) or isinstance(count, bool)
                or count <= 0 or count > 4096 or address < 0
                or address + count - 1 > self.dma_mask):
            raise ValueError('DMA range outside driver contract')
        return address

class Reprobe:
    """Lifecycle design model; not a QNX supervisor or reset implementation.
    Resources are acquired transactionally; any failure unwinds in reverse.
    Device state persists across process replacement: stale IRQ must be drained.
    """
    ORDER = ('pci', 'bar', 'abilities', 'ist', 'endpoint')
    OWNED_IRQ_MASK = 0x101
    def __init__(self, device):
        self.device = device
        self.owned = []
        self.generation = 0
        self.ready = False
        self.published = False
        self.events = []

    def start(self, fail_at=None):
        if self.owned:
            raise RuntimeError('already attached')
        if self.device.busy:
            raise TimeoutError('old work pending; bounded drain required')
        try:
            for resource in self.ORDER:
                if resource == fail_at:
                    raise OSError('injected host-model acquisition failure')
                self.owned.append(resource)
                self.events.append(('acquire', resource))
            self.device.acknowledge(self.device.irq & self.OWNED_IRQ_MASK)
            self.events.append(('drain', 'owned-status'))
            self.device.irq_enabled = True
            self.generation += 1
            self.published = True
            self.events.append(('publish', 'endpoint'))
            self.ready = True
        except OSError:
            self.stop()
            raise

    def stop(self):
        self.ready = False
        self.published = False
        self.device.irq_enabled = False
        for resource in reversed(self.owned):
            self.events.append(('release', resource))
        self.owned.clear()
