import unittest
from host.edu_model import EduModel, Reprobe, SOURCE

class RegisterModel(unittest.TestCase):
    def test_source_label(self):
        self.assertIn('NOT QNX', SOURCE)
    def test_liveness_width(self):
        d = EduModel()
        for v in (0, 1, 0x12345678, 0xffffffff):
            self.assertEqual(d.echo(v), (~v) & 0xffffffff)
    def test_factorials(self):
        d = EduModel()
        for value, result in ((0,1),(1,1),(10,3628800),(12,479001600)):
            d.submit(value)
            self.assertTrue(d.busy)
            self.assertEqual(d.complete(), result)
            self.assertFalse(d.busy)
    def test_busy_does_not_overwrite(self):
        d = EduModel(); d.submit(10)
        with self.assertRaises(BlockingIOError): d.submit(2)
        self.assertEqual(d.complete(), 3628800)
    def test_input_contract(self):
        for value in (-1,13,True,'10',1.5):
            with self.assertRaises(ValueError): EduModel().submit(value)
    def test_no_spurious_completion(self):
        with self.assertRaises(RuntimeError): EduModel().complete()
    def test_irq_ack_preserves_other_sources(self):
        d = EduModel(); d.irq_enabled=True; d.submit(3); d.complete()
        d.raise_irq(0x100); d.acknowledge(1)
        self.assertEqual(d.irq,0x100)
        d.acknowledge(0x100); self.assertEqual(d.irq,0)
    def test_mask_boundary(self):
        d=EduModel(); self.assertEqual(d.dma_address((1<<28)-4,4),(1<<28)-4)
        for a,n in (((1<<28)-4,5),(1<<28,1),(0,0),(0,4097),(-1,1)):
            with self.assertRaises(ValueError): d.dma_address(a,n)
    def test_explicit_mask(self):
        self.assertEqual(EduModel(0xffffffff).dma_address(0x10000000,4096),0x10000000)

class RestartDesign(unittest.TestCase):
    def test_partial_acquisition_unwinds(self):
        for stage in Reprobe.ORDER:
            p=Reprobe(EduModel())
            with self.assertRaises(OSError): p.start(stage)
            acquired=[r for e,r in p.events if e=='acquire']
            released=[r for e,r in p.events if e=='release']
            self.assertEqual(released,list(reversed(acquired)))
            self.assertFalse(p.ready); self.assertEqual(p.owned,[])
    def test_reprobe_drains_stale_status(self):
        d=EduModel(); p=Reprobe(d); p.start(); p.stop()
        d.raise_irq(0x101); p.start()
        self.assertEqual(d.irq,0); self.assertEqual(p.generation,2)
    def test_busy_reprobe_fails_closed(self):
        d=EduModel(); d.submit(10); p=Reprobe(d)
        with self.assertRaises(TimeoutError): p.start()
        self.assertFalse(p.ready); self.assertEqual(p.owned,[])
    def test_double_attach_rejected(self):
        p=Reprobe(EduModel()); p.start()
        with self.assertRaises(RuntimeError): p.start()
    def test_stop_idempotent(self):
        p=Reprobe(EduModel()); p.start(); p.stop(); events=list(p.events); p.stop()
        self.assertEqual(events,p.events)

class ReviewRegressions(unittest.TestCase):
    def test_dma_rejects_fractional_and_boolean(self):
        for a,n in ((0.5,1),(0,1.5),(True,True),(False,1),(0,False)):
            with self.assertRaises(ValueError): EduModel().dma_address(a,n)
    def test_reprobe_preserves_unowned_status(self):
        d=EduModel();d.raise_irq(0x80000101);p=Reprobe(d);p.start()
        self.assertEqual(d.irq,0x80000000)
    def test_publish_after_drain(self):
        p=Reprobe(EduModel());p.start()
        self.assertLess(p.events.index(('drain','owned-status')),p.events.index(('publish','endpoint')))
        self.assertTrue(p.published);p.stop();self.assertFalse(p.published)
    def test_failed_setup_never_publishes(self):
        for stage in Reprobe.ORDER:
            p=Reprobe(EduModel())
            with self.assertRaises(OSError):p.start(stage)
            self.assertFalse(p.published)
            self.assertNotIn(('publish','endpoint'),p.events)
