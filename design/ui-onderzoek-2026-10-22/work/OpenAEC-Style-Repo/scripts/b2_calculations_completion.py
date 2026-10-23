"""Calculations: distinguish mounted project controls from unused ribbon definitions."""
from b2_second_series import box

GROUPS = {106: 'Rekenmodules kiezen'}
ROWS = [(106, 'calculation.module-picker', 'Rekenmodule kiezen',
         'De modulekiezer openen; een gekozen normblad wordt pas met Toevoegen of dubbelklik in het project gezet.',
         '2dc7fe1dbf6192c2')]
KEYS = {row[1] for row in ROWS}
ACCENT_FRONT = {'calculation.module-picker': 'Het toevoegteken blijft vóór de modulecontour zichtbaar.'}
REUSED = {}
EXCLUDED = {}
DISPATCHERS = {}
DISPATCH_EVIDENCE = {}


def reuse(ids, key, reason):
    for rid in ids.split():
        REUSED[rid] = (key, reason)


def exclude(ids, reason):
    for rid in ids.split():
        EXCLUDED[rid] = reason


reuse('ff6aeec2181970a7 27a7a419fb679fae aeec77c5c0464f42 cc4284835a02ff34', 'file.open',
      'useBestandActies.openen kiest en leest een projectbestand, laadt het project en bewaart de recente verwijzing; Backstage is via activePanel=open bereikbaar en App bindt onBrowse aan openen.')
reuse('1fcc60f30e17670b bb67e54fef94a1ef', 'file.new',
      'nieuw controleert dirty en roept nieuwProject aan; lint en Bestand gebruiken dezelfde hook.')
reuse('41dec63fb1cc0e81 d8cdd8d1bf53426b', 'file.save',
      'opslaan schrijft het bestaande geldige pad; zonder geschikt pad volgt opslaanAls met bestandsdialoog.')
reuse('b6cc2f131903e183', 'file.save-as',
      'opslaanAls vraagt altijd een nieuwe bestemming via saveCalculationFile; markeert daarna het project als opgeslagen.')
reuse('9d6d82e9e13efb3e 98e261a3a11ad12f 0a6ab67facdb7ac1', 'edit.undo',
      'CalcTab bindt ongedaan aan projectStore en schakelt de knop uit bij lege geschiedenis.')
reuse('c99a8a60684e4173 1c486fa25103ce47 f7a79960b86b961c', 'edit.redo',
      'CalcTab bindt opnieuw aan projectStore en schakelt de knop uit zonder toekomststappen.')
reuse('40e6ba0555a658cc', 'calculation.module-picker',
      'Tweede bronwaarneming van dezelfde werkende openModuleKiezer-knop; ModuleKiezer.voegToe wordt pas bij bevestiging aangeroepen.')
reuse('15e13ac846dedda0 b6f36c4cca99b44d', 'view.report-preview',
      'handleVoorbeeld selecteert RAPPORT_ID en toonVoorbeeld(null, rapport); de gemonteerde rapportwerkruimte toont het afdrukvoorbeeld. Geen PDF-bestand schrijven.')
reuse('f6cab0fa8f389a9c 78e2582a005cd7e2', 'file.print',
      'PDF blad roept afdrukken([activeId], bladen) aan. App monteert PrintDocument, zet afdrukmodus en roept window.print aan; geen rechtstreekse PDF-export.')
reuse('1750426dc052f271 da13769381614c88 d0d7a8d55b765fa8 91c7ab448ba86c53', 'file.print',
      'PDF project en useAfdrukken gebruiken de rapport-/bladselectie uit printStore. App wacht op drukvellen en roept window.print aan; titelbalk en Bestand hebben werkende printcallbacks.')
reuse('65294e3b84bdef05 199191a544970db1', 'ui.dropdown',
      'De chevron zit in de trigger die het bestaande selectiemenu of themamenu open/dicht zet; geen navigatiepijl.')
reuse('067c2665e052de01 ef97a9e36de01cd8', 'ui.settings',
      'App bindt onSettingsClick aan setSettingsOpen(true); titelbalk en Bestand openen SettingsDialog.')
reuse('30c11523452f049c', 'window.minimize', 'Titelbalk roept de native minimize aan.')
reuse('66dc0d2a9e072614', 'window.restore', 'Deze tak wordt bij isMaximized getoond; toggleMaximize herstelt het venster.')
reuse('2beabe7b7bbf0174', 'window.maximize', 'Deze tak wordt bij niet-gemaximaliseerd venster getoond; ondanks cataloguslabel Herstellen is de werking maximaliseren.')
reuse('905ae4ba95d51780 301101a3f2afe4ed', 'window.close', 'Native venster sluiten vanuit titelbalk of Bestand.')
reuse('ef97a9e36de01cd8', 'ui.settings', 'Bestand opent de door App gebonden instellingenroute.')
reuse('b10d6d6ff2146080', 'ui.about', 'Bestand opent het Over-paneel.')
reuse('b3d3b471df0f1551', 'ui.close', 'De terugknop sluit alleen de Bestand-overlay via onClose.')
reuse('6060fb77797237b2 b198cc804cff7dac', 'link.open-external',
      'Werkende website- en GitHub-koppelingen uit Over; geen issueformulier publiceren of feedback verzenden.')
