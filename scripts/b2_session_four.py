"""Original B2 artwork: 40 source-reviewed PDF actions and field indicators."""
import math
from b2_second_series import box
from b2_bulk_series import page
from b2_session_two import dimension_arrow,fill_rect
from b2_session_three import plus
from b2_energy_pile_audio import arc_points
from b2_font_geometry import add_letter

AVAILABLE_SERIES=(39,40,41,42,43,44,45)
GROUPS={39:'Notities en afdrukgedrag',40:'Meetbewerkingen',41:'Zoekresultaten',42:'Werkruimte',43:'Formulierveldtypen',44:'Documentgegevens en sessies',45:'Thema en kleur'}
# Series, function, label, exact behavior, source record, original cluster.
ROWS=[
 (39, 'note.open', 'Pop-upnotitie openen', 'De bestaande annotatienotitie openen via openStickyPopup; geen nieuwe annotatie maken.', '8d0c937be7f77035', 'review.popupnotitieopenen'),
 (39, 'note.hide', 'Pop-upnotitie verbergen', 'De pop-up sluiten via closeStickyPopup; annotatie en tekst blijven bestaan.', '4ca7070d06ef031e', 'review.popupnotitieverbergen'),
 (39, 'note.reset-position', 'Notitiepositie herstellen', 'popupX/popupY wissen en de pop-up op zijn standaardpositie heropenen.', '2c6ce69d1d0fdb4a', 'review.popupnotitielocatieherstellen'),
 (39, 'note.reply', 'Reactie toevoegen', 'Een lege reactie aan annotation.replies toevoegen en de notitie openen.', '145cdd8fcb6bc2d9', 'review.reactietoevoegen'),
 (39, 'annotate.printable', 'Annotatie afdrukbaar', 'De printable-eigenschap van de geselecteerde annotatie schakelen; geen afdrukopdracht.', '0ba7eeedcf19fdda', 'review.afdrukbaar'),
 (40, 'line.reverse', 'Lijnrichting omkeren', 'Start- en eindcoordinaten van de geselecteerde lijn verwisselen.', '4403657c2937cbb0', 'review.lijnomdraaien'),
 (40, 'line.to-measure', 'Lijn naar afstandsmeting', 'Het lijntype veranderen naar measureDistance met behoud van de eindpunten.', '7be95a9b4c2467b7', 'review.omzettennaarmeting'),
 (40, 'measure.calibrate-line', 'Kalibreren vanuit lijn', 'showCalibrationDialog openen met de pixellengte van de geselecteerde meetlijn.', 'ab7704cc5ed71f88', 'review.kalibrerenvanuitdezelijn'),
 (40, 'measure.set-scale', 'Meetschaal instellen', 'Het schaaldialoog openen met lengte, tekst, eenheid en geselecteerde annotatie.', '7135d2fcc4afe9bc', 'review.schaalinstellen'),
 (40, 'measure.chain-add', 'Maatketting uitbreiden', 'dimChainAdd activeren en de geselecteerde meetlijn als doel vastleggen.', 'f8c439cc0d7bd714', 'review.puntentoevoegenaanmaatketting'),
 (40, 'measure.chain-remove', 'Maatketting inkorten', 'dimChainRemove activeren om een hulplijn uit de gekozen maatketting te verwijderen.', '18a6b614a961b7e6', 'review.hulplijnuitmaatkettinghalen'),
 (40, 'room.select-from-tag', 'Ruimte vanuit tag selecteren', 'De bij een room-tag behorende ruimte selecteren via selecteerRuimteVanTag.', '3fda932fad46d2ca', 'review.ruimteselecteren'),
 (40, 'measure.add-hole', 'Sparing in meetvlak', 'addHole activeren voor de geselecteerde oppervlaktemeting.', 'debae6af99f76ec4', 'review.sparingtoevoegen'),
 (40, 'line.to-polyline', 'Lijn naar polylijn', 'De lijn naar polyline omzetten met start- en eindpunt als eerste punten.', '5b6ab6fa62381857', 'review.omzettennaarpolylijn'),
 (40, 'line.to-polygon', 'Lijn naar veelhoek', 'De lijn naar polygon omzetten; de bron start met twee bestaande eindpunten.', '9c4fe4ee7aee3e72', 'review.omzettennaarveelhoek'),
 (41, 'search.previous', 'Vorige zoektreffer', 'onFindPrevious activeren binnen de huidige zoekresultaten.', '8ea28c824acb0862', 'review.vorigetreffer'),
 (41, 'search.next', 'Volgende zoektreffer', 'onFindNext activeren binnen de huidige zoekresultaten.', '82b72f4010cb57cb', 'review.volgendetreffer'),
 (41, 'search.whole-word', 'Alleen hele woorden', 'De wholeWord-zoekoptie via onOptionsChange schakelen.', 'd88f06ad1a01f2d3', 'review.helewoorden'),
 (41, 'search.highlight-all', 'Alle zoektreffers markeren', 'De markering van alle zoektreffers via onHighlightAllChange schakelen.', '7b2193e288675d8b', 'review.allesmarkeren'),
 (42, 'workspace.ribbon-toggle', 'Lint in- en uitklappen', 'toggleCollapsed van het lint bedienen; geen venster maximaliseren.', '25028afb58b06625', 'review.lintuitklappen'),
 (42, 'workspace.dock-left', 'Palet links vastzetten', 'Sleepdoel voor een uitbreidingspalet; startExtDrag registreert docked-left na loslaten.', '82d10edb8d7f2cd4', 'review.linksdocken'),
 (42, 'workspace.dock-right', 'Palet rechts vastzetten', 'Sleepdoel voor een uitbreidingspalet; startExtDrag registreert docked-right na loslaten.', '040af2cf51855441', 'review.rechtsdocken'),
 (42, 'workspace.toolbar-toggle', 'Onderste werkbalk inklappen', 'handleToggleCollapse bedient de onderste mobiele werkbalk.', '6fe6bec4abd1e1a6', 'review.onderstewerkbalkinuitklappen'),
 (42, 'workspace.navigation-menu', 'Navigatiemenu openen', 'setDrawerOpen(true) opent de mobiele navigatielade.', '12c9a45935d6b4ee', 'review.navigatiemenuopenen'),
 (43, 'field.text', 'Tekstveld', 'Typeaanduiding van een bestaand tekstveld in FormFieldsPanel; geen invoegactie.', '027ace8b0316ca0c', 'review.tekstveld'),
 (43, 'field.checkbox', 'Selectievak', 'Typeaanduiding van een bestaand selectievak in de formulierveldenlijst.', 'fb0dac081b01203b', 'review.selectievak'),
 (43, 'field.radio', 'Keuzerondje', 'Typeaanduiding van een bestaand radiobutton-veld.', '3b56956b26f5f1ef', 'review.keuzerondje'),
 (43, 'field.combo', 'Uitklapbaar keuzeveld', 'Typeaanduiding combobox; apart van een altijd zichtbare lijst.', '2f6ad39989e87bee', 'review.keuzelijst'),
 (43, 'field.list', 'Lijstveld', 'Typeaanduiding listbox met meerdere zichtbare keuzeregels.', 'c3124ee8a1ced5c5', 'review.lijstveld'),
 (43, 'field.button', 'Formulierknop', 'Typeaanduiding van een bestaande formulierknop; geen algemene bevestiging.', '6819f2c8d4b47df2', 'review.formulierknop'),
 (44, 'document.properties', 'Documenteigenschappen', 'showDocPropertiesDialog openen voor het actieve document.', '2083929968e0adbf', 'review.documenteigenschappen'),
 (44, 'page.properties', 'Pagina-eigenschappen', 'page-properties openen voor de geselecteerde miniatuurpagina.', 'd5f9aa3ae6b0dd57', 'review.paginaeigenschappen'),
 (44, 'file.reveal', 'Bestand in map tonen', 'revealInFileManager met doc.filePath aanroepen; alleen beschikbaar met lokaal bestandspad.', 'fa035d78e67c6b05', 'review.bestandtoneninbestandsbeheerder'),
 (44, 'page.labels', 'Paginalabels instellen', 'Het page-labels-dialoog openen; geen bladwijzer toevoegen.', 'e5e74bc432548fa0', 'review.paginalabelsopenen'),
 (44, 'document.open-url', 'Openen via URL', 'Het URL-subpaneel voor het openen van een PDF tonen; geen externe link volgen.', '62874eba684fd598', 'review.navigatieopenenvanurl'),
 (44, 'workspace.sessions', 'Opgeslagen sessies', 'Het sessieoverzicht met bewaren/herstellen openen.', '026d1eea2926126a', 'review.navigatiesessies'),
 (44, 'document.compare-swap', 'Vergelijkingsdocumenten wisselen', 'Oud/nieuw-document en hun paginanummers samen verwisselen in CompareDialog.', '1642450512186aff', 'review.documentenomwisselen'),
 (45, 'theme.dark', 'Donkere modus', 'De lichte weergave naar donker omschakelen via applyTheme.', '9291ed54cb19cbe3', 'review.donkeremodusinschakelen'),
 (45, 'theme.light', 'Lichte modus', 'De donkere weergave naar licht omschakelen via applyTheme.', '56df659c81cb5864', 'review.lichtemodusinschakelen'),
 (45, 'format.no-color', 'Geen kleur', 'De onNone-callback van de kleurkiezer activeren en de kiezer sluiten.', 'e32c5f81b05c4279', 'review.geenkleur'),
]
DEFINITIONS=[(k,l,GROUPS[b],m) for b,k,l,m,_,_ in ROWS]
EXAMPLES={k:r for _,k,_,_,r,_ in ROWS}
SOURCE_FUNCTIONS={k:s for _,k,_,_,_,s in ROWS}
SERIES={k:b for b,k,_,_,_,_ in ROWS}
KEYS=set(SERIES)
EVIDENCE={k:'Typeaanduiding gelezen in FIELD_TYPE_ICONS[field.type], geen aanmaakknop.' for k in KEYS if k.startswith('field.')}
EVIDENCE.update({k:'Sleepdoelweergave en startExtDrag/onUp gelezen; geen klikknop.' for k in ('workspace.dock-left','workspace.dock-right')})
REUSED={'289cadfa2e020361':('object.properties','Het menu Beoordelingsgeschiedenis roept alleen showProperties(a) aan; geen aparte geschiedenisfunctie bewezen.')}
ISSUES={'e59cfa883ea6d9b1':'Bronlabel Palet losmaken klopt niet: dit is de sluitknop van FloatingExtPalette (visible=false). Algemene sluitbediening heeft nog geen eigen B2-contract; niet aan venster sluiten koppelen.'}



