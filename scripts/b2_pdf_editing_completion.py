"""PDF context-menu and palette controls, including grid endpoint coupling."""
from b2_second_series import box
from b2_bulk_series import page
from b2_energy_pile_audio import arc_points

GROUPS = {114: 'Stramienuiteinden koppelen', 115: 'Annotatiekeuzes',
          116: 'Pagina’s op het klembord en in de volgorde', 117: 'Wolkpolylijn'}
ROWS = [
 (114, 'grid.end-couple', 'Stramienuiteinde koppelen', 'Het dichtstbijzijnde uiteinde terug in zijn stramiengroep koppelen; gekoppelde uiteinden schuiven daarna samen langs hun eigen lijn. Geen bewerkvergrendeling.', '99877d20db7ed53c'),
 (114, 'grid.end-decouple', 'Stramienuiteinde loszetten', 'Alleen het gekozen stramienuiteinde uit de koppeling loszetten; het blijft de groepsidentiteit bewaren voor later terugkoppelen.', '018c49b66c3db6b3'),
 (115, 'annotate.marked', 'Annotatie gemarkeerd', 'De marked-eigenschap van de gekozen annotatie omschakelen; geen tekstmarker of geaccepteerde reviewstatus.', '62ca81a35c472193'),
 (115, 'annotate.status-options', 'Reviewstatus kiezen', 'Het statuskeuzemenu voor annotation.status openen; de gekozen optie wijzigt het object, niet het zichtbaarheidfilter.', 'ad34938d260ac8a1'),
 (115, 'object.arrange-options', 'Schikopties openen', 'Het annotatiemenu met stapelvolgorde, rotatie, spiegelen en dupliceren tonen; nog geen geometrie wijzigen.', 'b73b21d33b316bc9'),
 (115, 'nav.page-menu', 'Paginanavigatiemenu', 'Het submenu voor eerste/laatste/vorige/volgende documentpagina openen; geen benoemde bestemming kiezen.', '21391d8bb419f18c'),
 (116, 'page.cut', 'Pagina’s knippen', 'Gekozen PDF-pagina’s als zelfstandige PDF-bytes op het interne paginaklembord zetten en uit het document verwijderen, mits minstens één pagina overblijft.', '12d8d3080f9de6a7'),
 (116, 'page.copy', 'Pagina’s kopiëren', 'De gekozen PDF-pagina’s als zelfstandige PDF-bytes op het interne paginaklembord zetten; bronpagina’s behouden.', 'b198c2711684f36d'),
 (116, 'page.paste', 'Pagina’s plakken', 'De pagina’s uit het interne paginaklembord ná de doelpagina invoegen; geen annotaties op het canvas plakken.', 'a3ecab1309793dc2'),
 (116, 'page.replace', 'Pagina uit bestand vervangen', 'Een vervangende PDF kiezen en de doelpagina door alle pagina’s uit dat bestand vervangen via replacePages; geen achtergrondafbeelding omwisselen.', '0847cc99f8b2bd1c'),
 (116, 'page.move-up', 'Pagina één plaats eerder', 'De miniatuurpagina met haar voorganger verwisselen via een volledige reorderPages-permutatie; het PDF-document wordt aangepast.', 'a56a86378084aa80'),
 (116, 'page.move-down', 'Pagina één plaats later', 'De miniatuurpagina met haar opvolger verwisselen via reorderPages; geen laag of lijstverwijzing herschikken.', '51d28cf708297edb'),
 (116, 'page.insert-file', 'Pagina’s uit bestand invoegen', 'Een PDF kiezen en pagina’s vóór of ná de doelpagina invoegen; de bijbehorende menukeuze bepaalt de positie.', '2cb1c49c7452a77d'),
 (117, 'draw.cloud-polyline', 'Wolkpolylijn tekenen', 'Het geregistreerde cloudPolyline-gereedschap activeren voor een polylijn met wolkcontour. De gebruiker kan het pad bij het startpunt sluiten.', '21b50b9b45eece05'),
]
KEYS = {row[1] for row in ROWS}
ACCENT_FRONT = {k: 'De bepalende verbinding, pijl of eindpuntmarkering ligt vóór de achterliggende contour.' for k in KEYS}
REUSED = {}
EXCLUDED = {}
DISPATCHERS = {}
DISPATCH_EVIDENCE = {}


