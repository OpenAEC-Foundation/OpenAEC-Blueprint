"""PDF library navigation and v3 controls, traced through the native callbacks."""
from b2_second_series import box
from b2_bulk_series import page
from b2_reports_completion import glyph
from b2_font_geometry import font_sources
from b2_session_two import dimension_arrow
from b2_energy_pile_audio import arc_points

GROUPS = {107: 'Symboolbibliotheekcategorieën', 108: 'Basiszoom en paginahoogte', 109: 'Assistentopdrachten voor PDF'}
ROWS = [
    (107, 'symbol.category-electric', 'Elektrotechnische symbolen', 'De categorie NL Elektra in de symboolbibliotheek in- of uitklappen; geen aansluitpunt plaatsen.', '7eeef82122190ba4'),
    (107, 'symbol.category-site', 'Bouwplaatssymbolen', 'De categorie NL Bouwplaats in de symboolbibliotheek in- of uitklappen; geen bouwkraan plaatsen.', '9880d66d102acd2d'),
    (107, 'symbol.category-plumbing', 'Sanitaire symbolen', 'De categorie NL Sanitair in de symboolbibliotheek in- of uitklappen; geen closet plaatsen.', 'c6fd1c99f5df440d'),
    (107, 'symbol.category-kitchen', 'Keukensymbolen', 'De categorie NL Keuken in de symboolbibliotheek in- of uitklappen; geen keukenblok plaatsen.', '87d7f3ddca4c62e7'),
    (107, 'symbol.category-nen1414', 'NEN 1414-symboolcategorie', 'Vaste categorieaanduiding bij de NEN 1414-groepen; het gedeelde N-beeldmerk staat niet voor een concreet veiligheidssymbool.', '23fb113d608b95b0'),
    (107, 'symbol.category-custom', 'Eigen symboolgroep', 'De opgeslagen eigen symboolgroep in de bibliotheek aanduiden en in-/uitklappen; het plusvormige bronicoon voegt hier geen groep toe.', '4c678249cc4f6427'),
    (108, 'view.zoom-default', 'Standaardzoom', 'De appbasiszoom herstellen: PDF v3 gebruikt 1.0 bij basisrenderbreedte 1100 pixels; Planner gebruikt dagbreedte 30. Geen fysieke 1:1-weergave.', '8f232b44904078e1'),
    (108, 'view.fit-height', 'Paginahoogte passend', 'PDF v3 fit-page berekent uitsluitend de zoom uit vensterhoogte en pagina-aspect; brede pagina’s kunnen horizontaal buiten beeld blijven.', '85b3e80ec5fdccc7'),
    (109, 'assistant.translate', 'Documentvertaling vragen', 'De vertaalprompt via AssistantPanel.send aan de beschikbare assistentprovider aanbieden; nog geen gegarandeerd vertaald uitvoerbestand.', '501ea7f81bdc4783'),
    (109, 'assistant.summarize', 'Documentsamenvatting vragen', 'De samenvattingsprompt via AssistantPanel.send aanbieden; het antwoord verschijnt in het gesprek.', '078297abc6f021bb'),
    (109, 'assistant.draw', 'Tekenopdracht voorbereiden', 'De tekenprompt in het invoerveld zetten en focus geven; de gebruiker vult de opdracht aan vóór verzenden.', '3aabea18d9fde5a0'),
    (109, 'assistant.detect-doors', 'Deurherkenning vragen', 'De opdracht voor het herkennen en markeren van deuren aan de assistent aanbieden; geen lokale detector direct uitvoeren.', '011ddd1d3c6de08d'),
    (109, 'assistant.structural-layout', 'Constructieopdracht voorbereiden', 'De prompt voor draagstructuur/stramien in het invoerveld klaarzetten; vraagt nog een opgave en verzendactie.', '145636ac56ebecae'),
    (109, 'assistant.structural-overview', 'Constructieoverzicht voorbereiden', 'De constructieoverzichtprompt klaarzetten voor bron, bouwlagen en constructieprincipe; nog niets op het blad plaatsen.', 'b85952b89c423b91'),
    (109, 'assistant.floorplan', 'Plattegrondopdracht voorbereiden', 'De plattegrondprompt klaarzetten en het invoerveld focussen; nog geen wand of ruimte maken.', '562c2227d9c0759e'),
]
KEYS = {r[1] for r in ROWS}
TYPOGRAPHY = {key: {**font_sources()['format.color'], 'glyph': ch,
                   'purpose': 'Vaste cijfer-/lettercontour uit Space Grotesk Medium.'}
              for key, ch in [('symbol.category-nen1414', 'N'), ('view.zoom-default', '1'), ('assistant.translate', 'A')]}
