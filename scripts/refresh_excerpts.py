"""Refresh article teasers without cutting words or Markdown syntax."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parent.parent
path=root/'content/articles.json'
articles=json.loads(path.read_text(encoding='utf-8'))
for article in articles:
    for lang,key in [('en','excerptEn'),('ar','excerpt')]:
        text=(root/'content/articles'/f'{article["slug"]}.{lang}.md').read_text(encoding='utf-8').split('\n\n')[0]
        text=re.sub(r'[`*#]','',text).strip()
        if len(text)>180:
            text=text[:181].rsplit(' ',1)[0].rstrip('.,;:،؛')+'…'
        article[key]=text
path.write_text(json.dumps(articles,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