def reuse(ids, key, reason):
    for rid in ids.split(): REUSED[rid] = (key, reason)


def exclude(ids, reason):
    for rid in ids.split(): EXCLUDED[rid] = reason


def dispatch(ids, keys, reason):
    for rid in ids.split():
        DISPATCHERS[rid] = keys
        DISPATCH_EVIDENCE[rid] = reason


reuse('a054bf41568966b9 dea2d98b7b91153e', 'edit.cut', 'Knippen kopieert de selectie, breidt zo nodig een vervangingsgroep uit en verwijdert die met undo; geen PDF-pagina’s knippen.')
reuse('8a032339e01da3de 2b94df0108cd0155 0e6d12749b512733', 'edit.copy', 'Enkel-/meervoudige annotaties kopiëren; het tekstselectiemenu schrijft geselecteerde tekst naar het systeemklembord. Concrete inhoud staat in de context.')
reuse('89d2a1ff805960c0 948d8aa977e92af5', 'edit.paste', 'Beide menu’s roepen pasteFromClipboard voor annotaties/klembordinhoud aan, geen interne PDF-paginaplakactie.')
reuse('ccc986501aab8324 e303d70c059ad279', 'edit.paste-in-place', 'pasteAnnotationsInPlace behoudt de oorspronkelijke annotatiecoördinaten.')
reuse('6de8c9e3a3183f02 549930f657464d7f b32782c76adf89af', 'edit.delete', 'Het contextueel gekozen punt of de annotatieselectie verwijderen. Annotatie-/vervangingsgroepen gaan met undo en eventuele bevestiging; geen PDF-pagina verwijderen.')
dispatch('244f4b5f77de57e2', ('object.lock', 'object.unlock'), 'Checkboxmenu schakelt ann.locked. De twee iconen beelden de huidige toestand uit; de klik wisselt die om. Adapter moet de toestand/checkbox bewaren, geen losse vaste actie op basis van het asset kiezen.')
reuse('6f0507eb4a67ae47', 'list.filter', 'Tonen op status schakelt hiddenStatuses; dezelfde store als het annotatielijstfilter hertekent ook het canvas. annotation.status blijft behouden.')
reuse('cd3574894d9d2e8c', 'layer.assign-selection', 'LayerSubmenu kiest de markeringslaag en roept moveAnnotationsToAnnotationLayer aan voor de huidige selectie; geen lagenbeheer openen.')
reuse('ff6cfe9ffee35214', 'style.tools', 'Het menu biedt de stijl van de annotatie als standaard bewaren of de standaard toepassen; geen directe format-painteractie.')
reuse('3d68dbeae207029f', 'file.export-options', 'Het annotatie-exportsubmenu openen. Pas de onderliggende keuze roept exportAnnotationAsImage aan; nog geen uitvoerbestand schrijven.')
reuse('76939e82ebf33260', 'object.properties', 'showProperties toont de geselecteerde annotatie.')
reuse('f722290bdbe21038', 'document.properties', 'De als page.propertiesMenu gelabelde canvasopdracht opent werkelijk doc-properties; geen afzonderlijke pagina-eigenschappen.')
reuse('7c1da4b0e63ee44f', 'object.properties', 'De als Transformeren gelabelde opdracht roept uitsluitend showProperties(ann()) aan; er wordt geen transformatie uitgevoerd.')
reuse('469bf01bd07a7c8c', 'bookmark.add', 'addBookmarkAtCurrentPage voegt een bladwijzer bij de huidige documentpagina toe.')
reuse('65bbd08c525d3382 9cf8e2ac3622c03d', 'view.pan', 'setTool(hand) activeert het geregistreerde handgereedschap met echte panhandlers.')
reuse('208026e879fb81ea 1f09a1008f76c082', 'edit.select', 'Ondanks de oude variabelenaam selectAllIcon zet deze contextmenu-ingang alleen setTool(select). Het palet kiest dezelfde geregistreerde objectselectie, geen alles-selecteren.')
reuse('d961042ef977952e', 'edit.deselect', 'clearSelection wist alleen de annotatieselectie.')
reuse('017462b0545b0b9d', 'file.print', 'De desktopcontext opent de bestaande printdialoog via dialogStore.')
reuse('8a6606d7cc29c8e2', 'object.bring-front', 'bringToFront plaatst de annotatie vóór alle andere annotaties.')
reuse('4da3ec9be3f6374b', 'object.send-back', 'sendToBack plaatst de annotatie achteraan in de tekenvolgorde.')
reuse('c25d6c9d41ffd663', 'object.bring-forward', 'bringForward verplaatst één stap in de tekenvolgorde.')
reuse('9a7802b0a16ddabb', 'object.send-backward', 'sendBackward verplaatst één stap achteruit in de tekenvolgorde.')
reuse('f18156842f43d217 26303996a2b1c2c6', 'transform.mirror', 'De gekozen annotatie/selectie horizontaal spiegelen via flipHorizontal; undo wordt geregistreerd.')
reuse('ef825b817f81b851', 'transform.flip-vertical', 'flipVertical spiegelt de annotatie verticaal en recordModify bewaart undo.')
dispatch('2cb1c49c7452a77d', ('page.insert', 'page.insert-file'), 'Dezelfde thumbnailInsertIcon bedient zowel de lege-paginadialoog als het submenu voor PDF-bestand vóór/ná invoegen. Concrete callback bepaalt het contract.')
reuse('7b2e28619ddf01b7', 'page.extract', 'Het extractiedialoog krijgt de concrete geselecteerde paginareeks en doelpagina mee.')
reuse('f3b710da2559f973', 'page.delete', 'Het verwijderdialoog krijgt de concrete geselecteerde PDF-paginareeks mee; geen annotaties wissen.')
reuse('1efd786828a95ff5', 'page.rotate-left', 'draaiPaginas(-90,pages()) draait de geselecteerde PDF-pagina’s met de echte paginabewerking.')
reuse('188ae263225c72ad', 'page.rotate-right', 'draaiPaginas(90,pages()) draait de geselecteerde PDF-pagina’s rechtsom.')
reuse('c0a3a824ccf4b776', 'edit.select-all', 'selectAllPages selecteert alle pagina’s in de miniaturencontext; geen canvasobjecten selecteren.')
reuse('ca66976f9e55c95d', 'annotate.highlight', 'Palet -> ToolBtn -> setTool(highlight), geregistreerd shapegereedschap.')
reuse('5ee51e3fc979f74e', 'draw.freehand', 'Palet activeert draw, geregistreerd met drawTool.')
reuse('56d4d80888dc42c2', 'draw.line', 'Palet activeert line, geregistreerd met lineTool.')
reuse('0560b285350024fc', 'draw.arrow', 'Palet activeert arrow, geregistreerd met lineTool in pijlmodus.')
reuse('f6dabff182745b21', 'draw.polyline', 'Palet activeert de geregistreerde polylineTool.')
reuse('5637bfe51b7a2fed', 'draw.rectangle', 'Palet activeert box, geregistreerd met shapeTool.')
reuse('89a90a11ef2a04dd', 'draw.circle', 'Ondanks de variabelenaam ellipseIcon activeert deze paletknop circle; de twee broncontracten blijven apart.')
reuse('e035a908af897549', 'draw.cloud', 'Palet activeert cloud, de gesloten vormvariant van shapeTool.')
reuse('c6535647a28da4f7', 'draw.textbox', 'Palet activeert textbox, geregistreerd met shapeTool.')
reuse('2df51b8d7b7ed668', 'draw.note', 'Palet activeert comment, geregistreerd met commentTool.')
reuse('0d4f8485b85dac65', 'draw.leader', 'Palet activeert callout, geregistreerd met shapeTool.')
reuse('508d11f9d86b24f5', 'annotate.stamp', 'Palet activeert stamp, geregistreerd met stampTool.')
reuse('3fee64e0f3c05f9e', 'annotate.signature', 'Palet activeert signature, geregistreerd met signatureTool; geen digitale verificatie.')
reuse('b33a9e5582df03f7', 'measure.distance', 'Palet activeert de geregistreerde measureDistanceTool.')
reuse('d563af11397e811f', 'measure.area', 'Palet activeert de geregistreerde measureAreaTool.')
reuse('4d4f491ec80427de', 'measure.perimeter', 'Palet activeert de geregistreerde measurePerimeterTool.')
reuse('d6558005aec9a55a bc7d9afbf2423a3f', 'content.drag', 'De sleepgreep roept startDrag/startExtDrag aan voor paletverplaatsing, inclusief docking-preview en opgeslagen positie.')
reuse('f8acebc6a54204a7', 'ui.more', 'De als Settings benoemde knop opent alleen het contextmenu Small Icons/Large Icons; geen algemene appvoorkeuren.')
reuse('e7b97ed66ab88c9b ed76ef7661da0553 43847958b01e053b e59cfa883ea6d9b1', 'ui.close', 'Palet sluiten zet visible=false en bewaart de voorkeuren. Het oude label Palet losmaken bij e59 is onjuist: de SVG staat in de zwevende sluitknop, niet in een losmaakopdracht.')
reuse('781133779be11686', 'workspace.dock-left', 'Passieve linker sleepdoelaanduiding tijdens paletdrag; loslaten met dockPreview=left zet het palet links vast.')
reuse('a6862d7457c5f977', 'workspace.dock-right', 'Passieve rechter sleepdoelaanduiding tijdens paletdrag; loslaten met dockPreview=right zet het palet rechts vast.')
reuse('1665ef926a8340a5', 'object.align-left', 'ArrangeTab roept alignLeft voor de selectie aan; geen tekstuitlijning.')
reuse('ffd34fb3873dca3f', 'object.align-center', 'ArrangeTab roept alignCenter voor de selectie aan.')
reuse('a23b75d6db18f40f', 'object.align-right', 'ArrangeTab roept alignRight voor de selectie aan.')
reuse('99a5942975a19def', 'object.rotate-right-90', 'De gelezen callback draait alle geselecteerde annotaties 90 graden en registreert recordBulkModify; de oude vernieuwen-verdenking is hiermee opgelost.')
reuse('f64b292e3ba4b633 88d6ca5dd3b4e743 e5a427328cfe7ff3 db4b7cef1d4961a0 6b1496dbe409e2fc', 'ui.dropdown', 'De chevron opent respectievelijk uitlijnreferentie, splitbuttonmenu, kleurkeuze, thema of de overloop. Elke trigger heeft eigen open-state en echte keuzerijen.')
reuse('6ef2921b98234d72 5504999578341259', 'ui.more', 'Meer groepen/tabs opent de flyout met buiten beeld geraakte lintgroepen of extensietabs; geen nieuwe functie direct uitvoeren.')
reuse('26be92821e1c5a6f', 'format.align-left', 'ParagraphSection wijzigt textAlign=left via updateAnnotProp en bewaart de bestaande vergrendelingscontrole.')
reuse('e387660a7dc43f8f', 'format.align-center', 'ParagraphSection wijzigt textAlign=center via updateAnnotProp.')
reuse('76d2789f407370bc', 'format.align-right', 'ParagraphSection wijzigt textAlign=right via updateAnnotProp.')
reuse('af3bdc301ddd7d09', 'ui.close', 'De zoekbalk sluiten via closeFindBar en de findBarStore; dit is de werkende moderne route.')

