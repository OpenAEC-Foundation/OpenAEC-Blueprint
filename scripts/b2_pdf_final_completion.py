"""Remaining PDF controls: panel navigation, preferences, files and native editing."""
import math
from b2_second_series import box
from b2_bulk_series import page
from b2_reports_completion import glyph
from b2_font_geometry import font_sources
from b2_energy_pile_audio import arc_points

GROUPS = {118:'PDF-inhoud bewerken',119:'PDF-zijpanelen',120:'PDF-instellingen',
          121:'Bestandsbronnen en sessies',122:'Symbool- en tekeninstellingen',
          123:'Extensiepakketten onderhouden',124:'Koppelingen en handtekeningen',125:'Versies, diagnostiek en uitwisseling'}
ROWS = [
 (118,'draw.filled-area','Gevuld vlak tekenen','Het geregistreerde filledArea-gereedschap activeren voor een contour met rechte/gebogen randen en eventuele gaten; geen gewone rechthoek tekenen.','ae62cfd38d8bc80b'),
 (118,'image.embedded-edit','Ingebedde afbeelding bewerken','Een raster-XObject in PDF-paginainhoud kiezen en daarna verplaatsen, schalen, vervangen of verwijderen. De toolnaam removeImage is historisch; geen directe verwijderactie of afbeeldingsannotatie.','92144aca8d87de21'),
 (118,'transform.length-axis','Lijnlengte aanpassen','Eerst een lijn en het dichtstbijzijnde uiteinde kiezen, daarna de tweede klik op de eigen lijnas projecteren en dat uiteinde verplaatsen. Groeien en krimpen zijn mogelijk; geen verlengen tot een andere lijn.','3a26991f069be001'),
 (119,'panel.thumbnails','Paginaminiaturen','Het miniaturenpaneel openen en verversen; nog geen paginavolgorde wijzigen.','aebdbdaa9329a900'),
 (119,'panel.bookmarks','Bladwijzerpaneel','Het paneel met bestaande bladwijzers openen; geen nieuwe bladwijzer toevoegen.','0006e8097006f9a7'),
 (119,'panel.attachments','Bijlagenpaneel','Het paneel met PDF-bijlagen openen; nog geen bestand exporteren of toevoegen.','2ed1d48602bc477b'),
 (119,'panel.signatures','Handtekeningenpaneel','Het paneel met handtekeninggegevens openen; de afzonderlijke statussen bepalen geldigheid of onbekendheid.','6f2872b77e6e9bf7'),
 (119,'panel.form-fields','Formulierveldenpaneel','Het paneel met bestaande interactieve formuliervelden openen; geen nieuw veld maken.','c97c5839e004ab18'),
 (119,'panel.destinations','Bestemmingenpaneel','Het paneel met benoemde PDF-bestemmingen openen; een bestemming pas na rijselectie volgen.','e035cacbfc9b6b11'),
 (119,'panel.tags','Structuurtagpaneel','Het paneel met de PDF-structuurtags openen; geen label aan een annotatie toevoegen.','6c18221f30b68aa6'),
 (119,'panel.links','Koppelingenpaneel','Het paneel met interne en externe PDF-koppelingen openen; nog geen URL volgen.','3303d097851fabe9'),
 (119,'panel.measurements','Meetannotatiespaneel','Het paneel met bestaande meetannotaties openen; geen nieuwe afstandsmeting starten.','b68dbdbd3cf67882'),
 (119,'panel.schedules','Hoeveelhedenstatenpaneel','Het paneel met opgeslagen hoeveelhedenstaten openen; nog geen nieuwe staat plaatsen.','6100ecbddaceaf62'),
 (120,'preferences.annotations','Annotatievoorkeuren','De voorkeurencategorie voor annotatiestandaarden kiezen; geen annotatiepaneel of tekenmodus.','b6e9f64760efef40'),
 (120,'preferences.behavior','Gedragsvoorkeuren','De voorkeurencategorie voor opstarten, verwijderen en interactiegedrag kiezen.','a9822917176c3c51'),
 (120,'preferences.page-display','Paginaweergavevoorkeuren','De voorkeurencategorie voor standaard paginaweergave kiezen; geen huidige pagina onmiddellijk omschakelen.','76fa7f634db56688'),
 (120,'printer.virtual-settings','Virtuele printer instellen','De categorie voor installatie en opvangmodus van de virtuele printer openen; nog geen installatie of afdrukopdracht uitvoeren.','49d81a15f7d23134'),
 (121,'recent.pin-toggle','Recent bestand vastzetten','De pinned-status van de recente bestandsverwijzing omschakelen via pinRecentFile/unpinRecentFile; het PDF-bestand wordt niet bewerkvergrendeld.','a89a5615ace89142'),
 (121,'session.restore','Opgeslagen sessie herstellen','De gekozen sessie herstellen via restoreSession; geen sessieoverzicht of nieuw leeg document openen.','6d3f9c7a2614d1b7'),
 (121,'file.place-add','Maplocatie toevoegen','Een bestaande map kiezen en als opgeslagen locatieverwijzing toevoegen; geen nieuwe map op schijf maken.','f74e2aa751a960fe'),
 (121,'file.places','Opgeslagen maplocaties','Het paneel met opgeslagen maplocaties openen; pas een mapkeuze leest de PDF-bestandenlijst.','a4c6d4bed46a44b1'),
 (121,'file.host-library','Documenten van de site','De door de host aangeboden documentenlijst openen/vernieuwen; geen specifieke clouddienst of lokaal bestand veronderstellen.','0e1ba13c950e6007'),
 (122,'symbol.library-settings','Symboolbibliotheek instellen','De eigen bibliotheekinstellingen openen voor beschikbare categorieën, landen en eigen groepen.','9173e37b2a381b16'),
 (122,'drawing.settings','Tekeninstellingen','Het tekeninstellingendialoog openen vanuit NL IFC Bouw; geen algemene appvoorkeuren.','9173e37b2a381b16'),
 (122,'symbol.system-types','Systeemtypen beheren','Het dialoog systeemtypen openen voor onder meer systeemraster/plafondtypen; geen nieuw type direct toevoegen.','fb93b6b132734f6f'),
 (123,'extension.reinstall-file','Extensie uit bestand vervangen','Een oppx-pakket kiezen om een bestaande extensie opnieuw te installeren; de levenscyclus kan naar de vorige versie terugrollen bij activeringsfouten.','75a05038339ebace'),
 (123,'extension.uninstall','Extensie verwijderen','Na bevestiging de gekozen extensie uitschakelen, opruimen en van schijf verwijderen via de levenscyclus; geen documentobject wissen.','02df546959b0e9c3'),
 (124,'link.open-internal','Interne documentkoppeling','Aanduiding bij een interne PDF-koppeling; de rij selecteert de koppeling en dubbelklik volgt haar interne bestemming.','a330c71ed8472986'),
 (124,'signature.status-unknown','Handtekeningstatus onbekend','De fallback bij een handtekeningstatus die noch valid noch invalid is; geen geldigheidsclaim.','4f69e2c3be9eb10f'),
 (124,'annotate.tools-menu','Annotatiegereedschappen','Het mobiele menu met de vijf ondersteunde annotatie-/selectiegereedschappen openen; nog geen gereedschap direct activeren.','82d19ce7c55a8ba3'),
 (125,'update.previous-download','Vorige versie downloaden','De voorgaande gepubliceerde versie bepalen en de passende download in de browser openen. De app installeert niets stil.','9575c5d275cccb43'),
 (125,'diagnostics.startup-log','Opstartdiagnostiek tonen','Het pad van de opstartdiagnostiek opvragen en in de bestandsbeheerder tonen; geen logbestand versturen.','798edea0b9d21ca3'),
 (125,'bcf.import','BCF-issues invoeren','Een BCF ZIP kiezen, parsen en de herkende annotaties aan het actieve PDF-document toevoegen met undo; geen IFC-model importeren.','3c365ad66eca6d7c'),
]
KEYS = {r[1] for r in ROWS}
SEMANTIC = {'signature.status-unknown':'text-secondary'}
TYPOGRAPHY = {'signature.status-unknown':{**font_sources()['format.color'],'glyph':'?',
    'purpose':'Vraagtekencontour voor onbekende handtekeningstatus; Space Grotesk Medium.'}}
