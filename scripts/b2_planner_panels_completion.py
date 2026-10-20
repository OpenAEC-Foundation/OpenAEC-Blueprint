"""Planner panels and informational states, each tied to explicit pinned source records."""
import math
from b2_second_series import box
from b2_energy_pile_audio import arc_points
from b2_planner_safety_completion import turn

GROUPS={148:'Prestatiemeting en begeleiding',149:'Bezettingsinformatie en tabelkolommen',150:'Profielconcept en toelichting',151:'Bibliotheekkoppeling en conceptinvoer',152:'Pakketgrootte in releasevergelijking'}
ROWS=[
 (148,'diagnostics.benchmark','Prestatiemeting','Vaste kopaanduiding bij BenchmarkDialog met genereren, CPM, IFC schrijven/lezen en renderen; het Gauge-beeld zelf start geen meting.','683e094033f97411'),
 (148,'diagnostics.run-benchmark','Prestatiemeting starten','runBenchmark starten voor de gekozen synthetische projectgrootte en resources; de voortgang en meetresultaten blijven in de dialoog. Geen audio afspelen.','336fa071353dc251'),
 (148,'guide.compact','Begeleiding compact tonen','Het begeleidingspaneel tussen compacte en uitgebreide weergave wisselen via de lokale override; de stap en sessie blijven gelijk.','72e0334f57318b3d'),
 (149,'status.schedule-preview','Tijdelijk doorgerekende bezetting','Het document is nog als verouderd gemarkeerd, maar de getelde bezettingscijfers zijn op een kloon tijdelijk doorgerekend. Dit is informatief, geen waarschuwing of F5-actie.','6f26090b63e67a9e'),
 (149,'status.schedule-last-result','Laatst berekende bezetting','Het verouderde document telt mee met de laatst berekende taken omdat de tijdelijke solve voor dit document is overgeslagen; geen fout- of succesclaim.','6f26090b63e67a9e'),
 (149,'table.column-add-menu','Zichtbare kolom toevoegen','De kolommenkiezer openen voor een extra zichtbare tabelkolom; pas een beschikbare optie kiezen commit de toevoeging.','3db0102c6df46a3d'),
 (149,'table.columns-reset','Standaardkolommen herstellen','De tabelkolommen via de gedeelde commitroute op een kopie van defaultColumns terugzetten; geen tabellen of taken wissen.','41f0991d4d3e0c7e'),
 (149,'status.column-present','Kolom al zichtbaar','Vaste Check in de kolommenkiezer wanneer de kolom al zichtbaar is; de optie is dan disabled om dubbel toevoegen te voorkomen.','12b43c3642f5b53e'),
 (150,'planning.profile-new','Nieuw planningsprofiel','Het naamdialoog voor een nieuw benoemd planningsprofiel op basis van het huidige profiel openen; bevestigen maakt een nieuw profiel-ID in de formulierinvoer.','0b76be5246f89cc2'),
 (150,'help.context-hint','Korte toelichting','Een korte title- of hovertoelichting bij de huidige instelling of het veld aanduiden; geen algemeen helpartikel of zelfstandige dialoog.','da667c4f2ba3b045'),
 (151,'library.link-recognized','Herkende items koppelen','De voorgestelde herkomstkoppeling voor één of meerdere herkende projectresources of -kalenders vastleggen via linkRecognizedItems; geen projectitem naar de pool kopiëren.','a8648f847ed3122e'),
 (151,'status.library-item-missing','Bibliotheekorigineel ontbreekt','De herkomst verwijst naar een poolitem dat niet meer bestaat; de projectkopie blijft aanwezig. Vaste removed-status, geen verwijderactie.','6d3338a5a7cb53e2'),
 (151,'status.library-item-deviated','Bibliotheekafwijking beoordelen','De projectkopie wijkt af van de synchronisatiestempel of de vergelijkingshash ontbreekt terwijl de poolinhoud veranderde; de deviated-status vraagt een keuze, vervangt niets automatisch.','6d3338a5a7cb53e2'),
 (151,'status.library-suggestion','Voorgesteld bibliotheekitem','De vaste pijl tussen een projectnaam en de voorgestelde poolnaam aanduiden; geen vooruitnavigatie of directe koppeling.','c450e1fbdecb4faf'),
 (151,'input.confirm-draft','Conceptinvoer bevestigen','De lokale invoer voor een nieuwe bibliotheeknaam bevestigen en de naameditie sluiten; pas het hele projectformulier toepassen maakt de bibliotheek aan.','899af3928ea01a03'),
 (152,'status.install-size-smaller','Installatiepakket kleiner','Een negatieve pakketgrootteverandering in de getoonde releasevergelijking aanduiden; geen download of verkleinopdracht.','71cc93d4f9ed5731'),
 (152,'status.install-size-larger','Installatiepakket groter','Een positieve pakketgrootteverandering in de getoonde releasevergelijking aanduiden; geen download of vergrootopdracht.','31a60d97c3af6078'),
]
KEYS={r[1] for r in ROWS}
ACCENT_FRONT={k:'De bepalende markering blijft vóór de dragende contour zichtbaar.' for k in KEYS}
SEMANTIC={k:'text-secondary' for k in ('status.schedule-preview','status.schedule-last-result','status.column-present','help.context-hint','status.library-suggestion','status.install-size-smaller','status.install-size-larger')}
SEMANTIC.update({'status.library-item-missing':'error','status.library-item-deviated':'error'})
REUSED={};EXCLUDED={}
DISPATCHERS={'6f26090b63e67a9e':('status.schedule-preview','status.schedule-last-result'),
             '6d3338a5a7cb53e2':('status.library-item-missing','status.library-item-deviated'),
             '70d2153116d39216':('tree.expand','tree.collapse')}
