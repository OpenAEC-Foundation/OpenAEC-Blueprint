"""Build a small, explicit index of user feedback and its current disposition."""
from pathlib import Path
import html
import json
from urllib.parse import quote

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'design/icon-set-b2'
AUDIT=ROOT/'harmonization/icon-set-b2'
LABELS={'master':'Master bijgewerkt; beoordeling open','proposal':'Alleen voorbeeld bijgewerkt; niet toegepast','open':'Nog open','process':'Afspraak of werkwijze vastgelegd','approved':'Door jou goedgekeurd'}

def esc(value):return html.escape(str(value),quote=True)

def build():
    feedback=json.loads((AUDIT/'feedback-overview.json').read_text(encoding='utf8'))
    manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf8'))
    icons={i['id']:i for i in manifest['icons']}
    analyses={};rounds=[];applied={}
    for rev in (97,99,104):
        report=json.loads((AUDIT/f'analysis-review-{rev}.json').read_text(encoding='utf8'))
        for row in report['icons']:analyses[row['id']]={**row,'page':f'analysis-review-{rev}.html'}
    final=AUDIT/'final-review-104.json'
    if final.exists():
        for row in json.loads(final.read_text(encoding='utf8'))['icons']:analyses[row['id']]={**row,'page':'final-review-104.html'}
    for path in sorted(AUDIT.glob('feedback-review-*.json'),key=lambda p:int(p.stem.rsplit('-',1)[1])):
        report=json.loads(path.read_text(encoding='utf8'));records=report.get('icons',[])
        if report.get('id'):records=[report]
        for row in records:applied[row['id']]=int(report['revision'])
        rounds.append({'path':path.name,'revision':report['revision'],'date':report.get('date',''),'icons':[r['id'] for r in records]})
    last={key:row['number'] for row in feedback['feedback'] for key in row['icons']}
    def link(key):
        icon=icons[key];a=analyses.get(key)
        if a:return a['page']+f'?revision={manifest["revision"]}#icon-'+quote(key,safe='.')
        return 'completion-review.html#:~:text='+quote(icon['label'],safe='')
    def state(key):
        if key in feedback.get('approved_icons',[]):return 'approved'
        a=analyses.get(key,{})
        if a.get('decision')=='proposed':return 'proposal'
        if a.get('decision')=='corrected' or key in applied:return 'master'
        return 'open'
    cards=[]
    for row in feedback['feedback']:
        keys=row['icons'];states=sorted({state(key) for key in keys}) if keys else ['process']
        chips=''.join(f'<span class="chip {kind}">{LABELS[kind]}</span>' for kind in states)
        links=''.join(f'<p><a href="{esc(link(key))}">{esc(icons[key]["label"])}</a> <code>{esc(key)}</code></p>' for key in keys)
        evidence=[]
        for key in keys:
            icon=icons[key];a=analyses.get(key,{});source=icon.get('source_example') or {}
            action=a.get('action') or ('De master is geregistreerd als gewijzigd in revisie '+str(applied[key])+'. Bekijk de actuele vorm.' if key in applied else 'Geen geregistreerde wijziging gevonden; dit punt blijft open.')
            source_link=f'<a href="{esc(source.get("source_url",""))}">{esc(source.get("app",""))} · {esc(source.get("path",""))}:{esc(source.get("line",""))}</a>' if source else 'Geen afzonderlijk bronvoorbeeld.'
            hashes=' · '.join(f'{size}px <code>{asset["sha256"]}</code>' for size,asset in icon['assets'].items())
            evidence.append(f'<h4>{esc(icon["label"])}</h4><p>{esc(action)}</p><p>{esc(icon["meaning"])}</p><p>{source_link}<br>Broncommit: <code>{esc(source.get("commit",""))}</code></p><p class="hashes">{hashes}</p>')
        later=sorted({last[key] for key in keys if last[key]>row['number']})
        follow=' · '.join(f'<a href="#feedback-{n}">#{n}</a>' for n in later)
        later_note=f'<p class="muted">Later opnieuw besproken bij {follow}.</p>' if later else ''
        process=''
        if not keys:
            process={29:'Uitgevoerd als proef van 60 iconen; daarna gevolgd door 240.',32:'De voorkeur is bewaard; latere kritiek op platte vormen nuanceert de losse-accentregel.',33:'Alle 22 oorspronkelijke voorstellen hebben een getekend voorbeeld.',43:'De dubbele reviewgegevens worden vervangen door één gedeeld bestand; kleine voorbeeldwijzigingen bouwen alleen de betrokken concepten en analysepagina.',44:'Dit overzicht bewaart de feedback chronologisch en linkt naar de afzonderlijke uitwerking.',51:'Bij iedere volgende ronde worden de cirkelboog, pijlpunt, aansluiting en verwante gevallen expliciet samen gecontroleerd.'}.get(row['number'],'Vastgelegd in de ontwerpafspraken hierboven.')
        detail='<details><summary>Uitwerking, functie, bron en hashes</summary>'+''.join(evidence)+'</details>' if evidence else '<p>'+esc(process)+'</p>'
        search=row['feedback']+' '+' '.join(keys)+' '+' '.join(icons[key]['label'] for key in keys)
        cards.append(f'<article id="feedback-{row["number"]}" data-states="{" ".join(states)}" data-search="{esc(search.lower())}"><div class="row"><span class="number">#{row["number"]:02}</span>{chips}</div><h3>{esc(row["feedback"])}</h3>{links}{later_note}{detail}</article>')
    archive=[]
    remaining=''
    latest=AUDIT/f'feedback-review-{manifest["revision"]}.json'
    latest_report=json.loads(latest.read_text(encoding='utf8')) if latest.exists() else {}
    counts=latest_report.get('remaining')
    if counts:
        latest_page=latest_report.get('review_page') or (f'feedback-analysis-{manifest["revision"]}.html' if (OUT/f'feedback-analysis-{manifest["revision"]}.html').exists() else 'analysis-review-99.html')
        remaining=f'<section id="remaining"><h2>Wat staat nog open?</h2><p><strong>{len(counts["unprocessed_registered_feedback_points"])} onverwerkte vastgelegde feedbackpunten</strong>. De uitwerkingen wachten nog op jouw visuele beoordeling.</p><p><strong>{counts["proposals_total"]} losse voorstellen</strong> om te beoordelen: {counts["proposals_97"]} uit de eerste analyse en {counts["proposals_99"]} uit de tweede. Daarnaast vallen <strong>{counts["not_yet_in_consecutive_analysis"]} iconen</strong> in series 162–166 nog buiten deze opeenvolgende analyse.</p><p>Deze ronde: {counts["current_canonical_changes_for_user_review"]} gebruikte ontwerpen en {counts["current_proposal_changes_included_in_64"]} voorbeelden herzien. Die voorbeelden zitten al in de {counts["proposals_total"]} voorstellen. <a href="analysis-review-99.html?revision={manifest["revision"]}&amp;filter=corrected">Bekijk de correcties</a>.</p></section>'
    for item in rounds:
        names=' · '.join(f'<a href="{esc(link(key))}">{esc(icons[key]["label"])}</a>' for key in item['icons'] if key in icons)
        archive.append(f'<details><summary>Revisie {item["revision"]} · {esc(item["date"])} · {len(item["icons"])} geregistreerde icoonwijzigingen</summary><p>{names}</p><p><a href="../../harmonization/icon-set-b2/{esc(item["path"])}">Oorspronkelijk wijzigingsrapport met bronbewijs</a></p></details>')
    css='''<style>:root{color-scheme:dark;--bg:#28282e;--panel:#323239;--ink:#ebebeb;--muted:#c1c1c8;--line:#818187;--accent:#ed8c00}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 system-ui,sans-serif}main{max-width:1200px;margin:auto;padding:24px}h1{font-size:27px;margin:0 0 10px}h2{font-size:21px;margin:28px 0 12px}h3{font-size:16px;margin:12px 0}h4{margin-bottom:4px}a{color:inherit;text-underline-offset:3px}p{margin:8px 0}code{font:11px ui-monospace,monospace;overflow-wrap:anywhere}.muted{color:var(--muted)}.lead{max-width:950px}.controls{position:sticky;top:0;z-index:2;display:flex;flex-wrap:wrap;gap:10px;padding:14px 0;background:var(--bg);border-bottom:1px solid var(--line)}select,input{font:inherit;padding:8px;border:1px solid var(--line);border-radius:5px;background:var(--panel);color:inherit}input{min-width:240px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(440px,100%),1fr));gap:14px;align-items:start}article{border:1px solid var(--line);border-radius:9px;padding:16px;background:var(--panel);scroll-margin-top:95px}article:target{outline:2px solid var(--accent)}.row{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.number{color:var(--muted);font-size:12px}.chip{border:1px solid var(--line);padding:2px 6px;border-radius:4px;font-size:11px}.proposal{border-color:var(--accent)}.open{border-color:#e57373}summary{cursor:pointer}.hashes{font-size:10px;overflow-wrap:anywhere}details{margin:14px 0}[hidden]{display:none!important}li{margin:5px 0}:focus-visible{outline:3px solid var(--accent);outline-offset:2px}@media(max-width:600px){main{padding:14px}.controls{position:static}}</style>'''
    intro=f'''<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jouw vastgelegde iconenfeedback</title>{css}<main><h1>Jouw vastgelegde iconenfeedback</h1><div class="lead"><p><strong>{len(feedback['feedback'])} feedbackpunten uit dit gesprek</strong>, met de actuele uitwerking en oudere wijzigingsrondes. De opmerkingen zijn kort weergegeven; dit is geen volledige chattranscriptie.</p><p><strong>Master bijgewerkt</strong> betekent dat het gebruikte ontwerp is gewijzigd. <strong>Alleen voorbeeld bijgewerkt</strong> betekent dat de wijziging nog als afzonderlijk voorstel staat. Een wijziging krijgt daarmee geen automatische goedkeuring van jou.</p><p><a href="analysis-review-97.html?filter=proposed">Eerste 60 · 22 getekende voorstellen</a> · <a href="analysis-review-99.html?filter=proposed&revision={manifest['revision']}">Volgende 240 · 42 getekende voorstellen</a> · <a href="completion-review.html">Alle iconen</a></p></div><details><summary>Ontwerpafspraken uit jouw feedback</summary><ol>{''.join('<li>'+esc(a)+'</li>' for a in feedback['principles'])}</ol></details><div class="controls"><select id="state" aria-label="Status"><option value="all">Alle feedback</option><option value="master">Master bijgewerkt</option><option value="proposal">Alleen voorstel bijgewerkt</option><option value="open">Nog open</option><option value="process">Afspraken en werkwijze</option></select><input id="search" type="search" placeholder="Zoek bijvoorbeeld potlood of printer" aria-label="Zoek feedback"></div><p id="count" role="status"></p><section class="grid">{''.join(cards)}</section><h2>Oudere vastgelegde wijzigingsrondes</h2><p class="muted">Deze dossiers bevatten de geregistreerde uitwerking en bronbewijzen. Ze bevatten niet de letterlijke eerdere gebruikersberichten.</p>{''.join(archive)}<p class="muted">Bijgewerkt op 22 oktober 2026 · icoonmasters revisie {manifest['revision']}. Bronbestand: <a href="../../harmonization/icon-set-b2/feedback-overview.json">feedback-overview.json</a>.</p></main>'''
    if counts:remaining=remaining.replace('href="analysis-review-99.html?revision=',f'href="{latest_page}?revision=')
    if counts and counts['not_yet_in_consecutive_analysis']==0:
        remaining=remaining.replace('Daarnaast vallen <strong>0 iconen</strong> in series 162–166 nog buiten deze opeenvolgende analyse.','Alle laatste 16 iconen zijn nu geanalyseerd: negen aangepast en zeven behouden.')
        remaining=remaining.replace('Deze ronde: 46 gebruikte ontwerpen en 10 voorbeelden herzien.','Ter eindbeoordeling: 46 aangepaste ontwerpen en 64 alternatieven. Tien van deze voorbeelden zijn in de laatste ronde hertekend.')
    if counts and counts['proposals_total']==0:
        remaining=f'<section id="remaining"><h2>Wat staat nog open?</h2><p><strong>0 onverwerkte vastgelegde feedbackpunten</strong> en <strong>0 losse voorstellen</strong>. Alle 61 resterende varianten zijn op jouw slotakkoord toegepast, met behoud van de drie eerdere uitzonderingen.</p><p>Alleen het herstelde vierkant bij <a href="final-review-104.html?revision={manifest["revision"]}#icon-integration.platform-sync">Platform synchroniseren</a> is na dit akkoord nog aangepast. Bibliotheek- en appintegratie volgen afzonderlijk.</p></section>'
    if final.exists():intro=intro.replace('<details><summary>Ontwerpafspraken','<p><a href="final-review-104.html">Eindoverzicht: correcties, vier groepen van 16 voorstellen en de laatste 16</a></p><details><summary>Ontwerpafspraken',1)
    intro=intro.replace('<details><summary>Ontwerpafspraken',remaining+'<details><summary>Ontwerpafspraken',1)
    script='''<script>const rows=[...document.querySelectorAll('article[data-states]')],search=document.getElementById('search'),state=document.getElementById('state');function render(){const q=search.value.toLocaleLowerCase('nl');let visible=0;for(const row of rows){row.hidden=(state.value!=='all'&&!row.dataset.states.split(' ').includes(state.value))||!row.dataset.search.includes(q);if(!row.hidden)visible++}document.getElementById('count').textContent=visible+' van '+rows.length+' feedbackpunten zichtbaar'}search.oninput=render;state.onchange=render;render();</script></html>'''
    target=OUT/'feedback-overview.html';temp=target.with_suffix('.html.tmp');temp.write_text(intro+script,encoding='utf8',newline='\n');temp.replace(target)
    print(f'{len(cards)} feedbackpunten; {len(rounds)} wijzigingsdossiers; {target.stat().st_size} bytes.')

if __name__=='__main__':build()