ACCENT_FRONT = {k:'Het bepalende teken blijft vóór de dragende contour zichtbaar.' for k in KEYS if k not in SEMANTIC}
REUSED = {}; EXCLUDED = {}; DISPATCHERS = {}; DISPATCH_EVIDENCE = {}

def reuse(ids,key,reason):
    for rid in ids.split(): REUSED[rid]=(key,reason)

def exclude(ids,reason):
    for rid in ids.split(): EXCLUDED[rid]=reason

def dispatch(ids,targets,reason):
    for rid in ids.split():
        DISPATCHERS[rid]=targets; DISPATCH_EVIDENCE[rid]=reason

reuse('f055a91e2c7b93f3','file.new','De Home-knop opent showNewDocDialog; geen bestandskeuze voor een bestaand document.')
reuse('9a31b3537452cd4d 84ba676e133c26ef 6af10ac93aa00020 a31db9ac60837271','ui.close','De lokale symbooleditor/hoeveelhedeneigenschappen/staat/wizard sluiten via hun eigen state of cancelSymbolTypeEdit; geen native venster sluiten.')
reuse('6adf64090530ed5b','nav.go-to','De bestemmingsrij roept navigateToDestination(dest.name) aan voor de bestaande benoemde bestemming.')
reuse('eba8893b6b183cd0 70ecf25578ff1018','content.drag','De echte dragstart van staat of palet gebruiken; de grip is geen nieuw-itemknop.')
reuse('987e683e6a8ee6f5 8342a11466a18ac3 67090a4d4ebc19ca b1d4ad86881047cc','file.type-other','Generieke bestandsaanduiding naast een bijlage, recent/site-document of PDF uit een maplocatie. De omringende rij heeft de concrete open-/downloadroute.')
reuse('aef0480c1602b40e','link.open-external','Externe koppeling in LinksPanel; dubbelklik roept navigateToLink voor de URL aan, enkele klik selecteert/markeert haar eerst.')
reuse('f8ff9fe1d88136dd','status.error','SignatureIcon kiest deze tak uitsluitend bij status=invalid; detailtekst bepaalt de concrete fout.')
reuse('abc530f45248c1a3','status.success','SignatureIcon kiest deze tak uitsluitend bij status=valid; geen gebruik als ondertekenactie.')
reuse('e8dc169df3b4b303 58f79b5b1cdd89a3 7e3a29b0ce58d4db','file.open','Mobiel kiest via native dialoog of bestandsinput en laadt PDF-bytes; desktop Browse roept openPDFFile aan.')
reuse('3dd38b9642ca1ed1','workspace.toolbar-toggle','handleToggleCollapse bedient de onderste mobiele werkbalk.')
reuse('a3133820d15dde78','page.previous','handlePrevPage gaat naar de vorige documentpagina; RTL bepaalt welke pijl/callback zichtbaar is.')
reuse('3179407a5b43ef77','page.next','handleNextPage gaat naar de volgende documentpagina; RTL blijft in de app.')
reuse('f3566e81cbd71bb7','view.zoom-out','Mobiele zoomfactor delen door1.25 met ondergrens0.25.')
reuse('d9816ade1c705007','view.zoom-in','Mobiele zoomfactor vermenigvuldigen met1.25 met bovengrens5.')
reuse('14b6f8f9ea85f134','page.rotate-right','handleRotate roept draaiVanafKnop(90) aan; werkelijke paginabewerking, geen tijdelijke weergaverotatie.')
reuse('75b4713b9c256c9d','edit.copy','De mobiele kopieerknop schrijft de geselecteerde PDF-tekst naar het klembord.')
reuse('bd79d53e1397c060 170aaecb92402711 f2d96035b5f7977f','ui.close','Mobiele lade/voorkeuren of symboolpalet/bibliotheekinstellingen sluiten; eigen state bepaalt de lokale scope.')
reuse('d4df7ba9fbfc57cb','file.save','Mobiel roept savePDF rechtstreeks aan; de bestandsdialoog/Android-URI-route blijft bij de saver.')
reuse('0a1bd40993e4b94f','file.save-as','Mobiel roept savePDFAs rechtstreeks aan en kiest een bestemming.')
reuse('7618c2e74dc3eb8a 1b8ab0a57e0ed71b','ui.settings','Mobiel opent de echte voorkeuren; desktop kiest General in het gemonteerde PreferencesDialog.')
reuse('3a17c64565597b41','ui.feedback','handleFeedback opent het feedbackdialoog; nog geen feedback versturen. Host-/webbeperkingen volgen knopUit.')
reuse('f505c443588dd875','ui.about','De mobiele Over-knop opent het gemonteerde AboutDialog via dialogStore.')
reuse('3e337bf96cb0ad1d','edit.select','ToolIcon-variant select hoort bij MOBIELE_GEREEDSCHAPPEN.select en directe setTool(select).')
reuse('66da0de813c716db','annotate.highlight','ToolIcon-variant highlight kiest het geregistreerde markeergereedschap.')
reuse('8e25c76b565773ca','draw.freehand','ToolIcon-variant draw kiest het geregistreerde vrijehandgereedschap.')
reuse('991f7fa419ddbfbb','draw.textbox','ToolIcon-variant textbox kiest het geregistreerde tekstvakgereedschap.')
reuse('0b2bd240b3ccb40a','draw.note','ToolIcon-variant comment kiest het geregistreerde commentTool.')
reuse('56ecbe88f6a6313e','project.forget-recent','removeRecentFile verwijdert alleen de recente verwijzing en ververst de lijst; geen bestand op schijf wissen.')
reuse('e4fc925b8c04a987 976f02e0c15360b9','view.search','Recente lijst of symboolbibliotheek filtert met eigen searchQuery; geen documenttekst zoeken.')
dispatch('14775887d71f2656 7f87010632d07513 42da3b593d805889',('tree.expand','tree.collapse'),'Vastgezette/overige recente groepen en symboolcategorieën klappen hun eigen geneste lijst om; chevron volgt de bestaande collapsed-/expanded-state.')
reuse('5245b53abb1873d5 4dbea5ecaf706cf1','edit.delete','De gekozen opgeslagen sessie of maplocatieverwijzing uit de eigen opslag verwijderen; onderliggende PDF-bestanden blijven behouden.')
reuse('64608e9d2f043341','project.folder','Een bestaande maplocatie uitklappen en listPdfFiles(path) lezen; geen map aanmaken.')
reuse('570759ef3b260e18','project.recent','Het werkende paneel met recente bestandsverwijzingen kiezen.')
reuse('a83eb8ff58b13c06','ui.file-associations','PreferencesDialog kiest de gemonteerde FileAssocTab met de echte desktopbestandskoppelingen; geen systeembrede actie onmiddellijk uitvoeren.')
reuse('90702dc3023ca976','view.fullscreen','De fullscreenIcon-tak hoort bij niet-volledig scherm; toggleFullscreen gebruikt de native/window fullscreen-helper.')
reuse('cf09d9c84ae86ffa','view.fullscreen-exit','De fullscreenExitIcon-tak hoort bij bestaand volledig scherm en verlaat die modus via dezelfde helper.')
reuse('f48843819ef7a262 ecdfd921d5b4c7c0','view.pan','Home en Drawing kiezen het geregistreerde handgereedschap.')
reuse('9c3c0149ba2efd5c','edit.select','Drawing activeert het geregistreerde select-gereedschap, geen alles-selecteren.')
reuse('a8edd510118b55a1 e21826904920687c','view.search','De werkende Drawing/Home-knoppen roepen de moderne zoek-/vervangroute of openFindBar aan; geen oude DOM-ID-ingang.')
reuse('7269345649d7805b','panel.right','togglePropertiesPanel schakelt het rechter eigenschappenpaneel.')
reuse('a875895273b345e4','style.tools','Format opent het menu met de beschikbare stijlhulpmiddelen; geen directe stijlplakactie.')
dispatch('85cef4641d3660dc',('object.hide','object.show'),'Format keert ann.hidden van de selectie om. Het vaste bronlabel Hide moet bij adoptie met de toestand worden gelezen; de callback kan ook weer zichtbaar maken.')
reuse('880db261f0a0dced','object.rotate-right-90','Drawing.rotateSelected draait de gekozen annotaties 90 graden rechtsom en registreert undo.')
reuse('8dcc8bb29193ee0a','transform.mirror','Drawing.flipSelectedH spiegelt de annotaties horizontaal.')
reuse('84a085d5c7dca005','transform.flip-vertical','Drawing.flipSelectedV spiegelt de annotaties verticaal.')
dispatch('9173e37b2a381b16',('symbol.library-settings','drawing.settings'),'settingsSvg wordt zowel bij de bibliotheekinstellingen als de afzonderlijke knop Tekeninstellingen van NL IFC Bouw gebruikt; concrete callback bepaalt de keuze.')
reuse('87a6999ea05597e1','ui.dropdown','De plaatsingsschaaltrigger opent de bestaande SchaalCombo-keuzelijst.')
reuse('68b962ca5e145033','file.export','XFDF-export schrijft de huidige annotaties als XFDF; geen raster-PDF of BCF-uitvoer.')
reuse('9d4b53658b1dc4c4','bcf.export','exportBcfToFile bouwt het BCF-pakket uit de PDF-markeringen en laat het bestand bewaren; geen issues pushen naar een server.')
reuse('807a5fd5601a69cb c361d44798fe45b8','file.import','CAD opent de native CAD-importworkflow; XFDF kiest en leest annotatiegegevens in het actieve document. Formaatlabel en desktopbeperkingen blijven expliciet.')
reuse('ae8191f090c89387','extension.install-file','De oppx-bestandskeuze voor een lokaal extensiepakket openen en via installPluginFromFile installeren; geen documentimport.')
reuse('437987078b5dd607','extension.item','Vaste pakketaanduiding bij geïnstalleerde extensies in de levenscycluslijst; geen nieuwe installatieactie.')
reuse('89f1567d07a34377','panel.annotations','LeftPanelTab kiest annotations en ververst de echte annotatielijst.')
reuse('fc467749bd29f802','object.layers','LeftPanelTab kiest het markeringslagenpaneel en ververst de bestaande lagengegevens.')
reuse('63c58d95c3bfbb43','panel.left','toggleLeftPanelCollapsed schakelt het linker paneel om; geen enkele boomgroep.')
dispatch('798edea0b9d21ca3',('ui.check-updates','diagnostics.startup-log'),'updatesIcon bedient zowel checkForUpdates(false) als revealStartupDiagnostics. De tweede vraagt startup_diagnostics_path op en onthult het bestand; geen updatecontrole.')
exclude('f3883c39a1b2785f','Drawing Table staat permanent disabled=true; broncommentaar meldt dat scheduleTable nog niet geregistreerd is.')
exclude('95c8c03a9d8411d0','De mobiele recente rij roept alleen een alert aan om het bestand opnieuw met Open te kiezen; wegens Android-padrechten wordt hier geen bestand heropend.')


