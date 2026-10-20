"""PDF chrome, annotation menus and dialogs with explicit source-level decisions."""
from b2_second_series import box
from b2_bulk_series import page
from b2_reports_completion import glyph
from b2_font_geometry import font_sources
from b2_energy_pile_audio import arc_points

GROUPS = {110: 'Bestandslijsten en klemborddocumenten', 111: 'Productkenmerken en documentstatus', 112: 'Aangepaste kleurkeuze', 113: 'Contact en update-informatie'}
ROWS = [
 (110, 'document.from-clipboard-image', 'Document uit klembordafbeelding', 'De bitmap van het klembord lezen, een PDF op afbeeldingsmaat maken en de afbeelding als paginavullende annotatie plaatsen; geen nieuwe schermopname maken.', '8a586382d820f5a7'),
 (110, 'file.list-add', 'Bestanden aan lijst toevoegen', 'De PDF-bestandskeuze openen en unieke bestanden aan de samenvoeglijst toevoegen; nog geen PDF samenvoegen.', '90006a206a2b8972'),
 (110, 'list.move-up', 'Lijstitem omhoog', 'Het geselecteerde bestand één positie eerder in de samenvoeglijst zetten; geen objectstapel of laag wijzigen.', 'fd0910c0e8f6cc50'),
 (110, 'list.move-down', 'Lijstitem omlaag', 'Het geselecteerde bestand één positie later in de samenvoeglijst zetten.', '392e110b6df21a76'),
 (111, 'product.free', 'Gratis product', 'Vaste productkenmerkaanduiding Gratis in Over; geen prijs berekenen of betaalactie.', '66176493d1e5f087'),
 (111, 'product.open-source', 'Open broncode', 'Vaste productkenmerkaanduiding Open broncode in Over; geen bronbestand of repository direct openen.', '57bc97f76f50e06e'),
 (111, 'product.no-vendor-lock', 'Geen leveranciersbinding', 'Vaste productkenmerkaanduiding Geen vergrendeling in Over; geen object ontgrendelen of PDF-wachtwoord verwijderen.', '70c13805a0b12bd0'),
 (111, 'status.pdf-protected', 'Beveiligde PDF alleen-lezen', 'De balk meldt dat de geopende PDF wachtwoordbeveiligd en alleen-lezen is; de balk biedt geen ontgrendelactie.', 'd307ddcab79cb05d'),
 (111, 'status.signature-section', 'Digitale handtekeninginformatie', 'Aanduiding bij de handtekeningstatusbalk in alle toestanden; geldigheid, fout of controlevoortgang staan afzonderlijk in tekst en statusmarkeringen.', '1e796ff6294ba99b'),
 (112, 'format.custom-color', 'Aangepaste kleur kiezen', 'Meer kleuren opent de verborgen native kleurinvoer; de gekozen waarde gaat naar onColorChange of setValue. Geen tekstkleur-only-contract.', '3acb575b2ae7e6b0'),
 (113, 'contact.email', 'Contact per e-mail', 'Een mailto-contactadres openen; geen document bijvoegen of bericht automatisch verzenden.', '3b6366ad2f095ab9'),
 (113, 'status.update-available', 'Update beschikbaar', 'De updatebeschikbaarheid en versievergelijking in UpdateDialog aanduiden; deze illustratie start geen controle of installatie.', 'f41080a6fc64cf3b'),
]
KEYS = {row[1] for row in ROWS}
TYPOGRAPHY = {'product.free': {**font_sources()['format.color'], 'glyph': '0',
                             'purpose': 'Nul in de vaste productkenmerkaanduiding; Space Grotesk Medium.'}}
ACCENT_FRONT = {k: 'De bepalende pijl, markering of pen ligt zichtbaar vóór de dragende contour.' for k in KEYS}
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


def dispatch(ids, targets, reason):
    for rid in ids.split():
        DISPATCHERS[rid] = targets
        DISPATCH_EVIDENCE[rid] = reason


