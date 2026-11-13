import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class StockIRQMode(unittest.TestCase):
    def test_read_only_opt_in_keeps_real_irq_gate(self):
        s=(ROOT/'native/edu_resmgr.c').read_text()
        self.assertIn('strcmp(argv[1], "--pci-line")',s)
        self.assertIn('argc == 2 ? "pci-line" : "pci-api"',s)
        self.assertIn('pci_device_cfg_rd8(bdf, 0x3c',s)
        self.assertIn('pci_device_cfg_rd8(bdf, 0x3d',s)
        self.assertIn('config_line >= 16',s)
        self.assertIn('irq = config_line;',s)
        self.assertNotIn('pci_device_cfg_wr',s)
        self.assertNotIn('qtest',s)
        self.assertIn('InterruptWait(0, NULL)',s)
        self.assertIn('int complete = (pending & 1U) && !(regs[8] & 1U)',s)
        self.assertLess(s.index('if (pending) regs[0x64/4] = pending;'),s.index('InterruptUnmask(0, irq_id)'))
        self.assertIn('return wait_error;',s)
    def test_step6_snapshots_share_opt_in(self):
        for name in ['starter','solution']:
            s=(ROOT/'steps/step6'/name/'main.c').read_text()
            self.assertIn('EDU IRQ metadata api=',s)
            self.assertIn('irq = config_line;',s)
if __name__=='__main__': unittest.main()