def frame(c):
    box(c,2,3,20,18)
    c.line([(2,7),(22,7)],radius=0)

def folder(c):
    c.line([(2,7),(2,21),(22,21),(22,7),(11,7),(9,4),(2,4)],closed=True,radius=.4)

def gear(c,x=18,y=18):
    c.circle(x,y,2.8,True)
    for a in range(0,360,60):
        rad=math.radians(a)
        c.line([(x+3*math.cos(rad),y+3*math.sin(rad)),(x+4.5*math.cos(rad),y+4.5*math.sin(rad))],True,radius=0)

def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key=='draw.filled-area':
        c.line([(3,5),(16,3),(21,11),(17,21),(3,21)],closed=True,radius=.4)
        for pts in [[(5,9),(10,19)],[(9,7),(15,19)],[(14,6),(18,14)]]:c.line(pts,True,radius=0)
    elif key=='image.embedded-edit':
        page(c,2,3,16,18)
        c.circle(7,8,1)
        c.line([(5,16),(8,12),(12,16)],radius=.3)
        c.line([(13,18),(19,12),(22,15),(16,21),(12,22)],True,closed=True,radius=.3)
    elif key=='transform.length-axis':
        c.line([(3,15),(17,15)],radius=0)
        c.line([(3,11),(3,19)],radius=0)
        c.circle(17,15,2,True)
        c.line([(9,6),(22,6)],True,radius=0)
        c.line([(12,3),(9,6),(12,9)],True,radius=.3)
        c.line([(19,3),(22,6),(19,9)],True,radius=.3)
    elif key.startswith('panel.'):
        kind=key[6:]
        if kind=='thumbnails':
            for x in (3,13):box(c,x,3,8,18)
            for x in (6,16):
                if small:c.line([(x,8),(x+2,8)],True,radius=0)
                else:c.line([(x,7),(x+2,7),(x+2,12),(x,12)],True,radius=.3)
        elif kind=='bookmarks':
            page(c,3,3,18,18)
            c.line([(9,3),(16,3),(16,16),(12.5,13),(9,16)],True,closed=True,radius=.3)
        elif kind=='attachments':
            page(c,2,3,14,18)
            c.line([(15,7),(15,16)]+arc_points(18,16,3,180,0,20)[1:]+[(21,7),(18,7),(18,15)],True,radius=.3)
        elif kind=='signatures':
            frame(c);c.line([(6,17),(10,10),(9,17),(14,12),(16,15),(20,12)],True,radius=.3)
        elif kind=='form-fields':
            page(c,2,3,20,18)
            for y in (8,15):
                box(c,6,y-1,3,3,True);c.line([(13,y+.5),(18,y+.5)],radius=0)
        elif kind=='destinations':
            frame(c);c.line([(8,20),(8,10)],True,radius=0)
            c.line([(8,10),(18,10),(15,13),(18,16),(8,16)],True,closed=True,radius=.3)
        elif kind=='tags':
            page(c,3,3,18,18)
            c.line([(7,8),(7,17),(17,17)],True,radius=.3)
            c.line([(7,11),(16,11)],True,radius=0)
            c.circle(16,11,1.2,True,filled=True)
        elif kind=='links':
            frame(c)
            c.line(arc_points(9,14,3.5,45,315,24),True,radius=0)
            c.line(arc_points(16,14,3.5,225,495,24),True,radius=0)
            c.line([(9,14),(16,14)],True,radius=0)
        elif kind=='measurements':
            frame(c)
            c.line([(5,10),(19,10)],True,radius=0)
            for x in (6,12,18):c.line([(x,10),(x,13)],True,radius=0)
            c.line([(6,17),(17,17)],radius=0)
        else:
            box(c,2,3,20,18)
            for y in (9,15):c.line([(2,y),(22,y)],radius=0)
            c.line([(9,3),(9,21)],radius=0)
            for y in (6,12,18):c.line([(13,y),(18,y)],True,radius=0)
    elif key.startswith('preferences.'):
        if key.endswith('annotations'):
            page(c,2,3,13,18);c.line([(5,15),(11,9)],radius=0);gear(c)
        elif key.endswith('behavior'):
            for y in (6,15):
                c.line([(3,y),(21,y)],radius=0)
                c.circle(8 if y==6 else 16,y,2.5,True)
        else:
            page(c,2,3,13,18);c.line([(5,8),(11,8)],radius=0);gear(c)
    elif key=='printer.virtual-settings':
        box(c,2,8,19,10);box(c,6,2,12,6);box(c,6,14,11,8);gear(c,18,18)
    elif key=='recent.pin-toggle':
        c.line([(12,14),(12,22)],radius=0)
        c.line([(7,3),(17,3),(16,9),(21,14),(3,14),(8,9)],True,closed=True,radius=.3)
    elif key=='session.restore':
        page(c,2,3,13,18)
        c.line(arc_points(17,15,5,-90,200,32),True,radius=0)
        c.line([(12,13),(12,18),(16,17)],True,radius=.3)
    elif key=='file.place-add':folder(c);c.plus(18,17,4,True)
    elif key=='file.places':
        folder(c);c.circle(12,12,2.5,True);c.line([(12,15),(12,19)],True,radius=0)
    elif key=='file.host-library':
        frame(c);page(c,6,10,6,9,True);page(c,15,10,4,9,True)
    elif key=='symbol.library-settings':
        c.line([(2,3),(10,3),(10,20),(2,20)],closed=True,radius=.3)
        c.line([(13,3),(21,3),(21,10)],radius=.3);gear(c)
    elif key=='drawing.settings':
        c.line([(3,3),(3,21),(16,21)],closed=True,radius=.3)
        c.line([(7,12),(7,17),(10,17)],radius=.3);gear(c)
    elif key=='symbol.system-types':
        for x,y in ((3,3),(13,3),(3,13)):box(c,x,y,7,7)
        c.line([(14,17),(17,14),(21,18),(17,22)],True,closed=True,radius=.3)
    elif key.startswith('extension.'):
        box(c,2,3,15,18);box(c,5,3,9,4)
        if key.endswith('reinstall-file'):
            c.line(arc_points(17,16,5,-80,200,32),True,radius=0)
            c.line([(12,14),(12,19),(16,18)],True,radius=.3)
        else:
            c.circle(18,17,4,True);c.line([(16,17),(20,17)],True,radius=0)
    elif key=='link.open-internal':
        page(c,3,3,18,18)
        c.line([(7,9),(16,9),(16,17),(12,13)],True,radius=.3)
        c.line([(16,17),(20,13)],True,radius=.3)
    elif key=='signature.status-unknown':
        c.circle(12,12,9);glyph(c,'?',8,6,8,12)
    elif key=='annotate.tools-menu':
        box(c,2,3,20,18)
        c.line([(5,15),(12,8),(15,11),(8,18)],True,closed=True,radius=.3)
        c.line([(18,11),(18,17)],radius=0)
    elif key=='update.previous-download':
        page(c,2,3,13,18)
        c.line([(22,8),(17,8),(17,18),(14,15)],True,radius=.3)
        c.line([(17,18),(20,15)],True,radius=.3)
    elif key=='diagnostics.startup-log':
        page(c,2,3,10,18)
        c.line([(5,8),(9,8)],radius=0)
        c.line([(5,13),(9,13)],radius=0)
        c.circle(19,15.5,3,True)
        c.line([(21.2,17.7),(23,20)],True,radius=0)
    elif key=='bcf.import':
        page(c,2,3,14,18)
        for y in (8,13,18):c.circle(6,y,.8,filled=True)
        c.line([(23,12),(11,12),(14,9)],True,radius=.3)
        c.line([(11,12),(14,15)],True,radius=.3)
    return True
