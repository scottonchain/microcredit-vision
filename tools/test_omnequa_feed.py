import unittest
from omnequa_feed import markdown, absolute
class FeedTests(unittest.TestCase):
 def test_images_and_sources(self):
  h=markdown('## A chart\n\n![Chart](../images/chart.svg)\n\n[Source](https://example.org/data)')
  self.assertIn('src="https://raw.githubusercontent.com/scottonchain/microcredit-vision/main/images/chart.svg"',h)
  self.assertIn('<h2>A chart</h2>',h)
  self.assertIn('href="https://example.org/data"',h)
 def test_inert_markup(self):
  h=markdown('<script>alert(1)</script>\n\n[bad](javascript:alert)\n\n![bad](data:payload)')
  self.assertNotIn('<script>',h);self.assertNotIn('href="javascript',h);self.assertNotIn('src="data:',h)
 def test_table(self):
  h=markdown('| Name | Value |\n|---|---|\n| Loan | 1 |')
  self.assertIn('<th>Name</th>',h);self.assertIn('<td>1</td>',h)
 def test_code(self):
  self.assertIn('&lt;script&gt;',markdown('```\n<script>\n```'))
if __name__=='__main__':unittest.main()