DISPATCH_EVIDENCE={
 '6f26090b63e67a9e':'De dim-AlertTriangle wordt alleen gebruikt bij doc.counted && doc.scheduleStale; ephemeralComputed kiest tijdelijke solve versus laatst berekende taken. occupancy.ts rekent een kloon door of gebruikt skipEphemeralSolve. De andere drie AlertTriangle-plaatsen zijn echte waarschuwingen voor niet meetellen.',
 '6d3338a5a7cb53e2':'De rode badge kiest d.status removed of deviated. libraryOps.classifyOnOpen onderscheidt ontbrekend poolorigineel van hashafwijking/ontbrekende syncedHash; beide zijn toestand, geen actie.',
 '70d2153116d39216':'Categorieknop toggelt openCategories; expanded bepaalt of de geneste itemList zichtbaar is. De ene ChevronDown met data-expanded is een rij-open/dichtdispatcher, geen los keuzemenu.'}
EVIDENCE={k:DISPATCH_EVIDENCE[rid] for k,rid in (('status.schedule-preview','6f26090b63e67a9e'),('status.schedule-last-result','6f26090b63e67a9e'),('status.library-item-missing','6d3338a5a7cb53e2'),('status.library-item-deviated','6d3338a5a7cb53e2'))}
EVIDENCE['input.confirm-draft']='confirmNewCompany zet alleen creatingCompany false en companyTouched true; addCompany gebeurt pas later in handleSubmit wanneer pendingNewCompany waar is. Check is geen status of onmiddellijke globale aanmaak.'
def reuse(ids,key,reason):
    for rid in ids.split():REUSED[rid]=(key,reason)
