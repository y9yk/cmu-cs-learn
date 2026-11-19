import json
import unittest
from pathlib import Path
from html.parser import HTMLParser
import re
import subprocess
ROOT=Path(__file__).resolve().parents[1]
EXPECTED={'10-605','15-110','17-214','15-442','17-635','17-643','11-768','17-645','15-259','11-777','17-619','07-280','17-627'}
class CatalogTest(unittest.TestCase):
 def setUp(self): self.data=json.loads((ROOT/'catalog.json').read_text())
 def test_official_inventory(self):
  items=self.data['courses']
  self.assertEqual({i['id'] for i in items},EXPECTED)
  self.assertEqual(len(items),len(EXPECTED))
  self.assertEqual(sum(i['status']=='available' for i in items),8)
  self.assertEqual(sum(i['status']=='planned' for i in items),5)
 def test_routes_resolve(self):
  ids={i['id'] for i in self.data['courses']}
  for route in self.data['routes']:
   self.assertTrue(route['steps'])
   self.assertEqual(len(set(route['steps'])),len(route['steps']))
   self.assertTrue(set(route['steps'])<=ids)
 def test_all_cards_render_and_build_is_current(self):
  html=(ROOT/'docs/index.html').read_text()
  self.assertEqual(set(re.findall(r'<article id="(course-\d\d-\d{3})"',html)),{f'course-{i}' for i in EXPECTED})
  subprocess.run(['python3','build.py','--check'],cwd=ROOT,check=True)
 def test_metadata_labels_and_links(self):
  for c in self.data['courses']:
   self.assertTrue(c['summary'] and c['practice'] and c['prepare'])
   self.assertTrue(all(r['url'].startswith('https://') for r in c['resources']))
   self.assertEqual(c['status']=='planned',c['release']=='2027-01')
 def test_study_room_is_available_without_invented_content(self):
  html=(ROOT/'docs/index.html').read_text()
  self.assertIn('id="study-next"',html)
  self.assertIn('id="study-progress"',html)
  self.assertEqual(html.count('data-workspace'),13)
  self.assertEqual(html.count('data-step-key="watch"'),8)
  self.assertIn('공식 커리큘럼이나 수료 기준이 아닙니다',html)
  self.assertNotIn('<iframe',html) # third-party player must be opt-in
  self.assertIn('data-play=',html)
 def test_eight_official_playlists_and_no_upcoming_embeds(self):
  expected={'10-605':'PLOz411Ejgqdw','15-110':'PLB27aM0tkAQs','17-214':'PLBDTyW_Uan_k','15-442':'PLSH_5v_OOfP8','17-635':'PLBXWgYnejeLU','17-643':'PLBAcFaUDLxMA','11-768':'PLf0BEPn2BGr0','17-645':'PLDOc_XHH9ABE'}
  self.assertEqual({c['id']:c['playlist'] for c in self.data['courses'] if 'playlist' in c},expected)
  html=(ROOT/'docs/index.html').read_text()
  self.assertEqual(set(re.findall(r'data-play="([^"]+)"',html)),set(expected.values()))
  self.assertIn('frame-src https://www.youtube-nocookie.com',html)
  self.assertNotIn('src="https://www.youtube-nocookie.com',html)