ACCENT_FRONT = {k: 'De categorieaanduiding of zoommarkering blijft vóór de dragende contour zichtbaar.' for k in KEYS}
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


reuse('fa30399f5ee5ffae', 'category.building',
      'NL IFC Bouw is een vaste categorieaanduiding bij de inklapbare bibliotheekgroep met wanden, vloeren en profielen; geen IFC-bestand importeren of gebouw invoegen.')
reuse('4b5cd4c0d1e2f292', 'view.zoom-default', 'Tweede bronwaarneming van dezelfde zoom-100 callback; AppWindow.set-zoom(1.0).')
reuse('6027577914e087fd', 'view.fit-height', 'Tweede bronwaarneming van dezelfde fit-page-knop; AppWindow berekent alleen de hoogteverhouding.')
reuse('0fc2d7ce21ccbc05 afa908d8bc05a523 1c492c3a4142bc08 5d084be79dfe69d9', 'file.open',
      'Backstage.do-open -> AppWindow.open-file -> Rust on_open_file opent de native PDF-bestandskeuze en laadt het document in een nieuwe tab.')
reuse('588bb8b819661545 0e5dcf1a2495a368 824d7c1cf84753d9 5f708da3b34a5ffd', 'ui.close',
      'De Bestand- of Voorkeuren-overlay sluiten door backstage-open/prefs-open false te zetten; het appvenster blijft open.')
reuse('6c1ea39c5f79829f 78b141cfb8d23596', 'project.forget-recent',
      'RecentRow.remove -> remove-recent -> Rust verwijdert alleen de lijstverwijzing, slaat instellingen op en bouwt de lijst opnieuw op.')
reuse('15b703033adbef87 b71627049c6c1125', 'document.close',
      'DocTabBar.close -> close-doc -> Rust close_tab sluit het gekozen document; geen venster sluiten.')
reuse('3fc2fd7faf7458ed 89d0ea9e30b013d4', 'window.close',
      'Backstage.do-exit -> Rust bewaart venstergrootte en beëindigt de app via quit_event_loop.')
reuse('06ec2031a8bdee82 9420ee4228c6072b 58e643f54cb727dd ea8d8fc01ea74ad3', 'ui.settings',
      'Backstage opent de voorkeuren; General toont de werkende velden voor auteur, taal, thema en sessieherstel. Rust save-prefs schrijft deze waarden naar instellingen.')
reuse('c1bc34aa6366dba6 47db44fe6f681e6c', 'project.recent',
      'De Recent Files-keuze zet active-mid=0 en toont de werkelijk gevulde recente PDF-bestandenlijst. De overige drie middenkeuzes tonen alleen Coming soon.')
reuse('9ccb66028b3b1538 c3db8e33b53534d7', 'view.search',
      'Vaste zoekaanduiding naast LineEdit; edited -> filter-recents -> Rust rebuild_recents filtert de recente bestanden.')
reuse('6f169863f98accd5 924d56cf432f1983', 'view.zoom-in', 'Ribbon.zoom-in -> set-zoom(zoom*1.25), begrensd en doorgegeven aan render-engine.')
reuse('36aecaccfa18755c abd1a4309db42b00', 'view.zoom-out', 'Ribbon.zoom-out -> set-zoom(zoom/1.25), begrensd en doorgegeven aan render-engine.')
reuse('7f21cbf4c49f0d04 47ddaac10ebb824a', 'view.fit-width', 'AppWindow.fit-width berekent de zoom uit flick.width-24 en de basisrenderbreedte.')
reuse('a512da16e5b3bede c71b5fe6f2c47110', 'page.first', 'first-page -> goto-page(1); Rust begrenst en past scrollpositie aan.')
reuse('3c9c50856d22bbbd 72ff9d54754a23f6', 'page.previous', 'prev-page -> goto-page(current-page-1); Rust kiest de vorige documentpagina.')
reuse('5ab0d528cb1d76f5 f4ba20e27633ccd2', 'page.next', 'next-page -> goto-page(current-page+1); Rust kiest de volgende documentpagina.')
reuse('ed3d2146ae6529a9 7ea98b0dcc6d0690', 'page.last', 'last-page -> goto-page(total-pages); Rust kiest de laatste documentpagina.')
reuse('3a0ae3820daaaf53 24fcc9f1308f1f03', 'page.view-single', 'set-display-mode(0) -> AppWindow toont alleen de huidige pagina en vernieuwt de render.')
reuse('79eb2340ae2e5e11 908114ad36110b9a', 'page.view-continuous', 'set-display-mode(1) -> AppWindow toont de pagina’s onder elkaar, reset scroll en vernieuwt de render.')

