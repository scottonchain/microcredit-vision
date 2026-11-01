#!/usr/bin/env python3
"""Verify current pages, preserved routes, canonical metadata and journal feed."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.h1=0;self.lang=None;self.title=False;self.canonical=False
 def handle_starttag(self,t,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.append(d['id'])
  if t=='a' and 'href' in d:self.links.append(d['href'])
  if t=='h1':self.h1+=1
  if t=='html':self.lang=d.get('lang')
  if t=='title':self.title=True
  if t=='link' and d.get('rel')=='canonical':self.canonical=d.get('href','').startswith('https://omnequa.org/')
errors=[];pages={}
for p in OUT.rglob('*.html'):
 if p.name.startswith('qa-'):continue
 obj=Page();obj.feed(p.read_text());pages[p]=obj
 if obj.h1!=1 or obj.lang!='en' or not obj.title or not obj.canonical:errors.append(f'{p}: metadata/headings')
 if len(obj.ids)!=len(set(obj.ids)):errors.append(f'{p}: duplicate IDs')
for p,obj in pages.items():
 for href in obj.links:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  target=OUT/unquote(u.path).lstrip('/') if u.path else p
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{p.relative_to(OUT)}: missing {href}')
  elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{p.relative_to(OUT)}: missing anchor {href}')
for name in ['feed.xml','sitemap.xml']:ET.parse(OUT/name)
f=json.loads((OUT/'journal-feed.json').read_text());assert f['version']==1
assert len({p['id'] for p in f['posts']})==len(f['posts'])
assert len({p['slug'] for p in f['posts']})==len(f['posts'])
assert (ROOT/'assets/journal.js').read_text()==(OUT/'journal.js').read_text()
assert 'Legal, compliance and impact discovery with nonprofit sponsors and prospective partners concluded in fall 2026.' in (OUT/'history/index.html').read_text()
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages, links and anchors, metadata, feeds, unique posts, neutral history.')