exclude('699ea716b48aaf4d 6937ecf3abf40647 94bf1261a266cbcd', 'Contextmenu op paginavlak: Cut/Copy/Delete zijn letterlijk disabled=true zonder handler. De werkende miniatuurpagina-acties hebben eigen bronrecords en ontwerpen.')
exclude('18695417aa9a9a5d 2a8ef385de25c748 a6dedcc496bb09de bcba3c77347357aa bc51cb10ad02cc5e', 'Oude paginacontext zet image/qrCode/snapshot/selectText/zoom als currentTool, maar geen van deze namen is geregistreerd in tools/index.js of de ingebouwde pluginregistratie. Dispatcher heeft daardoor geen handler. Huidige beeldinvoer, screenshot en tekstselectie hebben elders eigen werkende routes.')
exclude('32e2654cbb02e9da 6465afdee1942d9d', 'Oude contextzoekknoppen gebruiken getElementById(find-bar/find-input). De gemonteerde FindBar heeft alleen classes en refs, geen van beide IDs; er wordt niets geopend. De moderne zoekroute is afzonderlijk beoordeeld.')


def extend(c, key):
    if key not in KEYS: return False
    if key.startswith('grid.end-'):
        apart = key.endswith('decouple')
        for x, y in ((6, 6), (17, 11 if apart else 6)):
            c.circle(x, y, 2.5)
            c.line([(x, y+3), (x, 22)], radius=0)
        if apart:
            c.line([(6, 6), (11, 6)], True, radius=0)
            c.line([(12, 11), (17, 11)], True, radius=0)
        else: c.line([(6, 6), (17, 6)], True, radius=0)
    elif key == 'annotate.marked':
        c.line([(5, 2), (5, 22)], radius=0)
        c.line([(5, 3), (21, 3), (17, 8), (21, 13), (5, 13)], True, closed=True, radius=.3)
    elif key == 'annotate.status-options':
        page(c, 3, 3, 18, 18)
        for y in (8, 13, 18):
            c.circle(8, y, 1, True, filled=True)
            c.line([(12, y), (17, y)], radius=0)
    elif key == 'object.arrange-options':
        box(c, 2, 2, 10, 10)
        box(c, 7, 7, 10, 10)
        box(c, 12, 12, 10, 10, True)
    elif key == 'nav.page-menu':
        page(c, 2, 3, 13, 18)
        c.line([(18, 8), (22, 12), (18, 16)], True, radius=.3)
    elif key == 'page.cut':
        page(c, 2, 2, 12, 20)
        for x in (17, 21): c.circle(x, 19, 1.5, True)
        c.line([(17, 17), (23, 7)], True, radius=0)
        c.line([(21, 17), (16, 7)], True, radius=0)
    elif key == 'page.copy':
        page(c, 8, 2, 13, 16)
        page(c, 3, 7, 13, 15, True)
    elif key == 'page.paste':
        box(c, 2, 4, 14, 17)
        box(c, 6, 2, 6, 4)
        page(c, 10, 10, 12, 12, True)
    elif key == 'page.replace':
        page(c, 2, 3, 9, 18)
        page(c, 14, 3, 8, 18)
        c.line([(7, 10), (19, 10), (16, 7)], True, radius=.3)
        c.line([(17, 16), (5, 16), (8, 19)], True, radius=.3)
    elif key in {'page.move-up', 'page.move-down'}:
        page(c, 2, 3, 12, 18)
        if key.endswith('up'):
            c.line([(20, 21), (20, 4), (17, 7)], True, radius=.3)
            c.line([(20, 4), (23, 7)], True, radius=.3)
        else:
            c.line([(20, 4), (20, 21), (17, 18)], True, radius=.3)
            c.line([(20, 21), (23, 18)], True, radius=.3)
    elif key == 'page.insert-file':
        page(c, 2, 3, 12, 18)
        c.line([(23, 12), (10, 12), (14, 8)], True, radius=.3)
        c.line([(10, 12), (14, 16)], True, radius=.3)
    elif key == 'draw.cloud-polyline':
        pts = []
        for x in (5, 11, 17):
            arc = arc_points(x, 14, 3, 180, 360, 20)
            pts.extend(arc if not pts else arc[1:])
        c.line(pts, radius=0)
        for x in (2, 20): c.circle(x, 14, 1.5, True, filled=True)
    return True