exclude('97d588bf983f731e 6a2743ce23d77346 e475b1678620a1f7 8c33b75dfe3f8156 3ffe8ab1304e7612 46fe3787b1b112ec fdcd8978885f3f35 3d95a0bf8a772b8a d90ab819338f1063 5e67ae2e04e9a916 d9b46402f3d0ffc6 6bcd13952130b162 b43e866c0e2c27df e1aa30058fce116c 1d67aee7bfa5aa31 db250a1a6de2a7d8 a656b99be1d7ace2 f42a2ddfd73e31b9 442994e5e504f135 2151a565f2d471e0 66bf9b44418b0ac9 67a83a2465601268 544e8f045e50e77f 06b6527a513dd053 950f2a2c1c8bb758 8e82e04d48ec010b b3cd2216c58eaf04 2f622da63eeabd80 6ac122d549f9db72 25d3338524767e84 ecebb95f230f592d f181f90b528ec9d3 31d211410c653478 1a8560dfe26018f5 25395a4065fea02e 889399b4bfda7604 a862857861b0ebfd 18a4023786ee2727 598d2ef6dac51ec9 a9379cd17c0d23aa b28a936ab01c560c d0477818bddb9587 e70756742f060fe7 e49d41d2d40652ca 1b8c46aa82c17eda 2d19f249b5d90725 68d5a51777e59855 d62512aacdfba1ad b2b1f2b8ac724dda d31e05832ee97342 cda263d212d16b93 ae704b2491b2cf52 45d6d0ab57e41e99',
        'NL-bibliotheekpreviews tonen de te plaatsen bouwdelen met werkelijke geometrie: wand/vloer/profiel/isolatie, kraan, sanitair of keuken. SymbolPalette toont deze als sym.svg; modelvoorbeelden blijven afzonderlijk van de vaste categorieknoppen.')
exclude('d7ce7db1b2dcb222 84056564c81fef49 2dc63e52f2c911c2 d7b00e97cd842fd1 191a3a06ea50c9b3 7fd3d5c7c8a1732a 3af7907df54c25bb c33bb3f3984d739d 7f05e7d243925e9f ff3e2655e3521eab 9875097ac8cb23f0 de63a82b5fc63ebd 2a70ca64f4dcf586 b5c07d15bf26ae4f 9a4186d7bce9e80a 77164deacfae5f04 91f295c6cf9e1212 cd9945f6fb720881 b35f7325d2b3c83f 9fce86b4738ee0a0 7cde16218c8a52d6 4f89c3efdd5cf223 240d83f064fbdd83 1501c46e125e8abd 815e9fe379f1ae7d',
        'Cursorbadges zijn samengestelde 32px-aanwijzers met pijl en vaste hotspot 1,1 voor hover op annotaties; geen losse 16/24px-bedieningsiconen. De corresponderende gereedschappen worden afzonderlijk beoordeeld.')
exclude('07c1c36803618590 ac6fa6c4adb227ce',
        'Gedraaide resizecursor of gumcursor met schermradius en hotspot; ruimtelijke aanwijzer, geen los gereedschapsicoon.')
exclude('a0442e6dd37e06e4 31c1780a22dd6788',
        'MCP-stempelpayloadfallback of fabrikantlijnwerkpreview; te plaatsen annotatie-inhoud. Geen UI-knop of categorieaanduiding.')
exclude('50579e25bd72be71', 'Een 1px transparant achtergrondpatroon voor PDF-formuliervelden; geen symbool of bedieningsicoon.')
exclude('091793c837d23a6e 3059e41cbfcd69a2 c54ae45040b40761 1423158ad03b8c37 3cffeab81475e554 1dbf046c35bc83dd e4bfa098d7993f02 6ad225e44ba6d096 55202525b89e1048',
        'App-/bestandsbeeldmerk bij favicon, native venster, drag-afbeelding, executablebuild of MCP-pakket; branding buiten de vaste UI-iconen.')


