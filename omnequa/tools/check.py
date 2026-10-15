#!/usr/bin/env python3
"""Check built pages, routes, metadata and public launch data."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
errors=[]
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.hrefs=[]; self.ids=set(); self.titles=0; self.h1=0; self.desc=False; self.canon=False; self.lang=False
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if t=='html': self.lang=a.get('lang')=='en'
        if t=='title': self.titles+=1
        if t=='h1': self.h1+=1
        if t=='meta' and a.get('name')=='description': self.desc=bool(a.get('content'))
        if t=='link' and a.get('rel')=='canonical': self.canon=bool(a.get('href'))
        if t=='a' and 'href' in a:self.hrefs.append(a['href'])
        if 'id' in a:self.ids.add(a['id'])
for path in DIST.rglob('*.html'):
    text=path.read_text(); p=Page();p.feed(text)
    if not (p.lang and p.titles==1 and p.h1==1 and p.desc and p.canon):errors.append(f'{path}: missing unique h1/title or metadata')
    for href in p.hrefs:
        u=urlsplit(href)
        if u.scheme or u.netloc:continue
        if u.path:
            target=DIST/unquote(u.path).lstrip('/')
            if u.path.endswith('/'):target=target/'index.html'
            if not target.exists():errors.append(f'{path}: missing {href}')
            elif u.fragment and target.suffix=='.html':
                destination=Page();destination.feed(target.read_text())
                if unquote(u.fragment) not in destination.ids:errors.append(f'{path}: missing cross-page anchor {href}')
        elif u.fragment and u.fragment not in p.ids:errors.append(f'{path}: missing anchor {href}')
for xml in ['sitemap.xml','feed.xml']:ET.parse(DIST/xml)
brief=(DIST/'partners/index.html').read_text()
if '<form' in brief or 'type="submit"' in brief:errors.append('Employer brief must not silently submit via native form navigation')
for name in ['employer','source','task','eligibility','pay','payout','barrier']:
    if f'for="{name}"' not in brief or f'id="{name}"' not in brief:errors.append(f'Employer brief missing associated label: {name}')
if 'id="prepare-draft" class="button" type="button" disabled' not in brief:errors.append('Draft action must be disabled until JavaScript attaches its handler')
data=json.loads((ROOT/'content/site.json').read_text())
for post in data['posts']:
    n=len(post['paragraphs'])
    if not 5<=n<=20:errors.append(f'{post["slug"]}: expected 5–20 sentences, got {n} paragraphs')
    if not post['sources']:errors.append(f'{post["slug"]}: missing evidence')
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(list(DIST.rglob("*.html")))} HTML files, routes, metadata, XML and launch content.')
