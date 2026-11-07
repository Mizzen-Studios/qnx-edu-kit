"""Host-only provenance checks; never accepts runtime markers as new evidence."""
import importlib.util,json,hashlib,subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('review_packet',ROOT/'docs/review/build_packet.py')
packet=importlib.util.module_from_spec(spec);spec.loader.exec_module(packet)
class ReviewPacket(unittest.TestCase):
 def test_receipt_and_surface_inventory_current(self):
  self.assertEqual(json.loads((ROOT/'docs/review/appendix.json').read_text()),packet.build())
 def test_all_sources_and_generated_pages_covered(self):
  d=packet.build();sources={x['path'] for x in d['source_surfaces']}
  for p in ['README.md','STATUS.md','codelab/codelab.md','REVIEW.md']:self.assertIn(p,sources)
  for page in d['site_projection']:self.assertIn(page['source'],sources)
  self.assertEqual(len(d['evidence']['compile']['binary_hashes_from_raw_log']),12)
 def test_no_archival_commit_promoted_to_tested_commit(self):
  d=packet.build()
  for name in ['reference','reference-clean','compile','step3-wrong','step3-correct','finish','stock-build','export']:
   self.assertTrue(d['evidence'][name]['tested_source_commit'].startswith('UNVERIFIED'))
  self.assertFalse(d['evidence']['export']['current_source_matches_receipt'])
  self.assertFalse(d['evidence']['route-export']['current_source_matches_receipt'])
  self.assertFalse(d['evidence']['bootstrap-export']['current_source_matches_receipt'])
  self.assertTrue(d['evidence']['packaging-export']['current_source_matches_receipt'])
 def test_raw_success_and_negative_control_not_interchanged(self):
  d=packet.build()
  def receipt(k):return json.loads((ROOT/d['evidence'][k]['path']).read_text())
  self.assertFalse(receipt('step3-wrong')['success'])
  self.assertFalse(receipt('step3-wrong')['checks']['device_readback'])
  self.assertTrue(receipt('step3-correct')['success'])
  self.assertTrue(receipt('finish')['checks']['normal_io'])
  self.assertIn('/unmasked/',d['evidence']['finish']['path'])
  self.assertIsNone(receipt('oom')['build_exit_code'])