exclude('cec726d54e699c11 d26ed6f237b2fc97 45c6e1a2e1d632c3 99a0f03476aeb192 3de93c072723b977 64ac0f13d1d1258f 5bf45313ad742c9c 24731ede0167842f 633f137c4081d319 ccbcc8a208776a6a 00555b39b5127a5e a0cc1e21225fa48c 4a58d9b8c27d095b 2b226f431a36a7a1 fd300ac73dbb077d da33867ab7a3edc0 d83132de1d946058 30db436dfae3462e d19f7303051548d4 913e94b0037cb688 d31e10f9e1053740 603a73a0861cb505 ca9fde94aab32b41 7202a9d9e5e92285 047e46870138e162 13923920f72f756a c5275b0ad3e72b31 eaec31401ae87495 5b280c18608b8eaa',
        'PDF v3: menu-item roept todo aan of toont Coming soon. AppWindow -> on_action_todo schrijft uitsluitend een niet-geïmplementeerd-melding; pin/nieuwe sessie/URL/plaats en deze bestandshandelingen voeren de genoemde functie niet uit.')
exclude('adb3d1fb92c0c5ca 921142fa8b31a69f 85146ff6d6b25e79 3d72b875fda7bc5f 1e854518f2e4463b f30ad00cb7fd9d5b 29e18476faeea9db 59862eb5b056ec42 defdb57a643409c2 71482050d7372482',
        'PDF v3: deze voorkeurencategorie toont uitsluitend This section is coming soon. Alleen General bevat echte velden; geen inhoudelijke instellingenfunctie voor deze categorie.')
exclude('d8cd0b53fa4b4954 2dfbbd1734f048e0 30893b2fb82940ca dfb97d73e015f881 1fa766179719a15d 5609ad7427edbc05 491b6a255b643d52 a0ba4d1af49eebe4 e17eedc69c5d50cb 0cb2b6fb418882b5 13311e65ab2b839d 33cfae8a1c0d65af 4ca88b521a31ac45 6df7ee5acec27a23 d1bab48d3342520c fc12a98e1d00fe22 5dd7e03fb2f5d16e 9470a01b5baf3003 bf77504098f530ad 6b9047024cd46051 3f88f8f98e5fdf74 8c6000f92b6d43e3 053ce917d54a23f2 d0a2ba4040a5a608 de00a8f491773191 ee48f0db02b6b342 3aea00adc6d0590e ccb0d7d88b62cf4d 0781b98cf44eba8d d59906db43f8b7ff 05b5f4ca3b7060c1 7fd701a3e30bbb82 5266ce44bd01a4e8 89fc107b5652d45b 4d5c66d167091bc4 dbda08d13ad38741 8984ca239e41c11f b657016c7f625c35 f1d2e79c36513a24 ea43f2aa0b2c0c61 f7c328f2d310ccac 87326d32d25e74ed d780487285b85f29 09ed8b648a9ec5bf 1e9a037ddc30b8a7 907491526df0ad25 ef66022ff7efdaac c5325ac6b3d683c9 f9c7b7abf46e2070 6ccd57ce6d058246 bc50f497013ce830 6b415bac44cf1732 c2fd118e6061fd27 2527ad9dedf51a85 00efcbd69ee705bb d102dd065a17ad5f 322dc6b3e76177ff e2b86ceb600e298e f1842366d1efaf09 2f3aa67acf0ea264 ba05220ff7b0dac3 acea9ee9818d374c 5ac180ba179e6843 dce2ca77d3ceb730 9c308c652db276bb d79463e98e64615d',
        'PDF v3: klik gaat via tab-action/select-hand/screenshot/rotate/find naar action-todo, of heeft geen gebonden select-cursor-handler. Rust schrijft alleen een statusmelding; geen annotatie-, selectie-, meet- of paneelbewerking. De werkende zoom-, paginanavigatie- en paginamodusknoppen zijn apart beoordeeld.')
exclude('dcba38bd959ee815 64121367f5cb1f8e',
        'PDF v3: gedeelde has-dropdown-chevron wordt uitsluitend bij de Screenshot-placeholder getoond; geen werkend menu. Screenshot -> action-todo.')


def sparkle(c, x=19, y=5):
    c.line([(x, y-3), (x+1, y-1), (x+3, y), (x+1, y+1),
            (x, y+3), (x-1, y+1), (x-3, y), (x-1, y-1)], True, closed=True, radius=.2)


