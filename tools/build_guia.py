#!/usr/bin/env python3
"""Build plantillas-3d/GUIA.pdf from tools/guia-3d.md (with template previews). Run: python3 tools/build_guia.py"""
import markdown, base64, io, pathlib
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent; T=ROOT/'plantillas-3d'
MAPS={'### 1.':'01-banner_2560x1440.png','### 2.':'02-muro_2560x300.png','### 3.':'03-textura-fondo_1024x1024.png','### 4.':'04-antorcha_200x320.png',
      '### 5.':'05-pasto_2560x200.png','### 6.':'06-marco_600x740.png','### 7.':'07-compartir_1200x630.png','### 8.':'08-niebla_1920x1080.png'}
def thumb(f):
    im=Image.open(T/f); bg=Image.new('RGBA',im.size,(36,40,38,255)); bg.alpha_composite(im); bg=bg.convert('RGB')
    if bg.width>1400: bg=bg.resize((1400,round(1400*bg.height/bg.width)),Image.LANCZOS)
    b=io.BytesIO(); bg.save(b,'JPEG',quality=82); return base64.b64encode(b.getvalue()).decode()
out=[]
for ln in (ROOT/'tools/guia-3d.md').read_text(encoding='utf-8').split('\n'):
    out.append(ln)
    for k,f in MAPS.items():
        if ln.startswith(k):
            cls='tall' if f[:2] in ('03','04','06') else 'wide'
            out.append(f'\n<img class="tpl {cls}" src="data:image/jpeg;base64,{thumb(f)}" alt="">\n')
body=markdown.markdown('\n'.join(out),extensions=['tables']).replace('<li>[ ] ','<li class="chk">☐ ')
css='''@page{size:A4;margin:16mm 15mm}
body{font:10.5pt/1.5 "DejaVu Sans",Arial,sans-serif;color:#1d211f}
h1{font-size:22pt;margin:0 0 4mm;color:#2b2140;border-bottom:2px solid #6f8a68;padding-bottom:2mm}
h2{font-size:14pt;color:#5d4785;margin:7mm 0 2mm;break-after:avoid}
h3{font-size:12pt;color:#3e5a39;margin:6mm 0 1.5mm;break-after:avoid}
p,li{margin:0 0 1.2mm} ul,ol{padding-left:6mm;margin:0 0 2mm}
table{border-collapse:collapse;width:100%;font-size:9.5pt;margin:2mm 0}
td,th{border:1px solid #cfd3cf;padding:1.6mm 2mm;vertical-align:top;text-align:left} th{background:#eef0ec}
code{font-family:"DejaVu Sans Mono",monospace;font-size:8.6pt;background:#f0f1ee;padding:0 1mm;border-radius:1mm;word-break:break-all}
img.tpl{display:block;margin:2mm 0 3mm;border:1px solid #999;break-inside:avoid} img.wide{width:100%} img.tall{height:62mm}
li.chk{list-style:none;margin-left:-5mm} a{color:#5d4785}'''
html=f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>'
tmp=ROOT/'tools/.guia.html'; tmp.write_text(html,encoding='utf-8')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto(tmp.as_uri())
    pg.pdf(path=str(T/'GUIA.pdf'),format='A4',print_background=True,prefer_css_page_size=True); b.close()
tmp.unlink(); print('built',T/'GUIA.pdf')
