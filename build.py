"""Build the dependency-free Scribble storefront into dist/."""
from pathlib import Path
import json, shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
config = json.loads((ROOT / 'site.config.json').read_text())
shutil.copytree(ROOT / 'assets', OUT / 'assets', ignore=shutil.ignore_patterns('*.jpg'))
shutil.copytree(ROOT / 'docs', OUT / 'docs')

def page(path, kind, title, description, product=''):
    prefix = '../' if '/' in path else './'
    file = OUT / path
    file.parent.mkdir(parents=True, exist_ok=True)
    canonical = config['siteUrl'].rstrip('/') + '/' + ('' if path == 'index.html' else path)
    file.write_text(f'''<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Scribble</title><meta name="description" content="{description}">
<meta name="theme-color" content="#000000"><meta property="og:title" content="{title} — Scribble"><meta property="og:description" content="{description}"><meta property="og:type" content="website"><meta property="og:image" content="{config['siteUrl']}/assets/media/film-01.webp"><link rel="canonical" href="{canonical}">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{prefix}assets/style.css"><script src="{prefix}assets/data.js" defer></script><script src="{prefix}assets/app.js" defer></script>
</head><body id="top" data-root="{prefix}" data-page="{kind}" data-product="{product}"><div id="app"></div><noscript><main style="padding:100px 30px"><h1>Scribble / 001 — Streetwear</h1><p>Bu etkileşimli konsepti görmek için JavaScript’i etkinleştirin. / Enable JavaScript to view this interactive concept.</p><p>Görseller ilgili sahiplerine aittir. / Images belong to their respective owners.</p><a href="{prefix}docs/SOURCES.md">Kaynaklar / Sources ↗</a></main></noscript></body></html>''', encoding='utf-8')

page('index.html', 'home', 'Streetwear / 001', 'Scribble Streetwear. Sokaktan gelen bir ses. TR/EN konsept mağaza; tüm görsel kaynakları belirtilmiştir.')
page('shop.html', 'shop', 'Koleksiyon', 'Scribble 001: grafik tişörtler, alt giyim ve aksesuarlar. Portföy amaçlı konsept ürünler.')
page('films.html', 'films', 'Filmler', 'SNORES ve RUNT kaynaklı streetwear video referansları ve yapımcı kredileri.')
page('about.html', 'about', 'Hikâye', 'Tek marka, farklı dünyalar. Scribble’ın streetwear dünyası.')
page('references.html', 'references', 'Referanslar', 'Scribble Streetwear için tasarım, ürün, film ve sticker kaynakları. Orijinal markalar ve üretici kredileri.')
products = [('afterimage-tee','Afterimage Tişört'),('creations-tee','Creations Tişört'),('music-tee','Music Only Tişört'),('script-pants','Script Eşofman'),('washed-denim','Washed Script Denim'),('racing-cap','Racing Şapka'),('statement-cap','Statement Şapka')]
for slug,title in products:
    page(f'products/{slug}.html', 'product', title, f'{title} — Scribble Streetwear ürün tasarımı demosu. Fiyatlar örnektir, gerçek satış yapılmaz.', slug)
page('404.html', 'home', 'Scribble / 001', 'Scribble Streetwear konsept mağaza.')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+config['siteUrl']+'/sitemap.xml\n')
urls = ['index.html','shop.html','about.html','films.html','references.html'] + [f'products/{s}.html' for s,_ in products]
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+config['siteUrl']+'/'+('' if u=='index.html' else u)+'</loc></url>' for u in urls)+'</urlset>')
print(f'Built {len(urls)} pages and assets to {OUT}')
