/* One journal: GitHub is the editorial source; this site is its readable view. */
(() => {
  'use strict';
  const SOURCE='https://raw.githubusercontent.com/scottonchain/microcredit-vision/main/omnequa/feed.json';
  const REPO='https://github.com/scottonchain/microcredit-vision';
  const list=document.querySelector('[data-journal-list]');
  const reader=document.getElementById('journal-article');
  const search=document.getElementById('journal-search');
  const more=document.getElementById('load-more');
  let imageMirrors={}, pendingPublication=new Set(), remoteSlugs=new Set(), savedPending=[], posts=[], count=list ? Number(list.dataset.limit) : 18;
  const node=(tag,text,cls)=>{const el=document.createElement(tag);if(text)el.textContent=text;if(cls)el.className=cls;return el;};
  function safeURL(raw,image=false){
    if(typeof raw!=='string'||!raw.trim())return null;
    try {const u=new URL(raw,REPO+'/blob/main/posts/');
      if(u.username||u.password)return null;
      if(image)return u.protocol==='https:'&&u.hostname==='raw.githubusercontent.com'&&u.pathname.startsWith('/scottonchain/microcredit-vision/')?u.href:null;
      return (u.protocol==='https:'||u.protocol==='mailto:')?u.href:null;
    }catch{return null;}
  }
  function cleanHTML(html){
    const template=document.createElement('template');template.innerHTML=String(html);
    const allowed=new Set(['P','H1','H2','H3','H4','UL','OL','LI','STRONG','EM','B','I','A','IMG','FIGURE','FIGCAPTION','TABLE','THEAD','TBODY','TR','TH','TD','BLOCKQUOTE','PRE','CODE','BR','HR','SUP','SUB','DEL','DETAILS','SUMMARY']);
    const fragment=document.createDocumentFragment();
    function copy(source,target){
      for(const child of source.childNodes){
        if(child.nodeType===Node.TEXT_NODE){target.append(document.createTextNode(child.textContent));continue;}
        if(child.nodeType!==Node.ELEMENT_NODE||!allowed.has(child.tagName))continue;
        const el=document.createElement(child.tagName==='H1'?'h2':child.tagName.toLowerCase());
        if(child.tagName==='A'){
          const href=safeURL(child.getAttribute('href'));if(href){el.href=href;el.rel='noopener noreferrer';}
        }
        if(child.tagName==='IMG'){
          const src=safeURL(child.getAttribute('src'),true);if(!src)continue;
          el.src=src;el.alt=child.getAttribute('alt')||'';el.loading='lazy';el.decoding='async';
          const mirror=imageMirrors[src];
          if(typeof mirror==='string'&&mirror.startsWith('/journal-assets/')){
            const fallback=new URL(mirror,location.origin);
            if(fallback.origin===location.origin&&fallback.pathname.startsWith('/journal-assets/')){
              el.addEventListener('error',()=>{el.src=fallback.href;},{once:true});
            }
          }
        }
        if(['TH','TD'].includes(child.tagName))for(const a of ['colspan','rowspan']){const n=Number(child.getAttribute(a));if(n>0&&n<=20)el.setAttribute(a,String(n));}
        copy(child,el);target.append(el);
      }
    }
    copy(template.content,fragment);return fragment;
  }
  function normalize(data){
    if(data.version!==1||!Array.isArray(data.posts))throw new Error('Invalid journal feed');
    const ids=new Set();
    return data.posts.slice(0,1000).filter(p=>{
      if(!p||typeof p.id!=='string'||!/^[-a-z0-9]+$/.test(p.slug)||typeof p.title!=='string'||typeof p.summary!=='string'||!safeURL(p.url)||!p.url.startsWith(REPO+'/blob/main/posts/')||ids.has(p.id))return false;
      ids.add(p.id);return true;
    }).sort((a,b)=>String(b.date).localeCompare(String(a.date)));
  }
  function dateLabel(date){const d=new Date(date);return Number.isNaN(d.valueOf())?'Journal':d.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric',timeZone:'UTC'});}
  function articleLink(p){return p.content_html?'/journal/read/?slug='+encodeURIComponent(p.slug):p.url;}
  function renderList(){
    if(!list)return;
    const query=(search?.value||'').trim().toLowerCase();
    const filtered=posts.filter(p=>[p.title,p.summary,p.author,...(p.tags||[])].join(' ').toLowerCase().includes(query));
    const items=document.createDocumentFragment();
    for(const p of filtered.slice(0,count)){
      const card=node('article',null,'post-card');
      card.append(node('p',dateLabel(p.date)+' · '+(p.tags?.[0]||'Journal').replaceAll('-',' '),'eyebrow'));
      const heading=node('h3');const anchor=node('a',p.title);anchor.href=articleLink(p);heading.append(anchor);card.append(heading,node('p',p.summary),node('span','Read the story →','read-more'));items.append(card);
    }
    if(!filtered.length)items.append(node('p','No stories match that search. Try a broader topic.'));
    list.replaceChildren(items);if(more)more.hidden=filtered.length<=count;
  }
  function renderArticle(){
    if(!reader)return;
    const slug=new URLSearchParams(location.search).get('slug');const p=posts.find(p=>p.slug===slug);
    if(!p){reader.replaceChildren(node('p','The Omnequa journal','eyebrow'),node('h1','Find your next idea.'),node('p','This story is not in the available journal edition.'));const a=node('a','Browse all stories →');a.href='/journal/';reader.append(a);return;}
    document.title=p.title+' | Omnequa';
    document.querySelector('meta[name="description"]')?.setAttribute('content',p.summary);
    document.querySelector('meta[property="og:title"]')?.setAttribute('content',p.title+' | Omnequa');
    document.querySelector('meta[property="og:description"]')?.setAttribute('content',p.summary);
    const canonical='https://omnequa.org/journal/read/?slug='+encodeURIComponent(p.slug);
    document.querySelector('link[rel="canonical"]')?.setAttribute('href',canonical);
    document.querySelector('meta[property="og:url"]')?.setAttribute('content',canonical);
    reader.replaceChildren(node('p','The Omnequa journal','eyebrow'),node('h1',p.title),node('p',p.summary,'lede'),node('p',dateLabel(p.date)+' · '+(p.author||'The Omnequa AI team'),'byline'));
    const back=node('p',null,'article-back');const backLink=node('a','← All stories');backLink.href='/journal/';back.append(backLink);reader.prepend(back);
    if(p.content_html){const body=node('div',null,'article-body');body.append(cleanHTML(p.content_html));reader.append(body);}else reader.append(node('p','This article is available in full on our GitHub journal.'));
    if(!pendingPublication.has(p.slug)||remoteSlugs.has(p.slug)){const source=node('p',null,'source-link');const a=node('a','Read the same story on GitHub ↗');a.href=p.url;source.append(a);reader.append(source);}
  }
  async function fetchJSON(url){const response=await fetch(url,{signal:AbortSignal.timeout(7000),credentials:'omit'});if(!response.ok)throw new Error('Journal unavailable');return response.json();}
  async function start(){
    // Render the bundled edition immediately; refresh from the canonical feed.
    try{const saved=await fetchJSON('/journal-feed.json');imageMirrors=saved.image_mirrors||{};pendingPublication=new Set(saved.pending_publication_slugs||[]);posts=normalize(saved);savedPending=posts.filter(p=>pendingPublication.has(p.slug));renderList();renderArticle();}catch{}
    try{const data=await fetchJSON(SOURCE);const canonical=normalize(data);remoteSlugs=new Set(canonical.map(p=>p.slug));posts=normalize({version:1,posts:[...canonical,...savedPending.filter(p=>!remoteSlugs.has(p.slug))]});renderList();renderArticle();const status=document.querySelector('[data-feed-status]');if(status)status.textContent='Articles from the Omnequa journal.';}
    catch{const status=document.querySelector('[data-feed-status]');if(status)status.textContent='Showing the saved edition.';}
  }
  search?.addEventListener('input',()=>{count=18;renderList();});more?.addEventListener('click',()=>{count+=18;renderList();});start();
})();