reuse('15b2a622a4199220 da71566f29567d51','extension.install-file','De ZIP-/JS-knoppen roepen de concrete bestandspickers installFromFile/installFromJsFile aan; installatie volgt het bestaande toestemmingspad. Het formaatlabel blijft bij de knop.')
reuse('55e052a76eafc448 252888cce5e3b049','extension.item','Puzzle is de manifestfallback van een geïnstalleerd pakket; Plus is een vast CatalogCard-beeld naast een aparte tekst-installatieknop. Het Plus-beeld zelf voert geen installatie uit.')
reuse('544ca123e177afed','status.warning','De vaste quarantainekaart meldt dat de extensie niet is geladen met ext.reason; het amberkleurige teken is geen foutieve verwijder-/installatieknop.')
reuse('886157b884d98700','edit.copy','Kopieert de werkelijk opgebouwde Markdown-meetresultaten; useCopyFeedback en een textarea-fallback geven kopieersucces terug.')
reuse('784e276fe10dd32b','status.success','Check is uitsluitend de tijdelijke copied-toestand na het kopiëren van benchmarkresultaten.')
reuse('a8d1bc15cd850d48','status.warning','Alleen bij grote synthetische projecten staat de waarschuwing dat de benchmark zwaar kan zijn; geen bestaande meetfout.')
reuse('b004b0c0f775d13d','guide.compact','De uitgebreide tegenvorm zet de override op collapsed; dezelfde weergavebediening, niet stapnavigatie.')
reuse('6dfa58f3d8cae8ed 6cbb8c55286b8977','status.success','Beide CheckCircle2-plaatsen verschijnen alleen als view.done voor de huidige begeleidingsstap waar is; geen Voltooien-knop.')
reuse('8efbacac4f899b4d','ui.close','stopGuideSession sluit de begeleidingssessie, ruimt timer/subscriptie op en meldt de gewijzigde view; geen document sluiten.')
reuse('8b42bb49cf6c2e75 03db55a5edbabde7 279d440ec0c1364a','status.warning','Deze drie bezettingsplaatsen waarschuwen dat een document niet is meegeteld omdat er geen bruikbare doorgerekende planning beschikbaar is; de twee dim-informatietoestanden hebben eigen ontwerpen.')
EXCLUDED['15779475dac703c1']='Uitsluitend een streepjeslijn als grafieklegenda voor resourcecapaciteit, met aria-hidden en begeleidende tekst; dit is een visuele datasleutel, geen vast bedienings- of statusicoon.'
reuse('6350c251d8c672e2','view.search','De vaste Search staat bij de kolomzoekinvoer; query filtert beschikbare kolomlabels in buildColumnChooserModel.')
reuse('6970c7bd9259dcee','tree.collapse','ChevronDown staat bij de geopende Conventies-sectie; de knop toggelt conventionsOpen en sluit de uitlegrijen.')
reuse('22f1a68ae618c8ea','tree.expand','ChevronRight staat bij de gesloten Conventies-sectie en toont de geneste conventierijen.')
reuse('163e99a7168d3edb','ui.close','dismissOptionsNotice sluit de informatieve afwijkingsnotitie; wijzigt geen profielconventie via deze X.')
reuse('f88ac67684616406','tree.collapse','De geopende versielijst van een sitebestand sluiten via toggleVersions; geen dropdown voor een invoerveld.')
reuse('749bf70c9c5d5791','tree.expand','toggleVersions opent een geneste versielijst en haalt listSiteVersions op voor de bestandsrij.')
reuse('f53d722bc1c99714','file.type-other','De documentaanduiding staat bij een sitebestandsnaam; de rij kiest openLatest/answerSiteOpen, het beeld maakt geen nieuw document.')
reuse('a805647a88106fdc','file.open','Van deze pc kiest answerSiteOpen(kind local), waarna de gewone bestandsopenroute de lokale keuze afhandelt; geen vaste HardDrive-status.')
reuse('d68a1249b36dc6ec','ui.refresh','Opnieuw proberen zet attempt hoger; de effectroute laadt listSiteFiles opnieuw met dezelfde extensiefilters.')
reuse('e493a38ee9b5a9ba a205bbb2a71ead6a','status.warning','Paneelkop meldt verouderde planning; de rijtak toont een niet-fataal schedule warning. Het navigeren naar een doel gebeurt op de rij.')
reuse('532c3d6f9123f2dc','status.error','OctagonAlert is de expliciete error-tak in de planningswaarschuwingsrij; geen stopknop.')
reuse('b66677d14a205460','status.success','Alleen als cpmResult aanwezig is en warnings leeg is staat het vaste Geen-waarschuwingen-beeld.')
reuse('0fc7a3431364f3a1','planning.calculate','De als RefreshCw getekende knop roept werkelijk runCPM aan; geen lijstvernieuwing of spinner.')
reuse('459a9f7c5e4e45a0','ui.help','readMore sluit de formatnotitie en opent het passende interne helpartikel via openHelpArticleGuarded.')
reuse('b1bc368e8d812e93','status.success','De vaste success-notitie benoemt welke informatie bij de import behouden is; geen bevestigingsopdracht.')
reuse('9eee196070697242','status.warning','CircleMinus hoort bij de warning-notitie over formaatbeperkingen; geen waarde verlagen of item verwijderen.')
reuse('cdd32948be09ea83','status.info','De vaste Save in de info-notitie legt de toekomstige opslag uit; er is geen save-handler op dit beeld.')
reuse('99a5356fd5461747','link.open-external','De knop opent de changelog via het bewaakte openExternal-pad; geen inhoud of feedback verzenden.')
reuse('4a86a3a763ea9970','ui.help','De releasehighlight-knop sluit het updatevenster en opent het bijbehorende interne docsId.')
reuse('15b324d9159e3fd4','library.link-recognized','linkAll geeft alle kandidaten met suggestedPoolId aan dezelfde linkRecognizedItems-actie door; het label benoemt de meervoudige scope.')
reuse('964ad27e669abe58','object.rename','Pencil heropent de naameditie van een nog niet vastgelegde bibliotheek; de globale bibliotheek wordt pas bij het hele formulier toepassen gemaakt.')
reuse('10b7d59df23d3c54 f2b19427c8f5540c','data.discard','cancelNewCompany laat het lokale bibliotheekconcept vallen en wist de nieuwe naam; bestaande bibliotheken blijven behouden.')
reuse('f4c006ab175d1b68','planning.dependency-add','commitDraft roept createRelationDraftWithFeedback aan met gekozen voorganger/opvolger, type en vertraging; Check is een toevoegactie, geen success-status.')
reuse('135cece802ce7530','edit.delete','removeSequence verwijdert alleen de gekozen afhankelijkheidsrelatie; de twee taken blijven bestaan.')
reuse('eebf569c71e4af6d','ui.close','Verlaat het lokale relatieconcept via setDraft(null), zonder een relatie te maken.')
reuse('5422f44c7c53539e','planning.driving','Zap is de vaste aanduiding bij een sturende relatie volgens de berekende uitkomst; geen relatie-tekenmodus of stroomgereedschap.')


