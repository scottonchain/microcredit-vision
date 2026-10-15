#!/usr/bin/env python3
"""Check built pages, routes, metadata and public launch data."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
errors=[]

def focus_contrast_errors(css):
    """Bounded source check for this site's current focus rules and surfaces.

    Not a CSS cascade engine, browser test or WCAG conformance certification.
    Checks the enumerated declarations, not computed styles or arbitrary CSS.
    """
    problems=[]
    # Reject extra focus/outline writers instead of ignoring a later override.
    if len(re.findall(r'(?:^|[;{])\s*--focus\s*:',css))!=2:
        problems.append('Focus token declaration count changed; review required')
    if len(re.findall(r'(?:^|[;{])\s*outline\s*:',css))!=2:
        problems.append('Focus outline declaration count changed; review required')
    if re.search(r'(?:^|[;{])\s*(?:outline-(?:color|style|width)|forced-color-adjust)\s*:',css):
        problems.append('Additional focus rendering override requires review')
    def declaration(selector, property_name):
        rule=re.search(re.escape(selector)+r'\{([^}]*)\}', css)
        if not rule:
            raise ValueError('missing focus/surface rule')
        match=re.search(r'(?:^|;)'+re.escape(property_name)+r':([^;]+)', rule[1])
        if not match:
            raise ValueError('missing focus/surface declaration')
        return match[1].strip()
    def color(value):
        if re.fullmatch(r'var\(--[a-z-]+\)', value):
            value=declaration(':root', value[4:-1])
        if not re.fullmatch(r'#[0-9a-fA-F]{6}', value):
            raise ValueError('unsupported focus/surface color')
        channels=[int(value[i:i+2],16)/255 for i in (1,3,5)]
        linear=[c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4 for c in channels]
        return sum(c*w for c,w in zip(linear,(0.2126,0.7152,0.0722)))
    def ratio(a,b):
        light,dark=sorted((color(a),color(b)),reverse=True)
        return (light+0.05)/(dark+0.05)
    try:
        for selector in ('a:focus-visible,button:focus-visible','input:focus,textarea:focus'):
            if declaration(selector,'outline')!='3px solid var(--focus)':
                problems.append('Custom focus outline must use the reviewed focus token')
        light_focus=declaration(':root','--focus')
        dark_focus=declaration('.cta,.intro-strip','--focus')
        for selector in ('body','.intake-form','.hero-note','.history-band'):
            if ratio(light_focus,declaration(selector,'background'))<3:
                problems.append('Light-surface focus contrast below 3:1: '+selector)
        for selector in ('.cta','.intro-strip'):
            if ratio(dark_focus,declaration(selector,'background'))<3:
                problems.append('Dark-surface focus contrast below 3:1: '+selector)
    except ValueError:
        problems.append('Focus contrast source contract changed; review required')
    return problems

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
def main():
    errors.clear()
    css=(ROOT/'assets/style.css').read_text()
    errors.extend(focus_contrast_errors(css))
    if css!=(DIST/'style.css').read_text():errors.append('Generated stylesheet differs from its source')
    check_pages()
    if errors:raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(list(DIST.rglob("*.html")))} HTML files, routes, metadata, XML, launch content and source focus contrast.')

def check_pages():
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
  if '<label for="plain-draft">' not in brief or 'id="plain-draft" readonly rows="14" aria-describedby="plain-draft-help"' not in brief:errors.append('Plain-text brief needs a labeled, readonly, described copy field')
  if 'id="plain-draft-panel" hidden' not in brief or 'Nothing has been sent.' not in brief:errors.append('Plain-text brief must start hidden and explain its no-send boundary')
  if (ROOT/'assets/intake.js').read_text()!=(DIST/'intake.js').read_text():errors.append('Generated intake script differs from its source')
  data=json.loads((ROOT/'content/site.json').read_text())
  leads=json.loads((ROOT/'content/opportunities.json').read_text())['leads']
  lead_ids=set()
  for lead in leads:
    if lead['id'] in lead_ids:errors.append('Duplicate application lead')
    lead_ids.add(lead['id'])
    if lead['status']!='application_lead_not_recommended':errors.append('Lead promotion requires explicit content and evidence review')
    if not lead['checked_on']<=data['updated']:errors.append('Application lead source check is future-dated')
    if not lead['checked_on']<=lead['review_due']:errors.append('Application lead review date precedes source check')
    for key in ['location','eligibility','advertised_pay','payment_unknowns','participation_unknowns','closing_date','next_action']:
        if not lead.get(key):errors.append(f'Application lead lacks {key}')
    for key in ['source','employer_index','employer_provenance','evidence']:
        if urlsplit(lead[key]).scheme!='https':errors.append('Application lead requires secure original/evidence links')
    if f'id="{lead["id"]}"' not in (DIST/'opportunities/index.html').read_text():errors.append('Application lead missing from generated page')
  for post in data['posts']:
    n=len(post['paragraphs'])
    if not 5<=n<=20:errors.append(f'{post["slug"]}: expected 5–20 sentences, got {n} paragraphs')
    if not post['sources']:errors.append(f'{post["slug"]}: missing evidence')

if __name__=='__main__':main()
