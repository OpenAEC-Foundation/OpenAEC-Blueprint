#!/usr/bin/env python3
"""Build a source-evidenced visual workbench for verified UI-used icon assets."""
import html
import json
from collections import Counter
from pathlib import Path
from urllib.parse import quote, unquote

from build_icon_semantics import candidates

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'design'
assets = json.loads((ROOT / 'harmonization/asset-index.json').read_text())
repos = {r['name']: r for r in json.loads((ROOT / 'harmonization/inventory.json').read_text())}
adopted = {d['legacy_asset']: d['shared_icon'] for d in json.loads((DESIGN / 'icon-adoptions.json').read_text())['decisions']}
rows = []
for asset in assets:
    if asset['category'] != 'ui-used':
        continue
    repo, path = asset['repo'], asset['path']
    preview = unquote(asset['file'])
    assert (DESIGN / preview).is_file(), preview
    references = asset['ui_references']
    assert references, (repo, path)
    ref = references[0]
    commit = repos[repo].get('commit')
    source = (repos[repo]['url'].rstrip('/') + '/blob/' + commit + '/' + quote(ref['source']) +
              (f'#L{ref["line"]}' if ref.get('line') else '')) if commit else asset['url']
    semantics = candidates(Path(path).stem)
    rows.append({
        'repo': repo, 'path': path, 'preview': preview, 'source': source,
        'evidence': asset['evidence_type'], 'references': len(references),
        'candidate': semantics[0] if len(semantics) == 1 else '',
        'adopted': adopted.get(path, '') if repo == 'open-pointcloud-studio' else '',
        'sha256': asset['sha256'],
    })
rows.sort(key=lambda r: (r['repo'].lower(), r['path'].lower()))
assert len(rows) == 565
assert sum(bool(r['adopted']) for r in rows) == len(adopted) == 10
counts = Counter(r['repo'] for r in rows)
(DESIGN / 'icon-review-data.json').write_text(json.dumps({
    'status': 'visual-review-workbench',
    'scope': 'direct code references or active pyRevit pushbutton convention only',
    'count': len(rows), 'repositories': counts, 'records': rows,
}, ensure_ascii=False, indent=2) + '\n')
source = json.dumps(rows, ensure_ascii=False).replace('</', '<\\/')
options = ''.join(f'<option value="{html.escape(name, quote=True)}">{html.escape(name)} · {count}</option>'
                  for name, count in sorted(counts.items(), key=lambda x: (-x[1], x[0])))