reuse('451504d5eec4a30b fe902388b751078a', 'file.open', 'Titelbalk kiest en opent via openPDFFile; Bestand opent het werkende OpenPanel met recente/browse-ingangen.')
reuse('b4ffba1d74cab9bb 1c5cfe72860005a2', 'file.save', 'savePDF schrijft het actieve saveTargetPath/bestaande pad; zonder bestemming volgt de dialoogroute. Geen save-as afdwingen.')
reuse('86ae264c22a5f7c8 b0c267e96b961c2e 2dfb40500080ebe2', 'file.save-as', 'savePDFAs vraagt een bestemming en bewaart het actieve document daar; de als Opslaan geregistreerde duplicaatwaarneming staat werkelijk op Save As.')
reuse('c07ef1d6f50c456f a580f6180c2476a1', 'file.print', 'showPrintDialog opent de gemonteerde desktopafdrukdialoog; webvariant is expliciet uitgesloten via isTauri/webfuncties.')
reuse('401666fda6efa345', 'export.raster-pdf', 'Alle documentpagina’s worden op 300 dpi gerasterd, als PDF bewaard en vervolgens in een nieuwe tab geopend via exportAsRasterPdf.')
reuse('d355ff4663ebdc3d 65b1a5c05451a7d1', 'ui.settings', 'showPreferencesDialog opent de algemene voorkeuren via dialogStore.')
reuse('c672e9fca541b978', 'edit.undo', 'undoEnabled volgt de actieve undoStack; de klik roept de werkende undo-manager aan.')
reuse('a19c350bb8867841', 'edit.redo', 'redoEnabled volgt de actieve redoStack; de klik roept de werkende undo-manager aan.')
reuse('1fdd065f250df312', 'window.minimize', 'De native minimizeWindow-route uit platform.js.')
reuse('9f355d9634356aa7', 'window.maximize', 'De geregistreerde SVG op regel193 is de niet-gemaximaliseerde tak. maximizeWindow schakelt native maximaliseren; de andere tak toont herstellen.')
reuse('ac3e2864b4693763 f5b7a9a06e00c24f', 'window.close', 'Titelbalk sluit tabs met wijzigingscontrole voor closeWindow. Bestand controleert niet-opgeslagen wijzigingen en bewaart readerposities vóór sluiten.')
reuse('eb74e16b70ddcfc8', 'file.new', 'showNewDocDialog opent de dialoog voor een nieuw leeg PDF-document; nog geen bestaande pagina invoegen.')
reuse('1d676bcd7d23af15', 'file.import', 'Bestand kiest het gemonteerde ImportPanel met concrete bestandsimporters; de menu-ingang zelf voert nog geen import uit.')
reuse('527b0a8b38dc4fd1', 'file.export-options', 'Bestand kiest het gemonteerde ExportPanel met uitvoerkeuzes; geen bestand onmiddellijk exporteren.')
reuse('6b92e5d70f2df634', 'ui.about', 'openDialog(about) opent AboutDialog.')
reuse('13bced4d5756dcca', 'ui.whats-new', 'openWhatsNewManual opent release-informatie via whats-new-store; externe diensten moeten beschikbaar zijn.')
reuse('4ae46113a56054ff', 'extensions.manage', 'openDialog(extensions) opent de gemonteerde extensiebeheerinterface; geen pakket direct installeren.')
reuse('8d306518e8c92d20', 'ui.close', 'Bestand-terug sluit alleen de app-menu-overlay via closeAppMenu.')
reuse('2fe86738769c1e20 4f60dfca27cc42d8', 'link.open-external', 'De Over-koppelingen openen de website of GitHub via platform.openExternal; geen issue publiceren.')
reuse('bccaa488c096436b', 'list.filter', 'Tonen biedt pagina- en statusfilters. toggleHiddenStatus werkt de lijst én canvaszichtbaarheid bij, laat verborgen selectie los en hertekent. Geen objecten verwijderen.')
reuse('ef44b84fad2e74fd', 'ui.more', 'De toolbar-menuknop zet menuOpen om en positioneert het annotatieactiemenu; geen panelennavigatie.')
reuse('47b4efcbf7f3f9b6', 'list.group-by', 'Submenu kiest sortMode; applySort vernieuwt de annotatielijst volgens het gekozen groeperingscriterium.')
dispatch('c8ef1825a4816510 4f1886cf329a9992 a5e9b61b53298af6 adfe8320ae5695fb', ('tree.expand', 'tree.collapse'),
         'Kleur- en overige groepskoppen roepen toggleGroup(groupKey) aan. De SVG kiest rechts/omlaag vanuit collapsedGroups; de geneste annotatierijen volgen dezelfde set.')
