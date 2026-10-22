"""Build the bounded, source-linked B2 analysis review from its assessment JSON."""
from pathlib import Path
import argparse
import hashlib
import html
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'design/icon-set-b2'
REPORT = ROOT / 'harmonization/icon-set-b2/analysis-review-97.json'
LABELS = {'corrected': 'Doorgevoerd', 'proposed': 'Voorstel', 'retain': 'Behouden'}


def esc(value):
    return html.escape(str(value), quote=True)


class SvgRenderer:
    def __init__(self):
        self.sequence = 0

    def svg(self, path, size):
        self.sequence += 1
        source = (OUT / path).read_text(encoding='utf-8')
        source = source.replace('b2-blend-', f'b2-analysis-{self.sequence}-')
        source = re.sub(r'width="[0-9]+"', f'width="{size}"', source, count=1)
        return re.sub(r'height="[0-9]+"', f'height="{size}"', source, count=1)

    def sample(self, row, state):
        paths = {size: row['proposal_assets'][str(size)]['path'] if state == 'proposal' else row['assets'][str(size)][state + '_path'] for size in (16, 24)}
        hero = self.svg(paths[24], 52)
        native = ''.join('<span>' + self.svg(paths[16 if n == 16 else 24], n) + f'<small>{n} px</small></span>' for n in (16, 24, 32))
        return '<div class="hero">' + hero + '</div><div class="native">' + native + '</div>'


