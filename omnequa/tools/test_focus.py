"""Bounded color checks for light/dark focus surfaces, not a WCAG certification."""
from pathlib import Path
import re, unittest
CSS=(Path(__file__).resolve().parents[1]/'assets/style.css').read_text()
def luminance(value):
 rgb=[int(value[i:i+2],16)/255 for i in (1,3,5)]
 return sum((x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4)*w for x,w in zip(rgb,[.2126,.7152,.0722]))
def contrast(a,b):
 hi,lo=sorted([luminance(a),luminance(b)],reverse=True)
 return (hi+.05)/(lo+.05)
class FocusColors(unittest.TestCase):
 def test_light_surfaces(self):
  focus=re.search(r':root\{[^}]*--focus:(#[a-f0-9]{6})',CSS)[1]
  for surface in ['#f7f5ed','#eceee3','#ebeede','#e9eddb']:
   self.assertGreaterEqual(contrast(focus,surface),3)
 def test_dark_section_override(self):
  focus=re.search(r'\.mission-band\{--focus:(#[a-f0-9]{6})',CSS)[1]
  self.assertGreaterEqual(contrast(focus,'#183d37'),3)
 def test_focus_not_hidden(self):
  self.assertIn('outline:3px solid var(--focus)',CSS)
  self.assertNotRegex(CSS,r'outline\s*:\s*(none|0)')
if __name__=='__main__':unittest.main()
