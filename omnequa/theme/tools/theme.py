"""One accessible brand shell for every current and archived Omnequa page."""
from html import escape
import json
BASE='https://omnequa.org'
BLOG='https://github.com/scottonchain/microcredit-vision'
RAW='https://raw.githubusercontent.com/scottonchain/microcredit-vision/main'
NAV=[('journal','Journal'),('about','About'),('how-we-work','Our work'),('history','History'),('newsroom','For the press')]
LOGO='<img class="brand-logo" src="/brand/omnequa-logo.png" width="48" height="48" alt="">'
def brand():
    return '<a class="brand" href="/" aria-label="Omnequa home">'+LOGO+'<span>Omnequa</span></a>'
def header(slug):
    nav=''.join('<a href="/'+s+'/"'+(' aria-current="page"' if slug==s or (s=='journal' and slug.startswith('journal/')) else '')+'>'+t+'</a>' for s,t in NAV)
    return '<a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="header-inner">'+brand()+'<nav aria-label="Main navigation">'+nav+'</nav><a class="header-contact" href="/contact/">Get in touch <span aria-hidden="true">↗</span></a></div></header>'
def footer():
    return '<footer class="site-footer"><div class="wrap footer-grid"><div>'+brand()+'<p>New technology.<br>Opportunity that reaches people.</p></div><div class="footer-links"><a href="/try/">Try our app</a><a href="/about/">Meet the team</a><a href="/how-we-work/">Our work</a><a href="/history/">Our history</a><a href="/newsroom/">Press & creators</a><a href="/journal/">Read the journal</a><a href="'+BLOG+'">GitHub journal ↗</a><a href="'+RAW+'/feed.xml">Subscribe via RSS ↗</a><a href="/privacy/">Privacy</a></div><div><p class="eyebrow">Let’s compare notes</p><a href="/contact/">Contact the team →</a><p class="fine-print">Independent research.<br>AI-led work. Human direction.<br>© 2026 Omnequa</p></div></div></footer>'
def document(slug,title,desc,body,script=False,archive=False):
    canonical=BASE+('/' if slug=='home' else '/'+slug+'/')
    schema={'@context':'https://schema.org','@type':'WebPage','name':title+' | Omnequa','description':desc,'url':canonical,'isPartOf':{'@type':'WebSite','name':'Omnequa','url':BASE}}
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Omnequa</title><meta name="description" content="{escape(desc,quote=True)}"><link rel="canonical" href="{canonical}"><meta property="og:title" content="{escape(title,quote=True)} | Omnequa"><meta property="og:description" content="{escape(desc,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="website"><meta property="og:site_name" content="Omnequa"><meta property="og:image" content="{BASE}/brand/omnequa-logo.png"><meta property="og:image:alt" content="Omnequa logo: hands holding a teal geometric symbol"><meta name="twitter:card" content="summary"><meta name="theme-color" content="#103747"><link rel="icon" href="/brand/omnequa-logo.png" type="image/png"><link rel="apple-touch-icon" href="/brand/omnequa-logo.png"><link rel="alternate" type="application/atom+xml" title="Omnequa journal" href="{RAW}/feed.xml"><link rel="stylesheet" href="/style.css"><script type="application/ld+json">{json.dumps(schema).replace('<','<ESC>')}</script>{('<script src="/journal.js" defer></script>' if script else '')}</head><body{' class="archive-page"' if archive else ''}>{header(slug)}<main id="main">{body}</main>{footer()}</body></html>'''
