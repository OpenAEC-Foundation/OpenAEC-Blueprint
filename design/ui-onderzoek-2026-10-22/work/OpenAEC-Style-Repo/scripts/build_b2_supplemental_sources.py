"""Capture additional pinned UI call sites without modifying the original catalog.

This reads upstream text only. No upstream component, extension or installer runs.
The stored context describes behavior; upstream icon geometry is not copied.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'harmonization/icon-set-b2/supplemental-sources.json'
SHA='0961d795ce4f0e0ec14d3b25d223f8ced1879d0b'
INSTALLER=ROOT/'harmonization/sources/overnight/openaec-installer'

POINTS=[
 ('src/App.tsx',411,'search','Tools zoeken','Zoekinvoer filtert naam, beschrijving en vertaalde categorie.'),
 ('src/App.tsx',429,'refresh','Installaties en releases vernieuwen','refresh(true) scant installaties en haalt releasegegevens; de knop is tijdens verwerking disabled.'),
 ('src/components/CategoryIcon.tsx',98,'category-dispatch','Toolcategorie','De renderer kiest paths[category]; elf expliciete categorievarianten.'),
 ('src/components/Modal.tsx',98,'modal-close','Dialoog sluiten','De tekstglyph times roept onClose van de lokale dialoog aan.'),
 ('src/components/OpenAecLogo.tsx',9,'brand','OpenAEC-merkbeeld','Merkbeeld in titelbalk en cataloguskop; geen functieopdracht.'),
 ('src/components/SelfUpdateBanner.tsx',47,'update-available','Installerupdate beschikbaar','Vast beeld bij een nieuwere eigen release; geen actie op het beeld.'),
 ('src/components/SelfUpdateBanner.tsx',91,'self-update','Installer bijwerken','onUpdate volgt handleSelfUpdate en downloadAndRunInstaller; Linux vervangt eigen AppImage en vraagt daarna herstart.'),
 ('src/components/SelfUpdateBanner.tsx',101,'update-dismiss','Updatemelding sluiten','onDismiss verbergt de eigen updatemelding voor deze sessie.'),
 ('src/components/TabBar.tsx',30,'catalog','Appcatalogus tonen','De vaste catalogustab selecteert CATALOG_TAB; open webtooltabs blijven behouden.'),
 ('src/components/TabBar.tsx',60,'tab-close','Webtooltab sluiten','onClose(id) verwijdert die tab via closeTab; geen appvenster sluiten.'),
 ('src/components/ThemedSelect.tsx',34,'select','Keuzelijst openen','De trigger toggelt open; een optie roept onChange aan en sluit het menu.'),
 ('src/components/TitleBar.tsx',78,'settings','Voorkeuren','onSettingsClick opent SettingsDialog in App.'),
 ('src/components/TitleBar.tsx',98,'minimize','Venster minimaliseren','handleMinimize roept het native minimize aan.'),
 ('src/components/TitleBar.tsx',110,'restore','Venster herstellen','isMaximized kiest de herstelvorm; toggleMaximize herstelt het native venster.'),
 ('src/components/TitleBar.tsx',115,'maximize','Venster maximaliseren','De normale venstertoestand toont maximaliseren; toggleMaximize bedient het native venster.'),
 ('src/components/TitleBar.tsx',127,'window-close','Appvenster sluiten','handleClose roept native close aan.'),
 ('src/components/ToolCard.tsx',143,'launch','Geïnstalleerde app starten','De previewshortcut met kind launch volgt onLaunch naar launchTool(exePath).'),
 ('src/components/ToolCard.tsx',147,'preview-open','Tool openen','De open-previewshortcut opent de webversie in een interne tab wanneer webUrl bestaat, anders de externe product- of repopagina.'),
 ('src/components/ToolCard.tsx',179,'installed-version','Geïnstalleerde versie','Vaste Check naast installed.version; dit bewijst niet dat de geïnstalleerde versie de nieuwste is.'),
 ('src/components/ToolCard.tsx',190,'version-upgrade','Beschikbare opvolgversie','De tekstpijl tussen installed en latest verschijnt uitsluitend bij update_available.'),
 ('src/components/ToolCard.tsx',237,'install-or-update','Tool installeren of bijwerken','De tekstknop kiest Installeren of Bijwerken volgens status en roept onInstall naar handleInstall aan.'),
 ('src/components/ToolCard.tsx',265,'repository-link','Bronrepository openen','De knop opent de GitHub-URL via openUrl; geen gitopdracht. Het merklogo wordt niet overgenomen.'),
 ('src/components/ToolCard.tsx',279,'webtab','Webversie in tab openen','onOpenTab voert openTab uit en bewaart tabstate; de tool draait daarna in een iframe.'),
 ('src/components/ToolCard.tsx',293,'web-external','Webversie extern openen','open(tool.webUrl) opent de URL via het platform.'),
 ('src/components/ToolCard.tsx',307,'website','Productwebsite openen','open(tool.siteUrl) opent de externe productpagina.'),
 ('src/components/WebToolView.tsx',36,'web-reload','Webtool herladen','reload verhoogt reloadKey en remount het iframe; de huidige webtool wordt opnieuw geladen.'),
 ('src/components/WebToolView.tsx',49,'webtool-external','Webtool extern openen','openUrl(url) opent dezelfde webtool in de externe browser.'),
 ('src/components/settings/SettingsDialog.tsx',249,'theme-menu','Themakeuze openen','De thematrigger toggelt open; de afzonderlijke optie kiest het thema.'),
]
CATEGORIES={'calculatie':'Calculatie','cad':'CAD','constructief':'Constructief','geotechniek':'Geotechniek','bim':'BIM','planning':'Planning','documenten':'Documenten','ai':'AI en spraak','energie':'Energie','veld':'Veldwerk','gis':'GIS'}

def digest(b):return hashlib.sha256(b).hexdigest()
def record(app,repo,commit,path,line,name,label,meaning,root):
    raw=(root/path).read_bytes()
    assert 0<line<=len(raw.decode().splitlines())
    rid=digest(f'{repo}\n{commit}\n{path}\n{line}\n{name}'.encode())[:16]
    return {'app':app,'repository':repo,'commit':commit,'name':name,'label':label,
            'path':path,'line':line,'role':'expliciete UI-bronplaats','evidence':'aanvullende gepinde bronreview',
            'review':None,'assessment':{},'state':'','origin':'b2-supplemental-source-review',
            'context':meaning,'source_url':f'https://github.com/OpenAEC-Foundation/{repo}/blob/{commit}/{path}#L{line}',
            'asset':None,'exact_hash':None,'geometry_hash':None,'origins':['b2-supplemental-source-review'],
            'function_id':'supplement.'+rid,'function_status':'afzonderlijk beoordeeld in B2',
            'id':rid,'function_label':label,'category':'Aanvullende bronplaatsen',
            'source_file_sha256':digest(raw),'source_git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}

def main():
    records=[];corpus=[]
    for p in sorted((INSTALLER/'files').rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(INSTALLER/'files').as_posix();raw=p.read_bytes()
        actual=subprocess.check_output(['git','hash-object','--no-filters',str(p)],text=True).strip()
        pinned=subprocess.check_output(['git','--git-dir='+str(INSTALLER/'.git'),'rev-parse',SHA+':'+rel],text=True).strip()
        assert actual==pinned,(rel,actual,pinned)
        corpus.append({'path':rel,'sha256':digest(raw),'git_blob':pinned,'bytes':len(raw)})
    for path,line,name,label,meaning in POINTS:
        records.append(record('Installer','openaec-installer',SHA,path,line,name,label,meaning,INSTALLER/'files'))
    path='src/components/CategoryIcon.tsx';text=(INSTALLER/'files'/path).read_text()
    for key,label in CATEGORIES.items():
        match=re.search(r'^    '+key+r': \(',text,re.M);assert match
        line=text[:match.start()].count('\n')+1
        records.append(record('Installer','openaec-installer',SHA,path,line,'category-'+key,label+'-categorie',
            'Vast onderwerpbeeld voor toolcategorie '+key+' in kaartkop, previewfallback en webtooltab; geen gereedschap uitvoeren.',INSTALLER/'files'))
    calc=ROOT/'harmonization/sources/overnight/open-calc-studio/files';commit='b47042704efa388d95eb59ce77d23aeb5ee0e44c'
    records.append(record('Calc','open-calc-studio',commit,'src/components/ribbon/SpreadsheetTab.tsx',77,'decimals-up','Meer decimalen',
        'De .0-knop emit spreadsheet-action decimals-up. SubSheetEditor.tsx:235 verhoogt de decimalen van iedere geselecteerde cel met één, vanaf de standaardwaarde twee.',calc))
    calc_evidence=[]
    for path in ['src/components/ribbon/SpreadsheetTab.tsx','src/components/grid/SubSheetEditor.tsx']:
        raw=(calc/path).read_bytes()
        oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        expected=subprocess.check_output(['git','--git-dir='+str(calc.parent/'.git'),'rev-parse',commit+':'+path],text=True).strip()
        assert oid==expected
        calc_evidence.append({'path':path,'sha256':digest(raw),'git_blob':oid,'commit':commit})
    payload={'schema':1,'additional_evidence_files':calc_evidence,'scope':'Aanvullende B2-bronplaatsen: volledige Installer-iconinventaris en ontbrekende Calc-decimale verhoging.',
        'basis':'Brontekst op de genoemde commits gelezen; geen upstream-code uitgevoerd en geen broniconengeometrie overgenomen.',
        'installer_corpus':{'repository':'openaec-installer','commit':SHA,'license':'CC BY-SA 4.0 (bronrepository; geen artwork overgenomen)','files':corpus},
        'records':records}
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(records)} supplemental records; {len(corpus)} verified Installer text files')

if __name__=='__main__':main()
