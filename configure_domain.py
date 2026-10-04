from pathlib import Path
import sys,re,html
from urllib.parse import urlparse
from xml.etree.ElementTree import Element,SubElement,tostring
root=Path(__file__).resolve().parent
if len(sys.argv)!=2:raise SystemExit('Usage: python configure_domain.py https://your-real-site.example/path/')
base=sys.argv[1].rstrip('/')+'/'
p=urlparse(base)
if p.scheme!='https' or not p.netloc or 'example' in p.netloc:raise SystemExit('Enter your real HTTPS website URL.')
ns='http://www.sitemaps.org/schemas/sitemap/0.9';urlset=Element('urlset',xmlns=ns)
for f in sorted(root.glob('*.html')):
 url=base+(f.name if f.name!='index.html' else '')
 text=f.read_text();text=re.sub(r'<link[^>]+rel="canonical"[^>]*>','',text);text=re.sub(r'<meta[^>]+property="og:url"[^>]*>','',text)
 tags='<link rel="canonical" href="'+html.escape(url,quote=True)+'"><meta property="og:url" content="'+html.escape(url,quote=True)+'">'
 text=text.replace('</head>',tags+'</head>');f.write_text(text)
 entry=SubElement(urlset,'url');SubElement(entry,'loc').text=url
(root/'sitemap.xml').write_bytes(tostring(urlset,encoding='utf-8',xml_declaration=True))
(root/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+base+'sitemap.xml\n')
print('Canonical URLs and sitemap configured for',base)