reuse('4a6ff5d7100918c9', 'edit.delete', 'removeFile verwijdert het geselecteerde item uit de samenvoeglijst; het bronbestand op schijf blijft bestaan.')
reuse('b9c6e8b1635afa31', 'file.type-other', 'Vaste generieke bestandsaanduiding naast een PDF in de samenvoeglijst; selectie gebeurt op de rij, geen nieuw document maken.')
reuse('a0a067a5def1f6c7', 'page.first', 'Afdrukvoorbeeld zet previewIndex op0 binnen de uitvoervellen; geen actieve documentpagina wijzigen.')
reuse('7a6fb826e6da9cbb', 'page.previous', 'prevPreview verlaagt de index van het afdrukvoorbeeld, begrensd op0.')
reuse('5644ef97788c96db', 'page.next', 'nextPreview verhoogt de index van het afdrukvoorbeeld, begrensd op voorbeeldTotaal-1.')
reuse('6b0f7cdc855508a4', 'page.last', 'Afdrukvoorbeeld zet previewIndex op voorbeeldTotaal-1; dit kan een vel met meerdere bronpagina’s zijn.')
reuse('6d13cba35d674ba7', 'format.bold', 'setBold schakelt fontBold voor de tekstinvoer/preview; handleOk geeft dit aan de aanroeper door.')
reuse('bf07aec89e578e7b', 'format.italic', 'setItalic schakelt fontItalic voor de tekstinvoer/preview; handleOk geeft dit door.')
reuse('2fb2e2341065ed29', 'format.align-left', 'setAlignValue(left) bepaalt textAlign voor preview en het teruggegeven tekstobject.')
reuse('803b7d10d610282c', 'format.align-center', 'setAlignValue(center) bepaalt textAlign voor preview en tekstobject.')
reuse('e2860df970d9b957', 'format.align-right', 'setAlignValue(right) bepaalt textAlign voor preview en tekstobject.')
reuse('5230fd5dc7ab4843 18313faad0165b86', 'ui.dropdown', 'De chevron zit in de kleurkeuzetrigger die de bestaande palette-dropdown open/dicht zet.')
reuse('c1f5186b40b69cd9', 'format.no-color', 'PrefColorPicker.selectNone zet noneChecked=true en sluit het menu; een kleur kiezen zet deze vlag weer false.')
reuse('2df50765c01aefca', 'format.custom-color', 'Meer kleuren opent de verborgen input type=color; input wijzigt setValue en heft noneChecked op.')
reuse('a53ee5e4ec89a0aa', 'status.warning', 'De bevestigingsdialoog toont een waarschuwing bij de expliciet aan de dialoog meegegeven vraag; bevestigen en annuleren blijven afzonderlijke knoppen.')
reuse('c40e6375bef8e613', 'status.error', 'FormValidationDialog toont een invoervalidatiefout met meegegeven bericht; de OK-knop sluit de dialoog.')
reuse('f0e57fdb3d2584c6', 'ui.close', 'De generieke Dialog-kop roept props.onClose aan; sluit deze dialoog, niet het native appvenster.')
reuse('602e32c1ba2b176c 1173cdd736199c71', 'status.info', 'Informatiebalk meldt aanwezige interactieve velden of dat de app nog niet de standaard PDF-app is; de icoonvorm is geen actieknop.')
reuse('0c27d7e5471162f3', 'status.warning', 'PDF/A-balk toont de alleen-lezen/bewerkwaarschuwing; de aparte enableEditing/dismiss-knoppen voeren de wijziging uit.')
reuse('1226d72d0450b6cd', 'panel.right', 'PanelHeader.onCollapse klapt het rechter eigenschappenpaneel dicht; geen boomtak invouwen.')
reuse('8186244d4afaeeba c42eea5c8065240c d33a9e485ccb580c', 'ui.dropdown', 'De eigen LanguageSelect, PrefComboBox en PrefSelect trigger schakelt hun concrete lijst; keuze en eventuele tekstinvoer blijven in het bestaande veld.')
reuse('3c17d1839b925964', 'workspace.ribbon-toggle', 'Ribbon.toggleCollapsed schakelt het lint tussen open en dicht; chevron volgt ribbonCollapsed, geen boomtak.')
reuse('600525fed76cb2c7', 'document.compare', 'De bestaande vergelijkingssessie heeft een eigen tab; de rij roept focusCompareTab aan en toont de vergelijking. Het beeld is geen tweede bestand openen.')
reuse('4837f167267b89d2', 'edit.delete', 'verwijderGebied verwijdert het gekozen OCR-labelgebied uit de configuratie en herberekent de labels; geen PDF-pagina wissen.')

exclude('991333aa7e9a41aa d2741f870c014d63 ed6cd72ad90a9ea6',
        'AnnotationsPanel: Samenvatten, Opmerkingen importeren en beide exportkeuzes hebben class disabled en geen callback. De oude conflicten zijn hiermee expliciet opgelost; geen werkende bron voor deze acties.')
exclude('89b8ec210856007b 68098cc741a51f9f', 'Titelbalk Vorige/Volgende weergave is permanent disabled zonder callback; geen navigatiegeschiedenisfunctie.')