def build(report_path=REPORT, output_path=None):
    report = json.loads(report_path.read_text(encoding='utf-8'))
    assert len(report['icons']) == report['range']['count']
    renderer = SvgRenderer()
    cards = []
    for row in report['icons']:
        decision = row['decision']
        if decision == 'corrected':
            samples = '<div class="comparison"><div><h3>Voor</h3>' + renderer.sample(row, 'before') + '</div><div><h3>Nu</h3>' + renderer.sample(row, 'after') + '</div></div>'
        elif decision == 'proposed' and row.get('proposal_assets'):
            samples = '<div class="comparison"><div><h3>Huidig</h3>' + renderer.sample(row, 'after') + '</div><div><h3>Getekend voorbeeld</h3>' + renderer.sample(row, 'proposal') + '</div></div><p class="muted">Voorstel: nog niet toegepast op het gebruikte icoon.</p>'
        else:
            samples = '<div class="single">' + renderer.sample(row, 'after') + '</div>'
        source = row['source']
        hashes = ''.join(f'<li>{size} px: <code>{esc(asset["before_sha256"])}</code> → <code>{hashlib.sha256((OUT / asset["after_path"]).read_bytes()).hexdigest()}</code></li>' for size, asset in row['assets'].items())
        search = ' '.join(str(row[k]) for k in ('id', 'label', 'finding', 'action'))
        gap = row['metrics_before']['16'].get('raw_gap_px')
        measured = '' if gap is None else f'<p class="muted">Afstand vóór correctie op 16 px: {gap:.3f} px. Aansluitingen zijn per betekenis beoordeeld.</p>'
        cards.append(f'<article id="icon-{esc(row["id"])}" data-decision="{decision}" data-priority="{esc(row["priority"])}" data-search="{esc(search.lower())}"><header><span class="badge {decision}">{LABELS[decision]}</span><span class="muted">{row["number"]:02} / {len(report["icons"])} · serie {row["series"]}</span><h2>{esc(row["label"])}</h2><code>{esc(row["id"])}</code></header>{samples}<p><strong>Mijn bevinding:</strong> {esc(row["finding"])}</p><p><strong>{"Aangepast" if decision == "corrected" else "Ik zou doen" if decision == "proposed" else "Mijn oordeel"}:</strong> {esc(row["action"])}</p><p class="muted">Prioriteit: {esc(row["priority"])}.</p><details><summary>Functie, bron en controle</summary><p>{esc(row["ui_call"])}</p><p><a href="{esc(source["source_url"])}" target="_blank" rel="noopener">{esc(source["app"])} · {esc(source["path"])}:{source["line"]}</a><br>Broncommit: <code>{esc(source["commit"])}</code></p><pre>{esc(source["context"])}</pre>{measured}<ul class="hashes">{hashes}</ul></details></article>')
    criteria = ''.join('<li>' + esc(c) + '</li>' for c in report['criteria'])
    document = r'''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>__TITLE__</title><style>
:root{color-scheme:dark;--bg:#28282e;--panel:#323239;--ink:#ebebeb;--muted:#c1c1c8;--border:#818187;--icon-accent:#ed8c00}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 system-ui,sans-serif}body.light{color-scheme:light;--bg:#f4f4f4;--panel:#fff;--ink:#202020;--muted:#555;--border:#999;--icon-accent:#a55400}body.mono{--icon-accent:var(--ink)}a{color:var(--ink);text-underline-offset:3px}main{max-width:1500px;margin:auto;padding:24px}h1{font-size:26px;line-height:1.2;margin:0 0 12px}h2{font-size:17px;line-height:1.3;margin:10px 0 3px}h3{font-size:12px;font-weight:500;color:var(--muted);margin:0}.lead{max-width:950px}p{margin:10px 0}.muted{color:var(--muted);font-size:12px}.controls{position:sticky;top:0;z-index:2;background:var(--bg);border-bottom:1px solid var(--border);padding:14px 0;display:flex;flex-wrap:wrap;gap:10px;align-items:center}button,input,select{font:inherit;border:1px solid var(--border);border-radius:6px;padding:8px;background:var(--panel);color:var(--ink)}button{cursor:pointer}button[aria-pressed="true"]{outline:2px solid var(--icon-accent);outline-offset:1px}input[type="search"]{min-width:230px}input[type="checkbox"]{accent-color:var(--icon-accent)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(390px,100%),1fr));gap:16px;align-items:start}article{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:18px;scroll-margin-top:160px}article:target{outline:3px solid var(--icon-accent);outline-offset:2px}article header .muted{float:right}.badge{display:inline-block;border:1px solid var(--border);border-radius:4px;padding:1px 7px;font-size:11px}.proposed{border-color:var(--icon-accent)}.comparison{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:18px 0}.single{margin:18px 0}.hero{height:80px;display:flex;justify-content:center;align-items:center}.native{height:63px;display:flex;justify-content:center;gap:22px;align-items:end}.native span{display:flex;flex-direction:column;align-items:center;gap:5px}.native small{font-size:10px;color:var(--muted)}code{font:11px/1.4 ui-monospace,monospace;overflow-wrap:anywhere}.hashes{padding-left:18px}.hashes code{font-size:9px}details{margin:15px 0}summary{cursor:pointer}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:11px/1.5 ui-monospace,monospace}.criteria{max-width:1000px}.empty{padding:30px;border:1px solid var(--border)}[hidden]{display:none!important}:focus-visible{outline:3px solid var(--icon-accent);outline-offset:3px}@media(max-width:600px){main{padding:14px}.controls{position:static}.grid{grid-template-columns:1fr}}
</style><main><h1>__TITLE__</h1><div class="lead"><p>__INTRO__ Beoordeeld op je eerdere feedback, met de concrete bronfunctie erbij.</p><p><strong>__CORRECTED__ duidelijke correcties doorgevoerd · __PROPOSED__ voorstellen om zelf te beoordelen · __RETAIN__ behouden.</strong> De voorstellen zijn niet doorgevoerd. Bij de correcties kun je de vorige vorm met de huidige vorm vergelijken op 16, 24 en 32 px.</p><p><a href="completion-review.html">Terug naar de volledige iconenreview</a> · <a href="feedback-overview.html">Jouw eerdere feedback</a> · <a href="analysis-review-97.html">Eerste 60 en 22 voorbeelden</a> · <a href="analysis-review-99.html">Volgende 240 en 42 voorbeelden</a> · Analyse van 22 oktober 2026, revisie __REVISION__.</p></div><details class="criteria"><summary>Waarop ik heb gelet</summary><ol>__CRITERIA__</ol><p>Een afstand van nul is geen automatische fout: een bladhoek, verbonden hoek, grafiekas of gevuld bovenvlak kan bewust aansluiten. De gemeten afstand is samen met de betekenis en de weergave op klein formaat beoordeeld.</p></details><div class="controls" aria-label="Reviewfilters"><button data-filter="proposed" aria-pressed="true">Voorstellen (__PROPOSED__)</button><button data-filter="corrected" aria-pressed="false">Aangepast (__CORRECTED__)</button><button data-filter="retain" aria-pressed="false">Behouden (__RETAIN__)</button><button data-filter="all" aria-pressed="false">Alle __COUNT__</button><input id="search" type="search" aria-label="Zoek in deze __COUNT__ iconen" placeholder="Zoek icoon of bevinding"><label>Thema <select id="theme"><option value="dark">Donker</option><option value="light">Licht</option></select></label><label><input id="mono" type="checkbox"> Eén kleur</label></div><p id="count" role="status"></p><section class="grid" aria-label="Beoordelingen">__CARDS__</section><p class="empty" id="empty" hidden>Geen iconen met dit filter.</p></main><script>
let filter='proposed';const cards=[...document.querySelectorAll('article[data-decision]')];const search=document.getElementById('search');function render(){const q=search.value.toLocaleLowerCase('nl');let visible=0;for(const card of cards){card.hidden=(filter!=='all'&&card.dataset.decision!==filter)||!card.dataset.search.includes(q);if(!card.hidden)visible++}document.getElementById('count').textContent=visible+' van __COUNT__ iconen zichtbaar';document.getElementById('empty').hidden=visible!==0;for(const button of document.querySelectorAll('[data-filter]'))button.setAttribute('aria-pressed',String(button.dataset.filter===filter))}for(const button of document.querySelectorAll('[data-filter]'))button.onclick=()=>{filter=button.dataset.filter;render()};search.oninput=render;document.getElementById('theme').onchange=e=>document.body.classList.toggle('light',e.target.value==='light');document.getElementById('mono').onchange=e=>document.body.classList.toggle('mono',e.target.checked);const requested=new URLSearchParams(location.search).get('filter');if(['proposed','corrected','retain','all'].includes(requested))filter=requested;const target=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(target&&target.dataset.decision)filter=target.dataset.decision;render();if(target)requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));
</script></html>'''
    intro = f'De volgende {len(report["icons"])} iconen vanaf <strong>{esc(report["icons"][0]["label"])}</strong> tot <strong>{esc(report["icons"][-1]["label"])}</strong>, series {esc(report["range"]["series"])}.'
    values = {'TITLE': report['title'], 'COUNT': str(len(report['icons'])), 'CORRECTED': str(report['summary']['corrected']), 'PROPOSED': str(report['summary']['proposed']), 'RETAIN': str(report['summary']['retain'])}
    for key, value in values.items(): document = document.replace('__' + key + '__', esc(value))
    document = document.replace('__INTRO__', intro)
    document = document.replace('__REVISION__', str(report['revision'])).replace('__CRITERIA__', criteria).replace('__CARDS__', ''.join(cards))
    target = output_path or (OUT / (report_path.stem + '.html'))
    temporary = target.with_suffix('.html.tmp')
    temporary.write_text(document, encoding='utf-8', newline='\n')
    os.replace(temporary, target)
    print(f'{target}: {len(report["icons"])} iconen; {report["summary"]}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path, default=REPORT)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    build(args.report, args.output)