def extend(c, key):
    if key not in KEYS:
        return False
    if key == 'symbol.category-electric':
        c.line([(3, 4), (3, 20), (21, 20)], radius=.4)
        c.line([(13, 2), (7, 12), (12, 12), (10, 21), (18, 9), (13, 9)], True, closed=True, radius=.2)
    elif key == 'symbol.category-site':
        c.line([(9, 21), (9, 3), (21, 3)], radius=.3)
        c.line([(4, 21), (14, 21)], radius=0)
        c.line([(4, 7), (21, 7)], True, radius=0)
        c.line([(18, 7), (18, 15), (21, 15), (21, 13)], True, radius=.5)
    elif key == 'symbol.category-plumbing':
        box(c, 3, 3, 7, 8)
        c.line([(3, 11), (3, 15), (6, 19), (17, 19), (21, 14), (21, 11)], radius=.5)
        c.line([(10, 11), (21, 11)], True, radius=0)
        c.line([(10, 19), (10, 22), (18, 22)], radius=.3)
    elif key == 'symbol.category-kitchen':
        box(c, 2, 5, 20, 15)
        c.line([(2, 14), (22, 14)], radius=0)
        c.line([(12, 14), (12, 20)], radius=0)
        for x in (7, 17):
            c.circle(x, 10, 2.2, True)
    elif key == 'symbol.category-nen1414':
        box(c, 3, 3, 18, 18)
        glyph(c, 'N', 7, 7, 10, 10, True)
    elif key == 'symbol.category-custom':
        c.line([(2, 7), (2, 20), (22, 20), (22, 7), (11, 7), (9, 4), (2, 4)], closed=True, radius=.4)
        c.line([(12, 9), (17, 14), (12, 19), (7, 14)], True, closed=True, radius=.3)
    elif key == 'view.zoom-default':
        c.circle(10, 10, 7)
        c.line([(15, 15), (22, 22)], radius=0)
        glyph(c, '1', 8, 6, 4, 8, True)
    elif key == 'view.fit-height':
        page(c, 9, 3, 12, 18)
        c.line([(3, 3), (3, 21)], True, radius=0)
        c.line([(1, 6), (3, 3), (5, 6)], True, radius=.2)
        c.line([(1, 18), (3, 21), (5, 18)], True, radius=.2)
    elif key == 'assistant.translate':
        glyph(c, 'A', 2, 7, 8, 12)
        c.line([(13, 7), (22, 7), (19, 4)], True, radius=.3)
        c.line([(22, 17), (13, 17), (16, 20)], True, radius=.3)
    elif key == 'assistant.summarize':
        page(c, 2, 3, 12, 18)
        for y in (7, 11, 15):
            c.line([(5, y), (10, y)], radius=0)
        c.line([(16, 9), (19, 12), (16, 15)], True, radius=.2)
        c.line([(21, 12), (22, 12)], True, radius=0)
    elif key == 'assistant.draw':
        c.line([(3, 16), (13, 6), (17, 10), (7, 20), (2, 21)], closed=True, radius=.3)
        c.line([(10, 9), (14, 13)], radius=0)
        sparkle(c, 20, 4)
    elif key == 'assistant.detect-doors':
        c.line([(4, 21), (4, 4), (14, 4), (14, 21)], radius=.3)
        c.line([(4, 21), (12, 16), (12, 7), (4, 4)], radius=.3)
        c.line([(18, 2), (22, 2), (22, 7)], True, radius=.3)
        c.line([(18, 22), (22, 22), (22, 17)], True, radius=.3)
    elif key == 'assistant.structural-layout':
        for x in (4, 11, 18):
            c.line([(x, 10), (x, 21)], radius=0)
        for y in (10, 16, 21):
            c.line([(4, y), (18, y)], radius=0)
        sparkle(c, 19, 4)
    elif key == 'assistant.structural-overview':
        page(c, 2, 7, 13, 15)
        c.line([(5, 4), (18, 4), (18, 8)], radius=.4)
        c.line([(5, 12), (12, 12), (12, 18), (5, 18)], True, radius=.3)
        sparkle(c, 19, 13)
    elif key == 'assistant.floorplan':
        box(c, 2, 8, 17, 14)
        c.line([(2, 15), (10, 15), (10, 8)], radius=.3)
        c.line([(14, 15), (19, 15)], radius=0)
        sparkle(c, 19, 4)
    return True