def note(c,x=3,y=4,w=12,h=11):
    c.line([(x,y),(x+w,y),(x+w,y+h),(x+6,y+h),(x+3,y+h+3),(x+3,y+h),(x,y+h)],closed=True,radius=.6)


def info(c,x=19,y=17,r=4):
    c.circle(x,y,r,True)
    c.circle(x,y-1.7,.5,True,True)
    c.line([(x,y+.3),(x,y+2)],True,radius=0)


def ruler(c):
    box(c,3,4,18,7)
    for x in (7,12,17):c.line([(x,4),(x,7)],radius=0)


def folder(c):
    c.line([(3,20),(3,5),(9,5),(11,8),(21,8),(21,20)],closed=True,radius=.7)


def extend(c,key):
    if key not in KEYS:return False
    if key.startswith('note.'):
        note(c,w=11 if key=='note.reset-position' else 12)
        if key=='note.open':dimension_arrow(c,(18,14),(22,10),1.5)
        elif key=='note.hide':c.line([(18,12),(22,12)],True,radius=0)
        elif key=='note.reply':plus(c,20,17,2.5)
        else:
            c.line([(22,8),(22,18),(17,18)],True,radius=.8)
            c.line([(19,16),(17,18),(19,20)],True,radius=.3)
    elif key=='annotate.printable':
        c.line([(6,17),(3,17),(3,8),(17,8),(17,17),(14,17)],radius=.5)
        c.line([(6,8),(6,3),(14,3),(14,8)],radius=.4)
        box(c,6,13,8,8)
        c.line([(18,17),(20,19),(23,14)],True,radius=.3)
    elif key=='line.reverse':
        c.line([(4,7),(20,7)],radius=0)
        c.circle(4,7,1.6,filled=True);c.circle(20,7,1.6,filled=True)
        dimension_arrow(c,(5,14),(19,14),1.6)
        dimension_arrow(c,(19,20),(5,20),1.6)
    elif key in {'line.to-measure','line.to-polyline','line.to-polygon'}:
        c.line([(3,4),(11,4)],radius=0)
        dimension_arrow(c,(17,4),(21,8),1.5)
        if key=='line.to-measure':
            c.line([(3,15),(21,15)],radius=0)
            for x in (3,21):c.line([(x,12),(x,19)],True,radius=0)
        elif key=='line.to-polyline':c.line([(3,21),(3,13),(12,13),(12,20),(21,20)],True,radius=.5)
        else:c.line([(3,21),(5,13),(16,13),(21,21)],True,closed=True,radius=.5)
    elif key in {'measure.calibrate-line','measure.set-scale'}:
        ruler(c)
        if key=='measure.calibrate-line':
            c.line([(4,19),(20,19)],True,radius=0)
            for x in (4,20):c.line([(x,16),(x,22)],True,radius=0)
            c.circle(12,19,1.2,True,True)
        else:
            c.line([(5,16),(5,22)],True,radius=0)
            c.line([(12,16),(12,22)],True,radius=0)
            c.line([(19,16),(19,22)],True,radius=0)
            for x,y in ((5,18),(12,20),(19,18)):c.circle(x,y,1.5,True,True)
    elif key in {'measure.chain-add','measure.chain-remove'}:
        c.line([(3,9),(21,9)],radius=0)
        for x in (3,12,21):c.line([(x,5),(x,13)],radius=0)
        c.line([(9,20),(15,20)],True,radius=0)
        if key.endswith('add'):c.line([(12,17),(12,23)],True,radius=0)
    elif key=='room.select-from-tag':
        c.line([(3,3),(15,3),(15,9),(21,9),(21,21),(3,21)],closed=True,radius=.5)
        c.line([(8,8),(8,15),(13,12)],True,closed=True,radius=.3)
    elif key=='measure.add-hole':
        box(c,3,3,18,18);box(c,9,9,6,6,True)
    elif key in {'search.previous','search.next'}:
        c.circle(9,8,5);c.line([(12.6,11.6),(16,15)],radius=0)
        dimension_arrow(c,(4,21),(20,21),1.8)
        if key.endswith('previous'):c.mirror()
    elif key=='search.whole-word':
        c.line([(6,5),(3,5),(3,19),(6,19)],True,radius=.4)
        c.line([(18,5),(21,5),(21,19),(18,19)],True,radius=.4)
        add_letter(c,key)
    elif key=='search.highlight-all':
        for y in (5,12,19):
            c.line([(3,y),(7,y)],True,radius=0)
            c.line([(12,y),(21,y)],radius=0)
    elif key.startswith('workspace.') and key!='workspace.sessions':
        if key=='workspace.navigation-menu':
            for y in (5,12,19):c.line([(4,y),(20,y)],y==12,radius=0)
        else:
            box(c,3,3,18,18)
            if key=='workspace.ribbon-toggle':
                c.line([(3,9),(21,9)],radius=0)
                c.line([(9,14),(12,17),(15,14)],True,radius=.3)
            elif key=='workspace.toolbar-toggle':
                c.line([(3,16),(21,16)],radius=0)
                c.line([(9,11),(12,8),(15,11)],True,radius=.3)
            else:
                c.line([(9,3),(9,21)],radius=0)
                dimension_arrow(c,(19,12),(12,12),1.7)
                if key.endswith('right'):c.mirror()
    elif key.startswith('field.'):
        if key=='field.radio':
            c.circle(12,12,8);c.circle(12,12,3,True,True)
        elif key=='field.checkbox':
            box(c,4,4,16,16);c.line([(8,12),(11,15),(16,9)],True,radius=.4)
        elif key=='field.text':
            box(c,3,6,18,12)
            c.line([(7,9),(13,9)],True,radius=0);c.line([(10,9),(10,15)],True,radius=0)
            c.line([(17,9),(17,15)],radius=0)
        elif key=='field.combo':
            box(c,3,6,18,12);c.line([(14,6),(14,18)],radius=0)
            c.line([(16.5,11),(18,13),(19.5,11)],True,radius=.3)
            c.line([(6,12),(10,12)],radius=0)
        elif key=='field.list':
            box(c,3,3,18,18)
            for y in (7,12,17):c.line([(7,y),(17,y)],y==12,radius=0)
        else:
            box(c,3,6,18,12);dimension_arrow(c,(8,12),(16,12),1.6)
    elif key in {'document.properties','page.properties'}:
        if key=='document.properties':
            c.line([(2,17),(2,3),(10,3)],radius=.5)
            page(c,5,6,7,15)
        else:page(c,2,3,10,18)
        info(c,19,18,4)
    elif key=='file.reveal':
        folder(c)
        c.circle(12,13,2.5,True);c.line([(14,15),(17,18)],True,radius=0)
    elif key=='page.labels':
        page(c,1,3,9,18)
        c.line([(12,12),(19,12),(23,16),(19,20),(12,20)],True,closed=True,radius=.4)
        c.circle(15,16,.65,True,True)
    elif key=='document.open-url':
        c.circle(10,10,7)
        c.line([(3,10),(17,10)],radius=0)
        c.line([(10+3*math.cos(2*math.pi*i/64),10+7*math.sin(2*math.pi*i/64)) for i in range(64)],closed=True,radius=0)
        dimension_arrow(c,(16,21),(22,15),1.6)
    elif key=='workspace.sessions':
        box(c,3,3,18,18);c.line([(3,8),(21,8)],radius=0)
        for x in (6,9,12):c.circle(x,5.5,.5,filled=True)
        box(c,6,11,5,7);box(c,14,11,4,7,True)
    elif key=='document.compare-swap':
        page(c,2,6,7,12);page(c,15,6,7,12)
        dimension_arrow(c,(7,3),(17,3),1.5)
        dimension_arrow(c,(17,21),(7,21),1.5)
    elif key=='theme.light':
        c.circle(12,12,4.5)
        for a in range(0,360,45):
            t=math.radians(a);c.line([(12+8*math.cos(t),12+8*math.sin(t)),(12+10*math.cos(t),12+10*math.sin(t))],True,radius=0)
    elif key=='theme.dark':
        # A filled crescent from two equal circles with exact shared tips.
        angle=math.degrees(math.acos(2.5/9))
        outer=arc_points(12,12,9,-angle,angle-360,32)
        inner=arc_points(17,12,9,180-angle,180+angle,24)
        scale=c.size/24
        c.fills.append({'tone':'primary','rings':[[(x*scale,y*scale) for x,y in outer+inner[1:]]]})
        star=[(20,3.5),(20.7,5.3),(22.5,6),(20.7,6.7),(20,8.5),(19.3,6.7),(17.5,6),(19.3,5.3)]
        c.fills.append({'tone':'accent','rings':[[(x*scale,y*scale) for x,y in star]]})
    elif key=='format.no-color':
        # Paint bucket and separate minus: remove the chosen colour.
        c.line([(3,10),(10,3),(17,10),(10,17)],closed=True,radius=.5)
        c.line([(5,8),(5,3),(8,3)],radius=.5)
        c.line([(17,10),(20,13),(20,15)],radius=.5)
        c.line([(16,21),(22,21)],True,radius=0)
    return True
