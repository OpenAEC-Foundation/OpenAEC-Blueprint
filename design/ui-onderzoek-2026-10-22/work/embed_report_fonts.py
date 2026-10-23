from pathlib import Path
import base64
import hashlib
import html
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'outputs'
REPO = ROOT / 'OpenAEC-Style-Repo/crates/openaec-ui'
CACHE = ROOT / 'report-fonts'
CACHE.mkdir(exist_ok=True)

def get(url):
    with urllib.request.urlopen(url, timeout=40) as r:
        return r.read()

families = [('IBM Plex Sans', 'ibmplexsans'), ('Source Sans 3', 'sourcesans3'), ('Atkinson Hyperlegible Next', 'atkinsonhyperlegiblenext')]
def candidate_font(item):
    family, slug, weight = item
    css_url = 'https://fonts.googleapis.com/css2?family=' + family.replace(' ', '+') + ':wght@' + str(weight) + '&display=swap'
    css = get(css_url).decode()
    url = re.search(r'url\((https://fonts.gstatic.com/[^)]+)\)', css)[1]
    b = get(url)
    assert b[:4] in (b'\x00\x01\x00\x00', b'OTTO')
    path = CACHE / f'{slug}-{weight}.ttf'
    path.write_bytes(b)
    return {'family': family, 'weight': weight, 'path': path, 'url': url, 'sha256': hashlib.sha256(b).hexdigest()}

with ThreadPoolExecutor(max_workers=6) as pool:
    fonts = list(pool.map(candidate_font, [(f, s, w) for f, s in families for w in (400, 600)]))

for family, weight, filename in [('Inter',400,'Inter-Regular.ttf'),('Inter',500,'Inter-Medium.ttf'),('Inter',600,'Inter-SemiBold.ttf'),('Space Grotesk',500,'SpaceGrotesk-Medium.ttf'),('Space Grotesk',700,'SpaceGrotesk-Bold.ttf')]:
    path = REPO / 'assets/fonts' / filename
    fonts.append({'family': family, 'weight': weight, 'path': path, 'url': 'OpenAEC repository snapshot: ' + filename, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})

licenses=[]
for family,slug in families:
    url=f'https://raw.githubusercontent.com/google/fonts/main/ofl/{slug}/OFL.txt'
    content=get(url).decode()
    assert 'SIL OPEN FONT LICENSE' in content
    (CACHE/f'{slug}-OFL.txt').write_text(content)
    licenses.append((family, content))
for family,filename in [('Inter','Inter-OFL.txt'),('Space Grotesk','SpaceGrotesk-OFL.txt')]:
    licenses.append((family,(REPO/'licenses'/filename).read_text()))

rules=[]
for font in fonts:
    encoded=base64.b64encode(font['path'].read_bytes()).decode()
    rules.append('@font-face{font-family:"'+font['family']+'";font-weight:'+str(font['weight'])+';font-style:normal;font-display:swap;src:url(data:font/ttf;base64,'+encoded+') format("truetype")}')

path=OUT/'OpenAEC-ontwerponderzoek.html'
s=path.read_text()
s=re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com/[^>]+>','<style id="embedded-report-fonts">'+''.join(rules)+'</style>',s,count=1)
s=s.replace('De voorbeeldfonts worden online geladen via Google Fonts en kunnen verschillen van de exacte gebundelde TTF-versie. Zonder internet blijft het rapport leesbaar, maar kunnen de voorbeeldfonts terugvallen op een systeemfont.','De fonts zijn in dit rapport ingebed en werken zonder internet. Inter en Space Grotesk zijn de ongewijzigde bestanden uit de onderzochte repo. De drie andere kandidaten zijn vastgelegde Google Fonts-bestanden. Dit is een browservergelijking; de native rendering moet later apart worden getoetst.')
s=s.replace('Rapporttekst is lokaal leesbaar; externe fontproeven en bronlinks vragen internet.','Rapporttekst en fontproeven zijn lokaal beschikbaar; externe bronlinks vragen internet.')
notice='<details><summary>Licentieteksten van de ingebedde voorbeeldfonts</summary>'+''.join('<h3>'+html.escape(name)+'</h3><pre>'+html.escape(content)+'</pre>' for name,content in licenses)+'</details>'
s=s.replace('</ol>\n</section>\n</main>','</ol>'+notice+'\n</section>\n</main>')
path.write_text(s)
evidence_path=OUT/'OpenAEC-onderzoeksbewijs.json'
evidence=json.loads(evidence_path.read_text())
evidence['report_fonts']=[{k:str(v) for k,v in f.items() if k!='path'} for f in fonts]
evidence['report_font_notice']='Unmodified font binaries embedded in the HTML. Complete OFL notices included in its final section.'
evidence['google_inter_probe']={'url':'https://fonts.gstatic.com/s/inter/v20/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfMZg.ttf','version':'Version 4.001;git-66647c0bb','sha256':hashlib.sha256((ROOT/'Inter-Google.ttf').read_bytes()).hexdigest(),'absent_features':['ss02','ss04','cv05','cv08'],'scope':'Specific TTF returned to this research request. Delivery may differ with request context.'}
evidence_path.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'fonts':len(fonts),'report_bytes':path.stat().st_size,'families':[x[0] for x in licenses]},ensure_ascii=False))