exclude('41b98f725f9f07f1 06645ff48ba8ca78 893330a08606d795 3e93eb2fa63546ff ebedfad461980360 7a597b272a1438fd eff191a99ed16a46 87009ad7b27db91e f60d5bd89268a8e1 24dca809afc75071 a61c05686e64fde2 1801561fa7be26a3 6809f9c31ab5e850 a5a87ddef777955b 1fa6a70bbcff1d83 4ecd80174d8f524c 768f63bba267bf06 663f5e42c609b31e d358b4a2839b13c1 cb97b6610935a513 3c186d47a58c97d5 005beac7996e63c1 faadc4ade125b9d1 332421aab67a3691 cff46925b147029e 3a4e1d0c612ac7bf e19a84d4454befab f0769b46742cddf7 495721ae8f126d7a d38cca0cb109899c 3989776c4142a044 03544756bd721c6c 82595a64a6294b5f 626463205578ed49 4871c9941140a0be 722d7d7773d0b5cd 8c3b636a53fbd253 0b319ef56903f946 df1955badc97b12d ff0c4bfff3f46ae7 18fc12dd9acecf3c 4c9fe3e148f8b179 bd1a76d393a13431 e5fd6efb6e1d41bb d3753d2c7760e6e5 ae56bcca51df9c30 68be3cb96e3c123b 70520e28e36e0d39',
        'Meegeleverde PDF.js-standaardviewerinterface. Volledige gepinde grep vindt viewer.css alleen in vendor viewer.html; de eigen JS/index/styles gebruiken uitsluitend cmap/font/wasm-assets en de eigen Solid-interface. Geen bereikbare eigen-appbediening op basis van deze vendor-CSS.')


def extend(c, key):
    if key not in KEYS:
        return False
    if key == 'document.from-clipboard-image':
        page(c, 2, 4, 13, 18)
        box(c, 7, 2, 6, 4)
        c.line([(5, 17), (8, 13), (12, 17)], radius=.3)
        c.line([(17, 8), (22, 8), (22, 17), (17, 17)], True, radius=.4)
        c.line([(19, 14), (16, 17), (19, 20)], True, radius=.3)
    elif key == 'file.list-add':
        page(c, 2, 5, 12, 17)
        c.line([(5, 2), (17, 2), (17, 7)], radius=.4)
        c.plus(19, 17, 3, True)
    elif key in {'list.move-up', 'list.move-down'}:
        for y in (6, 12, 18):
            c.line([(3, y), (11, y)], radius=0)
        if key.endswith('up'):
            c.line([(18, 20), (18, 4), (14, 8)], True, radius=.3)
            c.line([(18, 4), (22, 8)], True, radius=.3)
        else:
            c.line([(18, 4), (18, 20), (14, 16)], True, radius=.3)
            c.line([(18, 20), (22, 16)], True, radius=.3)
    elif key == 'product.free':
        c.circle(12, 12, 9)
        glyph(c, '0', 8, 6, 8, 12, True)
    elif key == 'product.open-source':
        c.line([(7, 4), (2, 12), (7, 20)], radius=.4)
        c.line([(17, 4), (22, 12), (17, 20)], radius=.4)
        c.line([(14, 5), (10, 19)], True, radius=0)
    elif key == 'product.no-vendor-lock':
        page(c, 2, 3, 12, 18)
        c.line([(17, 12), (17, 8)] + arc_points(20, 8, 3, 180, 330, 20)[1:], True, radius=0)
        box(c, 15, 12, 8, 9, True)
    elif key == 'status.pdf-protected':
        page(c, 2, 3, 12, 18)
        box(c, 14, 13, 8, 8, True)
        c.line([(16, 13), (16, 10)] + arc_points(18, 10, 2, 180, 360, 20)[1:] + [(20, 13)], True, radius=0)
    elif key == 'status.signature-section':
        page(c, 2, 3, 18, 18)
        c.line([(6, 17), (10, 10), (9, 16), (14, 12), (15, 15), (19, 12)], True, radius=.3)
        c.line([(6, 19), (17, 19)], radius=0)
    elif key == 'format.custom-color':
        c.circle(10, 11, 8)
        for x, y in ((7, 7), (12, 6), (6, 12)):
            c.circle(x, y, .8, filled=True)
        c.line([(12, 16), (19, 9), (22, 12), (15, 19), (11, 20)], True, closed=True, radius=.3)
    elif key == 'contact.email':
        box(c, 2, 5, 20, 15)
        c.line([(3, 6), (12, 13), (21, 6)], True, radius=.4)
    elif key == 'status.update-available':
        c.line(arc_points(11, 13, 8, 0, 310, 48), radius=0)
        c.line([(11, 18), (11, 8), (7, 12)], True, radius=.3)
        c.line([(11, 8), (15, 12)], True, radius=.3)
        c.circle(20, 4, 2, True, filled=True)
    return True