page = '''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenAEC · UI-icoonreview</title><style>
@font-face{font-family:Inter;src:url('../assets/fonts/Inter-Regular.ttf')}*{box-sizing:border-box}body{margin:0;background:#eef0f2;color:#262a30;font:12px/1.4 Inter,'Segoe UI',sans-serif}button,select,input{font:inherit}button{cursor:pointer}.top{position:sticky;top:0;z-index:4;background:#272b32;color:#fff;border-bottom:3px solid #d97706;padding:11px 16px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}.brand{font-weight:700;letter-spacing:.05em;font-size:14px;margin-right:12px}.top select,.top input,.top button{height:32px;background:#393e47;color:#fff;border:1px solid #676e7a;border-radius:3px;padding:0 9px}.top input{width:225px}.top button{background:#bd6911;border-color:#db8a34}.top span{color:#c8cdd4}main{max-width:1560px;margin:auto;padding:18px}.notice{background:#fff;border-left:4px solid #d97706;padding:12px 15px;margin-bottom:14px}.notice a{color:#a45308}.toolbar{display:flex;align-items:center;gap:12px;margin:10px 0 15px}.toolbar button{padding:6px 10px;background:#fff;border:1px solid #c9ced5;border-radius:3px}.toolbar button:disabled{opacity:.4}.toolbar strong{margin-right:auto}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(245px,1fr));gap:10px}.card{background:#fff;border:1px solid #d4d8de;border-radius:5px;overflow:hidden;min-width:0}.card.adopted{border-color:#d97706}.card header{padding:10px 11px 7px;display:flex;align-items:start;gap:6px}.card header b{flex:1;font-size:12px;overflow-wrap:anywhere}.tag{font-size:9px;background:#edf0f3;color:#4b5560;border-radius:2px;padding:3px 5px}.card.adopted .tag{background:#fff0db;color:#93540b}.swatches{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:#d5dae0;margin:0 10px;border:1px solid #d5dae0}.swatch{height:74px;display:grid;place-items:center}.swatch.light{background:#fff}.swatch.dark{background:#282b33}.swatch img{width:var(--icon-size);height:var(--icon-size);object-fit:contain}.card .meta{padding:8px 11px;color:#59616c;font-size:10px;min-height:64px}.meta .path{overflow-wrap:anywhere;line-height:1.2;max-height:26px;overflow:hidden}.card footer{display:flex;gap:5px;align-items:center;padding:0 10px 10px}.card footer a{color:#9a570d;white-space:nowrap}.card footer select{min-width:0;flex:1;padding:5px;border:1px solid #cdd2d9;background:#fff;color:#30343b}.empty{padding:35px;text-align:center;background:#fff}.stat{font-size:11px;color:#707781}@media(max-width:650px){.top{position:static}.top input{width:100%}.grid{grid-template-columns:repeat(auto-fill,minmax(155px,1fr))}}
</style></head><body><div class="top"><div class="brand">OPENAEC · UI-ICOONREVIEW</div><input id="search" type="search" placeholder="Zoek bestandsnaam of pad…" aria-label="Zoek iconen"><select id="repo" aria-label="Repository"><option value="">Alle repositories · 565</option>REPO_OPTIONS</select><select id="filter" aria-label="Status"><option value="">Alle bewijsiconen</option><option value="adopted">Rust geadopteerd</option><option value="candidate">Naamkandidaat</option><option value="unmatched">Geen kernmatch</option><option value="reviewed">Mijn beoordelingen</option></select><select id="size" aria-label="Icoongrootte"><option value="16">16 px</option><option value="24" selected>24 px</option><option value="32">32 px</option></select><button id="export">Exporteer besluiten</button></div><main><div class="notice"><b>565 bewezen UI-bestanden uit vijf repositories.</b> Elk item heeft een broncodeverwijzing of volgt de actieve pyRevit-knopbundelconventie. Naamkandidaten zijn geen goedgekeurde betekenissen. Vergelijk de originele vorm op lichte en donkere ondergrond en leg per item een besluit vast; dat blijft lokaal in deze browser en kan als JSON worden geëxporteerd. <a href="icon-semantic-crosswalk.html">Vergelijk met de 26 gedeelde betekenissen</a> · <a href="library-icons.html">Code-importen apart</a>.</div><div class="toolbar"><strong id="count"></strong><span class="stat" id="progress"></span><button id="previous">Vorige</button><span id="page"></span><button id="next">Volgende</button></div><div id="grid" class="grid"></div></main><script>
const records=RECORDS;const key='openaec-icon-review-v1';let decisions={};try{decisions=JSON.parse(localStorage.getItem(key)||'{}')}catch{}let page=0;const PAGE_SIZE=48;const el=id=>document.getElementById(id);const escapeHtml=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));function filtered(){const q=el('search').value.trim().toLowerCase(),repo=el('repo').value,status=el('filter').value;return records.filter(r=>(!repo||r.repo===repo)&&(!q||(r.repo+' '+r.path+' '+r.candidate).toLowerCase().includes(q))&&(!status||status==='adopted'&&r.adopted||status==='candidate'&&r.candidate||status==='unmatched'&&!r.candidate||status==='reviewed'&&decisions[r.repo+'/'+r.path]))}function render(){const matches=filtered();const pages=Math.max(1,Math.ceil(matches.length/PAGE_SIZE));page=Math.min(page,pages-1);document.documentElement.style.setProperty('--icon-size',el('size').value+'px');el('count').textContent=matches.length+' iconen in huidige selectie';el('progress').textContent=Object.keys(decisions).length+' lokaal beoordeeld';el('page').textContent=(page+1)+' / '+pages;el('previous').disabled=page===0;el('next').disabled=page===pages-1;const visible=matches.slice(page*PAGE_SIZE,(page+1)*PAGE_SIZE);el('grid').innerHTML=visible.length?visible.map(r=>{const id=r.repo+'/'+r.path;const verdict=decisions[id]?.decision||'';const opts=[['','Beoordelen…'],['shared','Gedeelde kern'],['domain','Domeinicoon'],['specific','Toolspecifiek'],['redesign','Hertekenen'],['exclude','Geen UI-icoon']].map(([v,t])=>'<option value="'+v+'"'+(v===verdict?' selected':'')+'>'+t+'</option>').join('');return '<article class="card '+(r.adopted?'adopted':'')+'"><header><b>'+escapeHtml(r.path.split('/').pop())+'</b><span class="tag">'+escapeHtml(r.adopted?'Rust: '+r.adopted:r.candidate?'Kandidaat: '+r.candidate:'Review')+'</span></header><div class="swatches"><div class="swatch light"><img loading="lazy" src="'+escapeHtml(r.preview)+'" alt=""></div><div class="swatch dark"><img loading="lazy" src="'+escapeHtml(r.preview)+'" alt=""></div></div><div class="meta"><div>'+escapeHtml(r.repo)+' · '+escapeHtml(r.evidence)+'</div><div class="path">'+escapeHtml(r.path)+'</div></div><footer><a href="'+escapeHtml(r.source)+'" target="_blank" rel="noopener noreferrer">Broncode ↗</a><select data-id="'+escapeHtml(id)+'" aria-label="Besluit voor '+escapeHtml(r.path)+'">'+opts+'</select></footer></article>'}).join(''):'<div class="empty">Geen iconen gevonden.</div>';el('grid').querySelectorAll('select').forEach(select=>select.onchange=()=>{const id=select.dataset.id;if(select.value)decisions[id]={decision:select.value,name_candidate:records.find(r=>r.repo+'/'+r.path===id)?.candidate||'',updated_at:new Date().toISOString()};else delete decisions[id];try{localStorage.setItem(key,JSON.stringify(decisions))}catch{}render()})}for(const id of ['search','repo','filter','size'])el(id).addEventListener(id==='search'?'input':'change',()=>{page=0;render()});el('previous').onclick=()=>{page--;render()};el('next').onclick=()=>{page++;render()};el('export').onclick=()=>{const data={schema:'openaec-icon-review-v1',source_count:records.length,decisions};const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='openaec-icon-review-decisions.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};render();</script></body></html>'''
page = page.replace('REPO_OPTIONS', options).replace('RECORDS', source)
(DESIGN / 'icon-review-board.html').write_text(page)
print(f'Built icon review board: {len(rows)} UI assets, {len(counts)} repositories, {len(adopted)} adopted')
