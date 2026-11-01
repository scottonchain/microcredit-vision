"""Generate Omnequa's shared journal from validated blog posts. Standard library only.
Integration in tools/build.py: import omnequa_feed, then add
'omnequa/feed.json': omnequa_feed.render(posts) to prepare()'s output dictionary.
The normal build and CI --check therefore cover the website feed, too.
"""
import html, json, re, posixpath
from urllib.parse import urljoin, urlsplit
REPO='https://github.com/scottonchain/microcredit-vision'
RAW='https://raw.githubusercontent.com/scottonchain/microcredit-vision/main/'

def absolute(url, image=False):
    url=html.unescape(url).strip()
    if url.startswith('#'): return url
    if urlsplit(url).scheme:
        return url if urlsplit(url).scheme in ('https','mailto') else ''
    if image:
        return RAW+posixpath.normpath(posixpath.join('posts',url)).lstrip('/')
    return urljoin(REPO+'/blob/main/posts/',url)

def inline(s):
    # Escape raw HTML; only our generated, allowlisted markup reaches the feed.
    tokens=[]
    def hold(markup):
        tokens.append(markup);return '\x00'+str(len(tokens)-1)+'\x00'
    def link(m):
        image=bool(m[1]);url=absolute(m[3],image)
        label=html.escape(m[2])
        if not url:return label
        return hold('<img src="'+html.escape(url,quote=True)+'" alt="'+label+'">' if image else '<a href="'+html.escape(url,quote=True)+'">'+label+'</a>')
    s=re.sub(r'(!?)\[([^\]]+)\]\(([^\s)]+)(?:\s+"[^"]*")?\)',link,s)
    s=re.sub(r'`([^`]+)`',lambda m:hold('<code>'+html.escape(m[1])+'</code>'),s)
    s=html.escape(s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)',r'<em>\1</em>',s)
    return re.sub(r'\x00(\d+)\x00',lambda m:tokens[int(m[1])],s)

def markdown(body):
    body=re.sub(r'<!--.*?-->','',body,flags=re.S)
    lines=body.splitlines();result=[];para=[];i=0
    def flush():
        if para: result.append('<p>'+inline(' '.join(para))+'</p>');para.clear()
    while i<len(lines):
        line=lines[i].strip()
        if not line:flush();i+=1;continue
        if line.startswith('```'):
            flush();i+=1;code=[]
            while i<len(lines) and not lines[i].strip().startswith('```'):code.append(lines[i]);i+=1
            result.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>');i+=1;continue
        if re.match(r'^#{1,6} ',line):
            flush();level=min(4,max(2,len(line)-len(line.lstrip('#'))));result.append(f'<h{level}>'+inline(line.lstrip('# ').strip())+f'</h{level}>');i+=1;continue
        if i+1<len(lines) and '|' in line and re.match(r'^\|?\s*:?-{3,}',lines[i+1].strip()):
            flush();cells=lambda s:[x.strip() for x in s.strip().strip('|').split('|')]
            rows=['<thead><tr>'+''.join('<th>'+inline(x)+'</th>' for x in cells(line))+'</tr></thead><tbody>'];i+=2
            while i<len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append('<tr>'+''.join('<td>'+inline(x)+'</td>' for x in cells(lines[i]))+'</tr>');i+=1
            result.append('<table>'+''.join(rows)+'</tbody></table>');continue
        if re.match(r'^([-*]|\d+\.)\s+',line):
            flush();ordered=bool(re.match(r'^\d+\.',line));tag='ol' if ordered else 'ul';items=[]
            pattern=r'^\d+\.\s+' if ordered else r'^[-*]\s+'
            while i<len(lines) and re.match(pattern,lines[i].strip()):
                items.append('<li>'+inline(re.sub(pattern,'',lines[i].strip()))+'</li>');i+=1
            result.append('<'+tag+'>'+''.join(items)+'</'+tag+'>');continue
        if line.startswith('>'):
            flush();q=[]
            while i<len(lines) and lines[i].strip().startswith('>'):q.append(lines[i].strip().lstrip('> ').strip());i+=1
            result.append('<blockquote><p>'+inline(' '.join(q))+'</p></blockquote>');continue
        if re.fullmatch(r'[-*_]{3,}',line):flush();result.append('<hr>');i+=1;continue
        para.append(line);i+=1
    flush();return '\n'.join(result)

def render(posts):
    entries=[]
    for p in posts:
        url=REPO+'/blob/main/posts/'+p['slug']+'.md'
        entries.append(dict(id=p.get('source_id',url),slug=p['slug'],title=p['title'],date=p['dt'].isoformat().replace('+00:00','Z'),author=p['author'],summary=p['summary'],tags=p['tag_list'],url=url,image=RAW+p['image'],content_html=markdown(p['body'])))
    return json.dumps(dict(version=1,updated=max(p['updated_dt'] for p in posts).isoformat().replace('+00:00','Z'),posts=entries),ensure_ascii=False,indent=2)+'\n'
