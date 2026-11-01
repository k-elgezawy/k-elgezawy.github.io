"""Focused publishing checks: content coverage, public assets, links, and safe output."""
import json,re,sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse,unquote
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'docs'
articles=json.loads((ROOT/'content/articles.json').read_text(encoding='utf-8'))
errors=[]
if len(articles)<32:errors.append(f'Expected at least 32 migrated articles, found {len(articles)}')
if len({a['slug'] for a in articles})!=len(articles):errors.append('Duplicate article slug')
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for k in ('href','src'):
            if k in a:self.links.append(a[k])
for f in OUT.rglob('*.html'):
    text=f.read_text(encoding='utf-8');p=Links();p.feed(text)
    if len(p.ids)!=len(set(p.ids)):errors.append(f'Duplicate IDs in {f.relative_to(OUT)}')
    for u in p.links:
        parsed=urlparse(u)
        if parsed.scheme:
            if parsed.scheme not in ('https','http','mailto','tel'):errors.append(f'Unsafe link scheme: {u}')
            if re.match(r'^(localhost|127\.|10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)',parsed.hostname or ''):errors.append(f'Internal URL: {u}')
            continue
        if not parsed.path:continue
        dest=(OUT/parsed.path.lstrip('/')) if parsed.path.startswith('/') else f.parent/unquote(parsed.path)
        if dest.is_dir():dest=dest/'index.html'
        if not dest.exists():errors.append(f'Broken local asset/link: {f.relative_to(OUT)} -> {u}')
    if 'SOURCE_URL' in text or 'Tell your story' in text:errors.append(f'Editor placeholder in {f}')
for a in articles:
    page=OUT/'articles'/a['slug']/'index.html'
    if not page.exists():errors.append(f'Missing article: {a["slug"]}');continue
    text=page.read_text(encoding='utf-8')
    for expected in ('id="english"','id="arabic"','lang="ar"','dir="rtl"',a['canonical']):
        if expected not in text:errors.append(f'Missing {expected} in {a["slug"]}')
    for lang in ('ar','en'):
        if len((ROOT/'content/articles'/f'{a["slug"]}.{lang}.md').read_text(encoding='utf-8').split())<70:errors.append(f'Incomplete translation: {a["slug"]} {lang}')
    en=(ROOT/'content/articles'/f'{a["slug"]}.en.md').read_text(encoding='utf-8')
    ar=(ROOT/'content/articles'/f'{a["slug"]}.ar.md').read_text(encoding='utf-8')
    if len(re.findall(r'^```\w',en,re.M)) != len(re.findall(r'^```\w',ar,re.M)):
        errors.append(f'Code examples missing from translation: {a["slug"]}')
if errors:
    print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(articles)} complete bilingual articles, {len(list(OUT.rglob("*.html")))} HTML pages; local links, assets, IDs, source links and public URL checks passed.')