reuse('0a2450b10e7b491a', 'file.type-ifc', 'Recente lijst toont type ifc; inferType herkent ifc en ifcx. Geen importknop.')
reuse('fe22160e582263e8', 'report.document', 'Recente lijst toont type report; opslaan/openen registreert dit type, inferType herkent oaec en json.')
reuse('ed56694f423cd199', 'file.type-project', 'Recente lijst toont type project; inferType herkent oaecproj. Geen nieuw-projectactie.')
reuse('abee672ca594e502', 'file.type-other', 'Recente lijst toont de unknown-fallback voor overige bestandstypen.')
reuse('c56d5376f2d6df47', 'project.forget-recent',
      'removeRecentFile filtert de opgeslagen recente lijst en meldt de wijziging; het projectbestand blijft bestaan.')
DISPATCHERS['6db09078c94f81db'] = ('tree.expand', 'tree.collapse')
DISPATCH_EVIDENCE['6db09078c94f81db'] = (
    'TreeItem heeft eigen expanded-state en klapt alleen nodes met kinderen om. De rechterchevron is gesloten; CSS open draait hem omlaag. Het is geen IFC-type of volgende-pagina-opdracht.')

exclude('c41861a0d009e1bd 1caee6755dc6ba13 ac21882c13b07743',
        'Afbeelding heeft letterlijk een lege onClick; nog geen werkende invoegactie. Het oude betekenisconflict is hiermee expliciet beoordeeld, niet op de naam samengevoegd.')
exclude('c1109badbd8771a5 7754c214573a317a', 'Appbeeldmerk in titelbalk of Over; branding buiten de bedieningsiconen.')
exclude('c575ace37adeebcf b874070069e3778a 97b67478c073cd7f',
        'Titelbalk-snelknoppen Opslaan/Ongedaan/Opnieuw hebben geen onClick. De werkende lintknoppen zijn afzonderlijk beoordeeld.')
exclude('12f832f72902cc36 aea99604194ac0bf a899d740ed280b9e 51b74d43b8a3daa5',
        'Bestand Export opent slechts ExportPanel met drie niet-klikbare div-kaarten voor PDF/afbeelding/HTML. Geen gekoppelde uitvoerhandeling.')
exclude('80ffdabc11fc2007', 'ICONS.import is een ongebruikte definitie zonder menu-item in Backstage.')
exclude('5267f7f036e0e083 5dc22fd5a30bfe69 96873a36a25b8eb7 5a0c08ac7a09da4b fe4f00e8b38e21e1 391ce122631f2b94 d0051002e23a2195 7d58c5cf38d807d1 c936a96c1d69a408 6f284d947ec02d62 798e0995d2387e52 1bd4a9f045573b8e 3b69be95b80129fa 987c0e0debc4d45e 0e0286d7f0c26bbd 4b09e2b8b2915d93 e11df5d0628e2015 946760370ad70170 1a3afecb952dd1c8 3503733024c7b307',
        'Volledige git grep op de vastgelegde desktopcommit vindt alleen de calcIcons-definitie; geen import of UI-gebruik. IfcTab is bewust leeg; de huidige bestandsroute gebruikt Openen/Opslaan.')
exclude('dbe007392d4f3240',
        'spuwerWizard.icon is metadata die nergens gerenderd wordt: registry/host gebruiken inputs, id en Component. Het waterteken is geen bereikbare wizardkeuzeknop.')
exclude('620838908413e122', 'Renderer voegt door berekeningsinhoud geproduceerde SVG-fragmenten samen; dynamische model-/rapportinhoud, geen vast icoon.')
exclude('da8a738a5b3863c8 303e621da2c74dde ba5f51c23d6e14d8 360983b8bd62581c 1dc3abda6b984403 e28db6995645c0d7 25b42c782e32977f bbc4eebb812a3678 2e77e69e1e53c921 400d8eeb77fd803d 73a01a21d75532b6 63dac73c00bcfedd 033dea25a47673f3 54227fdf35a752d7 633d75685797ddf7',
        'Mechanica-tabellen bevatten belastingschemata bij berekende momenten, dwarskracht en doorbuiging; technische rapportillustraties, geen gereedschapsknoppen.')
exclude('3381d2c667e88cd5 44eb3b9c9ce65f80 e6a461634b07593d 0388a22f1745eb8f 7c774153e72e5312 39808df47e3a9953 54ae530559493bfb 27ed522c4228e84e 0b33da07e8eb18df',
        'Oude web-HTML-knoppen hebben geen handlers in de volledige src/main.ts. Alleen tabs, templates, paneelbreedte en data-view werken; deze bestands/media/IFC-knoppen blijven ongekoppeld.')
exclude('dc1fe2714bf6e234', 'Leaflet-locatiemarker op de windgebiedenkaart; geografische modelinhoud met kaartanker, geen vaste UI-knop.')


def extend(c, key):
    if key not in KEYS:
        return False
    for x, y in ((3, 3), (13, 3), (3, 13)):
        box(c, x, y, 7, 7)
    c.plus(18, 18, 4, True)
    return True