def page(c):box(c,3,3,18,18)
def gauge(c,x=10,y=10,r=7):
    c.circle(x,y,r)
    for angle in (180,225,270,315,0):
        a=math.radians(angle)
        c.line([(x+(r-1)*math.cos(a),y+(r-1)*math.sin(a)),(x+(r-2.5)*math.cos(a),y+(r-2.5)*math.sin(a))],radius=0)
def book(c):
    c.line([(3,21),(3,3),(18,3),(18,10)],radius=.3)
    c.line([(3,21),(10,21)],radius=0);c.line([(8,3),(8,21)],radius=0)
def field(c):
    page(c);c.line([(7,8),(14,8)],radius=0)
def columns(c):
    box(c,3,3,15,18)
    for x in (8,13):c.line([(x,3),(x,21)],radius=0)
def extend(c,key):
    if key not in KEYS:return False
    if key=='diagnostics.benchmark':
        gauge(c,12,12,9);c.line([(12,12),(17,7)],True,radius=0);c.circle(12,12,1,True,True)
    elif key=='diagnostics.run-benchmark':
        gauge(c);c.line([(10,10),(14,6)],radius=0)
        c.line([(17,14),(23,18),(17,22)],True,closed=True,radius=.3)
    elif key=='guide.compact':
        box(c,2,5,20,14);c.line([(2,9),(22,9)],radius=0)
        c.line([(6,13),(11,13)],radius=0);c.line([(6,16),(10,16)],radius=0)
        c.line([(14,15),(18,11),(22,15)],True,radius=.3)
    elif key in ('status.schedule-preview','status.schedule-last-result'):
        field(c)
        if key=='status.schedule-preview':
            c.line(arc_points(16,16,4,200,520,28),radius=0)
            c.line([(11,15),(12,18),(15,17)],radius=.3)
        else:
            c.circle(16,16,4);c.line([(16,13),(16,16),(18,16)],radius=.3)
    elif key=='table.column-add-menu':
        columns(c);c.plus(20,17,3)
    elif key=='table.columns-reset':
        columns(c);turn(c,17,17,4)
    elif key=='status.column-present':
        page(c);c.line([(10,3),(10,21)],radius=0);c.line([(3,9),(21,9)],radius=0)
        c.line([(12,15),(15,18),(19,12)],radius=.3)
    elif key=='planning.profile-new':
        page(c)
        for y in (7,12):
            c.circle(8,y,1);c.line([(12,y),(17,y)],radius=0)
        c.plus(18,19,3)
    elif key=='help.context-hint':
        c.line([(3,3),(21,3),(21,17),(12,17),(7,22),(7,17),(3,17)],closed=True,radius=.5)
        c.circle(12,7,.65,False,True);c.line([(12,10),(12,14)],radius=0)
    elif key=='library.link-recognized':
        book(c)
        c.line([(11,15),(14,12),(18,16),(15,19)],True,closed=True,radius=.5)
        c.line([(15,11),(18,8),(22,12),(19,15)],True,closed=True,radius=.5)
    elif key=='status.library-item-missing':
        book(c);c.circle(17,17,4);c.line([(14,17),(20,17)],radius=0)
    elif key=='status.library-item-deviated':
        book(c)
        for y in (14,19):c.line([(13,y),(21,y)],radius=0)
        c.line([(14,22),(20,11)],radius=0)
    elif key=='status.library-suggestion':
        box(c,2,6,6,12);box(c,16,6,6,12)
        c.line([(9,12),(15,12)],radius=0);c.line([(12,9),(15,12),(12,15)],radius=.3)
    elif key=='input.confirm-draft':
        field(c);c.line([(10,15),(14,19),(21,11)],True,radius=.3)
    elif key in ('status.install-size-smaller','status.install-size-larger'):
        box(c,3,3,12,18);c.line([(3,8),(15,8)],radius=0)
        c.line([(20,4),(20,20)],radius=0)
        if key.endswith('smaller'):c.line([(17,17),(20,20),(23,17)],radius=.3)
        else:c.line([(17,7),(20,4),(23,7)],radius=.3)
    return True
