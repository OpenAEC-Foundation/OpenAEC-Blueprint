#!/usr/bin/env python3
"""Show the two remaining Pointcloud annotation icons beside Rust candidates."""
import hashlib
import json
from html import escape
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'harmonization/pointcloud-annotation-icon-review.json').read_text())
cards = []
for item in data['items']:
    source = root / item['source']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == item['source_sha256']
    for key in ('candidate_24', 'candidate_16'):
        assert (root / item[key]).is_file()
    name = escape(item['command'])
    source_url = '../' + item['source']
    large_url = '../' + item['candidate_24']
    small_url = '../' + item['candidate_16']
    cards.append(f'''<article><h2>{name.title()}</h2><p><code>{escape(item['source_use'])}</code> roept deze bronvorm aan.</p><div class="samples">
      <div><b>Pointcloud-bron · 24 px</b><div class="swatch"><img src="{source_url}" width="24" height="24" alt="{name} bron"></div></div>
      <div><b>Rust · 16 px</b><div class="swatch"><img class="candidate" src="{small_url}" width="16" height="16" alt="{name} 16 px"></div></div>
      <div><b>Rust · 24 px</b><div class="swatch"><img class="candidate" src="{large_url}" width="24" height="24" alt="{name} 24 px"></div></div>
      <div><b>Rust · 32 px</b><div class="swatch"><img class="candidate" src="{large_url}" width="32" height="32" alt="{name} 32 px"></div></div>
    </div><p class="decision">{ 'De T-vorm en twee tekstregels blijven op 16 px herkenbaar; de bronkleuren zijn vervangen door één thematisch getinte lijnkleur.' if item['command']=='text' else 'De pijl, knik en tekstregels blijven ook op 16 px van een gewone maatlijn te onderscheiden; één tint werkt op beide thema’s.'}</p></article>''')

page = '''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pointcloud annotatie-iconen · review</title><style>
*{box-sizing:border-box}body{margin:0;background:#f1f1f2;color:#303039;font:14px/1.5 system-ui,sans-serif}header{background:#303039;color:#fafaf9;border-bottom:3px solid #d97706;padding:24px max(24px,calc((100vw - 1100px)/2))}header a{color:#ffc47e}h1{margin:9px 0 4px;font-size:27px}header p{margin:0;color:#d4d4d8;max-width:1000px}main{max-width:1160px;margin:auto;padding:24px}article{background:white;border:1px solid #d5d5da;padding:18px 20px;margin-bottom:16px}h2{font-size:19px;margin:0 0 3px}.samples{display:grid;grid-template-columns:repeat(4,minmax(150px,1fr));gap:12px;margin-top:15px}.samples>div{min-width:0}.samples b{font-size:12px}.swatch{height:76px;border:1px solid #d3d3d7;background:#fafaf9;display:grid;place-items:center}.dark .swatch{background:#36363e;border-color:#5f5f68}.dark .candidate{filter:invert(1)}.dark .swatch img:not(.candidate){filter:brightness(0) invert(1)}.decision{font-size:13px;margin-bottom:0;color:#57534e}.theme{display:flex;gap:8px;margin:0 0 16px}.theme button{border:1px solid #b8b8bf;background:white;padding:7px 12px;cursor:pointer}.theme button.active{background:#d97706;color:#fff;border-color:#d97706}code{font-size:12px}footer{color:#65656e;font-size:12px;margin-bottom:24px}@media(max-width:700px){.samples{grid-template-columns:repeat(2,minmax(130px,1fr))}main{padding:12px}}
</style><header><a href="review.html">← Ontwerpreview</a><h1>Pointcloud · Tekst en Leidlijn</h1><p>De twee annotatieknoppen die nog lokale OpenCAD-SVG’s gebruikten. Hun nieuwe Rust-domeinvormen staan hier op 16, 24 en 32 px; de bronvormen zijn uit de daadwerkelijk aangeroepen UI-bestanden verzameld.</p></header><main><div class="theme"><button type="button" class="active" data-theme="light">Licht</button><button type="button" data-theme="dark">Donker</button></div>''' + ''.join(cards) + '''<h2>Native Rust-render</h2><p>Dezelfde bron- en crate-SVG’s, getekend met de software-renderer van de Style Repo:</p><img src="pointcloud-annotation-icons-light.png" alt="Tekst en Leidlijn in de native Rust-render, licht" style="display:block;max-width:100%;height:auto;margin:8px 0;border:1px solid #ccc"><img src="pointcloud-annotation-icons-forge.png" alt="Tekst en Leidlijn in de native Rust-render, Forge" style="display:block;max-width:100%;height:auto;margin:8px 0;border:1px solid #555"><footer>Broncommit ''' + escape(data['source_commit']) + ''' · 24px-bronvormen en afzonderlijke 16px-Rust-geometrie. Dit blad beoordeelt iconen, niet de volledige Pointcloud-ribbon.</footer></main><script>document.querySelectorAll('[data-theme]').forEach(button=>button.onclick=()=>{document.querySelector('main').classList.toggle('dark',button.dataset.theme==='dark');document.querySelectorAll('[data-theme]').forEach(x=>x.classList.toggle('active',x===button));});</script></html>'''
(root / 'design/pointcloud-annotation-icon-review.html').write_text(page)
print('Reviewed Pointcloud text and leader source icons against 16/24/32 px Rust artwork')
