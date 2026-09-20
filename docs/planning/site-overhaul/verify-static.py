from pathlib import Path
from html.parser import HTMLParser
import json, re, xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[3]
class Page(HTMLParser):
  def __init__(self): super().__init__(); self.tags=[]; self.text=[]
  def handle_starttag(self,t,a): self.tags.append((t,dict(a)))
  def handle_data(self,d): self.text.append(d)
results=[]
for f in sorted((root/'_site').rglob('*.html')):
  p=Page(); p.feed(f.read_text()); tags=p.tags
  assert sum(t=='h1' for t,a in tags)==1,f
  assert sum(t=='main' for t,a in tags)==1,f
  ids=[a['id'] for t,a in tags if 'id' in a]; assert len(ids)==len(set(ids)),f
  assert any(t=='meta' and a.get('name')=='description' and a.get('content') for t,a in tags),f
  canonical=[a['href'] for t,a in tags if t=='link' and a.get('rel')=='canonical']; assert len(canonical)==1 and canonical[0].startswith('https://swiftlabs.xyz/'),f
  links=[]
  for t,a in tags:
    url=a.get('href') or a.get('src')
    if not url: continue
    links.append(url)
    if url.startswith('#'): assert url[1:] in ids,(f,url)
    elif url.startswith('/'):
      target=root/'_site'/url.lstrip('/')
      if url.endswith('/'): target=target/'index.html'
      assert target.exists(),(f,url)
    else: assert url.startswith(('mailto:jane@swiftlabs.xyz','https://swiftlabs.xyz/')),(f,url)
  assert not any(t in ('iframe','form') for t,a in tags),f
  forbidden=r'\b(Eleventy|Nunjucks|SQLite|Electron|Node\.js|Tailscale|Next\.js|React|Ubuntu|Linux|Vercel|Netlify)\b'
  assert not re.search(forbidden,' '.join(p.text),re.I),f
  results.append({'page':str(f.relative_to(root/'_site')),'headings':sum(t in ('h1','h2','h3') for t,a in tags),'links':len(links),'canonical':canonical[0],'result':'pass'})
html=(root/'_site/index.html').read_text(); obj=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)[1]); assert obj['name']=='Jane Swift'
manifest=json.loads((root/'_site/site.webmanifest').read_text()); assert manifest['theme_color']=='#f5f2e9'
sitemap=ET.parse(root/'_site/sitemap.xml'); urls=[x.text for x in sitemap.findall('.//{*}loc')]; assert set(urls)=={'https://swiftlabs.xyz'+p for p in ['/','/about/','/work/','/contact/']},urls
assert (root/'src/CNAME').read_text().strip()=='swiftlabs.xyz'
def lum(h):
  rgb=[int(h[i:i+2],16)/255 for i in (1,3,5)]
  return sum(c*w for c,w in zip([c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4 for c in rgb],[.2126,.7152,.0722]))
pairs=[('#252d28','#f5f2e9'),('#566058','#f5f2e9'),('#234c3b','#f5f2e9'),('#8d412c','#f5f2e9'),('#f5f2e9','#234c3b'),('#d9e1cf','#234c3b'),('#e0e5d9','#234c3b'),('#566058','#e7eadd'),('#8d412c','#e7eadd'),('#f2cdac','#234c3b')]
contrast=[]
for fg,bg in pairs:
  a,b=sorted([lum(fg),lum(bg)]); ratio=(b+.05)/(a+.05); assert ratio>=4.5,(fg,bg,ratio)
  contrast.append({'foreground':fg,'background':bg,'ratio':round(ratio,2)})
report={'pages':results,'sitemap':urls,'structured_data':'valid Person JSON','contrast':contrast,'scope':'Static build inspection; not browser or assistive-technology execution.'}
(root/'docs/planning/site-overhaul/static-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
