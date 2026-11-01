#!/usr/bin/env python3
"""Prepare original website news as canonical blog posts; never duplicate a source.
Run from the vision repository with --site PATH/TO/WEBSITE/CHECKOUT.
Idempotency: source_id=original site dedup_id/guid, then slug/title matches.
Writes only missing posts, an illustration, and a manifest. Does not commit/build.
Review archive content before publication; original news remains dated history.
"""
import argparse, json, re
from pathlib import Path
from email.utils import parsedate_to_datetime
from html import escape
p=argparse.ArgumentParser();p.add_argument('--site',required=True);p.add_argument('--output',default='.');args=p.parse_args()
site=Path(args.site);out=Path(args.output);data=json.loads((site/'content/site.json').read_text())
postdir=out/'posts';postdir.mkdir(parents=True,exist_ok=True)
existing=[]
for path in postdir.glob('*.md'):
    text=path.read_text();title=re.search(r'^title:\s*(.+)$',text,re.M);source=re.search(r'^source_id:\s*(.+)$',text,re.M)
    existing.append((path.stem,title[1].strip().casefold() if title else '',source[1].strip() if source else '',text))
manifest=[]
for item in data['posts']:
    source_id=item.get('dedup_id') or item.get('guid') or 'https://omnequa.org/journal/'+item['slug']+'/'
    original='https://omnequa.org/journal/'+item['slug']+'/'
    matches=[x for x in existing if x[0] in (item['slug'],'omnequa-'+item['slug']) or x[1]==item['title'].casefold() or x[2]==source_id]
    # A prior blog companion naming this exact canonical URL may already mirror the news.
    candidates=[x[0] for x in existing if original in x[3]]
    record=dict(source_id=source_id,site_url=original,original_title=item['title'],related_existing_posts=candidates)
    if matches:record.update(status='already_present',post=matches[0][0]);manifest.append(record);continue
    slug='omnequa-'+item['slug'];date=parsedate_to_datetime(item['rss_date']).strftime('%Y-%m-%d %H:%M UTC')
    lines=['<!--','title: '+item['title'],'date: '+date,'author: Codex','image: images/omnequa-archive.svg','summary: '+item['summary'],'tags: direction','source: Original Omnequa website journal, '+original,'source_id: '+source_id,'-->','','*From the October 2026 Omnequa website archive. Dates, goals and invitations below describe that period.*','']
    lines.extend(x+'\n' for x in item['paragraphs'])
    lines+=['## Original sources','']
    for src in item['sources']:
        url='https://omnequa.org'+src['url'] if src['url'].startswith('/') else src['url']
        lines.append('- ['+src['label']+']('+url+')')
    if item.get('measurement'):
        lines+=['','## Dated report','',item['measurement']['window'],'','| Measure | Target | Result | Scope |','|---|---|---|---|']
        for row in item['measurement']['measures']:lines.append('| '+' | '.join(row[k].replace('|','/') for k in ['measure','target','result','boundary'])+' |')
    (postdir/(slug+'.md')).write_text('\n'.join(lines)+'\n');record.update(status='prepared',post=slug);manifest.append(record)
(out/'images').mkdir(exist_ok=True)
(out/'images/omnequa-archive.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#f7f5ed"/><circle cx="960" cy="290" r="170" fill="#dbe4c7"/><circle cx="890" cy="370" r="120" fill="#234f42"/><text x="90" y="150" font-family="sans-serif" font-size="24" fill="#234f42">OMNEQUA • WEBSITE JOURNAL</text><text x="90" y="315" font-family="Georgia,serif" font-size="76" fill="#183d37">The October archive</text><text x="90" y="465" font-family="sans-serif" font-size="27" fill="#56635c">Dated notes from the next chapter.</text></svg>')
(out/'news-import-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'prepared':sum(x['status']=='prepared' for x in manifest),'already_present':sum(x['status']=='already_present' for x in manifest)}))
