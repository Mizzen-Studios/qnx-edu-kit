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
    def test_one_native_retry_receipt_is_bound_and_bounded(self):
        import json,hashlib
        d=ROOT/'docs/acceptance/irq-retry-20261113'
        r=json.loads((d/'receipt.json').read_text())
        self.assertEqual(r['status'],'PASS_ONE_STOCK_FINISH_TRANSACTION')
        self.assertEqual(r['native_boots'],1)
        self.assertEqual(r['stock_image_generation_attempts'],0)
        self.assertFalse(r['wrong_correct_mmio_gates_repeated'])
        self.assertEqual(r['native_oracle']['result'],3628800)
        self.assertTrue(all(r['native_oracle']['checks'].values()))
        self.assertTrue(r['no_routing_rewrite_or_qtest'])
        self.assertTrue(r['cleanup']['actual_lease_free'])
        self.assertEqual(r['observed_selection']['selected_irq'],11)
        for name,digest in r['evidence'].items():
            self.assertEqual(hashlib.sha256((d/name).read_bytes()).hexdigest(),digest,name)
        self.assertEqual(hashlib.sha256((d/'learner-source.c').read_bytes()).hexdigest(),r['source_sha256'])
if __name__=='__main__': unittest.main()
