"""Reviewed Reports controls: original vectors, with explicit source-record decisions."""
from b2_second_series import box
from b2_bulk_series import page
from b2_session_two import dimension_arrow
from b2_energy_pile_audio import arc_points
from b2_font_geometry import letter_contours, font_sources

GROUPS={56:'Account en beheer',57:'Rapportinhoud',58:'Tabellen en formulieren',
        59:'Rapportorganisatie',60:'Rapportweergaven',61:'Locatie en documentuitvoer'}
ROWS=[
 (56,'account.login','Aanmelden met SSO','loginWithSso start de SSO-aanmeldroute.','666617ca3d059ad5'),
 (56,'account.profile','Mijn account','De externe accountpagina openen; geen accountmenu of afmeldactie.','78c0c9a05cc7ca43'),
 (56,'account.admin','Beheeromgeving','onAdmin opent de beheeromgeving voor een beheerder.','1018237a0e8e8455'),
 (56,'account.logout','Afmelden','logout beeindigt de aanmeldsessie; geen venster sluiten.','3a00defe1c26d317'),
 (57,'report.text-block','Tekstblok invoegen','addBlock(paragraph) voegt een rapporttekstblok in.','748390ed7f926509'),
 (57,'report.calculation-block','Rekenblok invoegen','addBlock(calculation) voegt een rapportberekeningsblok in.','5109c3a825475909'),
 (57,'report.check-block','Toetsblok invoegen','addBlock(check) voegt een toetsblok in; dit is geen geslaagd-status.','9137a21c988c4570'),
 (57,'report.table-block','Tabelblok invoegen','addBlock(table) voegt een tabelblok in; geen spreadsheetblok.','6b13080726f40d5e'),
 (57,'report.spreadsheet-block','Spreadsheetblok invoegen','addBlock(spreadsheet) voegt het bewerkbare spreadsheetblok in.','b8d85e9c04723f78'),
 (57,'report.image-block','Afbeeldingsblok invoegen','addBlock(image) voegt een rapportafbeeldingsblok in.','ed572d79795d5a14'),
 (57,'report.map-block','Kaartblok invoegen','addBlock(map) voegt een kaartblok in; geen kaartpunt plaatsen.','94f4b0c83bd92856'),
 (57,'report.list-block','Opsommingsblok invoegen','addBlock(bullet_list) voegt een opsommingsblok in.','ea9ff4a4783b3c37'),
 (57,'report.heading-block','Subkop invoegen','addBlock(heading_2) voegt een H2-subkop in.','48fd976e20a90fca'),
 (57,'report.spacer-block','Witruimte invoegen','addBlock(spacer) voegt een verticale witruimte in.','29d037327a3bf156'),
 (57,'report.page-break','Pagina-einde invoegen','addBlock(page_break) voegt een expliciet pagina-einde in.','ca96995d5ddc93d5'),
 (57,'report.block-menu','Inhoudsblok kiezen','De bloktypenkiezer openen; de keuze voegt pas daarna een blok toe.','89d5daf101550459'),
 (58,'list.item-add','Opsommingsitem toevoegen','addItem voegt een item toe aan de huidige opsomming.','9fd6bf010cc7db83'),
 (58,'table.merge-cells','Cellen samenvoegen','mergeCells bewaart het geselecteerde rechthoekige celbereik als een samengevoegde cel.','ebf37c744b0a634e'),
 (58,'table.split-cells','Celsamenvoeging opheffen','unmergeCells verwijdert de samenvoeging van de actieve cel; geen willekeurige tabel splitsen.','08d986912affc8d4'),
 (58,'ui.dropdown','Keuzemenu openen','ThemedSelect schakelt het menu met bestaande keuzeopties.','c92c343814718b2b'),
 (58,'content.drag','Inhoud verslepen','Sleephandvat voor het herordenen van inhouds- of layout-items, zoals rapportblokken, hoofdstukken, bijlagen of kolommen.','32d487fccddff39e'),
 (58,'form.field-add','Gegevensveld toevoegen','addExtraField voegt een extra veld toe aan het voorbladformulier.','f867f857aa27fc84'),
 (58,'table.row-add','Tabelrij toevoegen','handleAddRow voegt een rij toe aan de actieve tabelveldgroep.','8ed68aa61ee4e2c6'),
 (58,'form.field-group','Veldgroep','Aanduiding bij een gewone formuliergroep; geen tabelgroep of nieuwe veldactie.','9a8147a53a6ef497'),
 (59,'report.chapter-add','Rapporthoofdstuk toevoegen','addNewSection voegt een rapporthoofdstuk toe; geen begrotingshoofdstuk.','febc928aace343e8'),
 (59,'report.appendix-add','Rapportbijlage toevoegen','addNewAppendix voegt een rapportbijlage als inhoudsstructuur toe; geen bestand bijvoegen.','523c48707977c3ce'),
 (59,'report.revision-add','Rapportrevisie toevoegen','addRevision voegt een revisieregel toe aan het colofon.','ae01c23637299b40'),
 (59,'report.properties','Rapportinstellingen','Het paneel met rapportmetadata, project en sjabloon openen.','1a7d814eac41b357'),
 (59,'report.cover','Rapportvoorblad','Het voorbladpaneel openen.','a5954fa31c7e58dc'),
 (59,'report.colophon','Rapportcolofon','Het colofonpaneel met documentverantwoording openen.','17a1bb60bc9466d8'),
 (59,'report.validate','Rapport controleren','onValidate laat de rapportdefinitie controleren; geen IFC-model valideren.','07694e578e0da59b'),
 (59,'report.options','Rapportopties','Het paneel met rapportspecifieke uitvoeropties openen; geen algemene appinstellingen.','e6673dae03ea638b'),
 (59,'report.catalog','Alle rapporten','Het projectfilter opheffen en alle rapporten ophalen.','2cc61a81dc2d779c'),
 (59,'report.move-project','Rapport naar project','Het menu voor het verplaatsen van een rapport naar een project openen.','0679c299aab61cbb'),
 (59,'report.unlink-project','Rapport uit project','handleMoveReport met null verwijdert de projecttoewijzing van het rapport.','4e6f28fa2f57b2fb'),
 (60,'view.report-editor','Rapporteditor','setMode(editor) toont alleen de rapporteditor.','b36c19d0e8e421e1'),
 (60,'view.report-split','Editor en voorbeeld','setMode(split) toont editor en rapportvoorbeeld naast elkaar.','89853e98efbb3a84'),
 (60,'view.report-json','Rapport als JSON','setMode(json) toont de rapportdefinitie als JSON.','72673248a49a3fd0'),
 (60,'view.report-preview','Rapportvoorbeeld','De rapportvoorbeeldweergave openen via setMode(preview) of toonVoorbeeld(null, rapport); geen bestand schrijven.','7c8d9c5ee811e4e7'),
 (61,'location.select','Locatie kiezen','Een adresvoorstel selecteren en coordinaten vastleggen in het kaartblok.','6519bbc77505ca04'),
 (61,'geo.cadastral','Kadastergegevens ophalen','lookupCadastral haalt perceelgegevens op voor de gekozen coordinaten.','5391a219dde49812'),
 (61,'file.download','Gegenereerd bestand downloaden','downloadPdf haalt het reeds gegenereerde PDF-resultaat op; geen nieuwe PDF genereren.','6af33617f5b02660'),
 (61,'document.close','Document sluiten','Het gekozen document of rapport sluiten; de applicatie blijft open. Reports/Heatloss resetten het huidige document, Geotechniek sluit de gekozen tab en bijbehorende cache.','55aa1761478de9a0'),
 (61,'server.storage','Serveropslag','Bestemmingsaanduiding voor opslag en openen van rapporten op de server; geen GPU-instellingen.','f2b9ef9eb7eacbdd'),
 (61,'file.local','Lokaal bestand','Bestemmingsaanduiding voor lokale rapportbestanden; geen eigenschappendialoog.','7322b3ef1f7d2647'),
 (61,'feedback.github-issue','GitHub-issue voorbereiden','handleSubmit opent een vooraf ingevuld GitHub-issueformulier; publiceert het issue nog niet.','5481ae8b0e72df53'),
]
KEYS={k for _,k,_,_,_ in ROWS}
ACCENT_FRONT={k:'De richting of markering loopt ononderbroken voor de contour.' for k in ('account.login','account.logout','report.check-block','report.move-project')}
TYPOGRAPHY={'report.heading-block':{**font_sources()['format.color'],'glyph':'H2',
                                 'icon_transform':'H and 2 fitted to separate optical boxes'}}
REUSED={
 'fd075b03be024a7d':('report.table-block','De Invoegen-tab roept eveneens addBlock(table) aan; dit lost de eerdere tabelweergaveverwarring op.'),
 '0d486f39fa39c30d':('status.busy','App-laadindicator met animate-spin.'),
 '3d441188e7775a15':('status.busy','Voortgangsindicator van de merkextractiewizard.'),
 'd543ffa6a8de17c0':('status.busy','Laadtoestand bij merkbeheer.'),
 'fb538c55754c866b':('status.busy','Laadtoestand bij sjabloonbeheer.'),
 'c2926af3623a58b6':('status.busy','Spinner-component in sjabloonbeheer.'),
 '7564d3818bd5897a':('status.busy','Laadtoestand bij tenantbeheer.'),
 'b764aeea3ad4f98e':('status.busy','Gedeelde LoadingSpinner.'),
 '1ca179f0846e54f9':('edit.delete','onDelete verwijdert de huidige YAML-zone.'),
 '0a8598276842a7b5':('edit.delete','removeItem verwijdert het gekozen opsommingsitem.'),
 '6993c31d64aaac68':('view.search','Zoekaanduiding bij het adresveld; de invoer vraagt adresvoorstellen op.'),
 '64908e696a6fd164':('status.success','Resolved location bevestigt de gekozen naam en coordinaten.'),
 '875fac1d1602f3dc':('selection.mark','Vinkje in de geselecteerde kaartlaagoptie, geen processtatus.'),
 'b05e61c436475b5b':('status.busy','De ophalentoestand van dezelfde kadastrale knop.'),
 '2a5ef35a90b6cff8':('geo.cadastral','Aanduiding naast de daadwerkelijk opgehaalde perceelgegevens.'),
 'cbe2299487228d68':('edit.delete','removeCadastral wist de perceelgegevens binnen het kaartblok.'),
 '01beb1d3fc9bf5e2':('tree.expand','De chevron toont of verbergt de handmatige coordinatenvelden.'),
 '20934c6ab6fda994':('format.align-left','IconAlignLeft wordt gebruikt door de setAlignment(left)-knop.'),
 '6a6e12a7580cb9ca':('format.align-center','IconAlignCenter wordt gebruikt door de setAlignment(center)-knop.'),
 '7a4dd20b173716e5':('format.align-right','IconAlignRight wordt gebruikt door de setAlignment(right)-knop.'),
 '68fccc006cb93575':('format.fill-color','De kleurkiezer stelt bg_color van de geselecteerde cellen in; het label geeft de celscope.'),
 '0dd522fb374316aa':('file.save','De titelbalk roept onSave aan.'),
 '558a086af3ead383':('edit.undo','De titelbalk roept undo aan.'),
 '115a8c9468f1faf6':('edit.redo','De titelbalk roept redo aan.'),
 'bac56e793804e1b2':('ui.settings','onSettingsClick opent appvoorkeuren.'),
 '13ea976ddec9caa9':('account.menu','De gebruikersknop schakelt menuOpen.'),
 '5b16fcec376b2ffd':('link.open-external','Externe-linkindicator naast Mijn account.'),
 'b93475a880399caf':('ui.settings','Externe SSO-instellingen; het label en de linkindicator blijven expliciet.'),
 '527403aa70c09196':('link.open-external','Externe-linkindicator naast SSO-instellingen.'),
 '24f66314e97b43c1':('file.new','De Bestand-nieuwactie roept handleNew aan, met bevestiging bij onopgeslagen werk.'),
 '8a128be15c300774':('file.open','Bestand Openen bevat de lokale JSON-bestandskeuze en serverrapportkiezer.'),
 '838ec6302fedcf4a':('file.save','handleSave bewaart op de server of lokaal afhankelijk van de sessie.'),
 '6b55a8971c7d6e6c':('file.save-as','Opslaan als maakt een andere rapportidentiteit of lokale kopie.'),
 '6fa474f836a59b05':('ui.settings','Bestand-voorkeuren opent de appinstellingen.'),
 '95242aadbd7b879a':('ui.about','Bestand-Over toont het About-paneel.'),
 '3d71155394066901':('nav.back','De Bestand-terugknop sluit Bestand en keert terug naar de werkruimte.'),
 '88bcb25a26b3d77c':('ui.close','De web-Exit-aanroep sluit alleen het Bestand-paneel; geen appafsluiting implementeren.'),
 'c6a85ee6e8c1abf2':('ui.close','De concrete Afsluiten-menuplaats doet in webmodus alleen onClose.'),
 'bf4e45ef81822d95':('report.text-block','De Invoegen-tab roept ook addBlock(paragraph) aan.'),
 'dbe927642b52c955':('report.calculation-block','De Invoegen-tab roept ook addBlock(calculation) aan.'),
 'b1a05727361ca28b':('report.check-block','De Invoegen-tab voegt hetzelfde toetsblok in.'),
 '2cf2c4987b6fdbce':('report.image-block','De Invoegen-tab voegt hetzelfde afbeeldingsblok in.'),
 '0e89e679b3551fd0':('report.map-block','De Invoegen-tab voegt hetzelfde kaartblok in.'),
 'f29bcf04f8000f56':('report.list-block','De Invoegen-tab voegt hetzelfde opsommingsblok in.'),
 '6f4803f4828a7eac':('report.heading-block','De Invoegen-tab voegt dezelfde H2-subkop in.'),
 '40fa4f16fa3bdafd':('panel.left','onToggleSidebar schakelt het navigatiezijpaneel.'),
 'a8d63ef9e428033b':('ui.dropdown','De keuzeknop opent het themamenu; de opties bepalen het gekozen thema.'),
 '35a5e9eeb5cc61be':('edit.duplicate','duplicateAppendixBlock dupliceert het gekozen bijlageblok.'),
 '49d5d7c16c0afc4a':('edit.delete','removeAppendixBlock verwijdert het gekozen bijlageblok.'),
 'cb8a1fa4ac0f9f2c':('status.info','Informatieve tekst over het voorbereiden van een GitHub-issue.'),
 '08139ecf57c64657':('edit.delete','onRemove verwijdert de gekozen revisieregel.'),
 '6e8e7a1574e2551f':('edit.delete','removeImage wist de voorbladafbeelding.'),
 'a279df41ce739236':('edit.delete','onRemove verwijdert het extra gegevensveld.'),
 '056142659a8a4646':('edit.delete','removeFlatTableRow verwijdert de gekozen tabelrij.'),
 '411c1b4679faf0cd':('data.table','Indicator bij een tabelveldgroep; geen nieuw tabelblok.'),
 '559411c5f1039f93':('report.properties','De formulierkop toont dezelfde rapportmetadata-instellingen.'),
 'c547fe146a8a02f6':('status.warning','Bevestigingswaarschuwing: sjabloon wijzigen wist het huidige rapport.'),
 '585f8a04e188f7d1':('status.busy','Spinner tijdens sjabloonladen.'),
 'fca74f8b2831b708':('status.success','Toast met type success.'),
 '4e3b1649b1eeea18':('status.error','Toast met de foutvariant.'),
 '0f776c63d3f21441':('status.error','Fouttoestand van de editor, ook al gebruikt de bron een driehoek.'),
 'b6c54c8e2150d48b':('content.drag','Het hoofdrapport gebruikt hetzelfde sleephandvat voor blokvolgorde.'),
 '5cdc68bb13a0cea5':('edit.duplicate','duplicateBlock dupliceert het gekozen blok.'),
 'd03a5a88487a5dae':('edit.delete','removeBlock verwijdert het gekozen blok.'),
 '5ad1603640669b42':('panel.left','setExpanded(true) toont het navigatiepaneel.'),
 '889690e919bdf76d':('panel.left','setExpanded(false) verbergt hetzelfde navigatiepaneel.'),
 'a4c2b762810b0484':('status.busy','Voortgang bij rapportgeneratie.'),
 'b7e03caa6d67e9ed':('report.generate','generatePdf genereert opnieuw het huidige rapport.'),
 '6b93003bf43149e9':('tree.expand','onToggleCollapse bedient een hoofdstuktak.'),
 '5da1ff9aafb9b914':('content.drag','Hoofdstuk-sleephandvat met dezelfde drag-and-dropbetekenis.'),
 'de59bbb8947960cf':('edit.delete','onRemove verwijdert het gekozen rapporthoofdstuk.'),
 '70276241719a6d9c':('content.drag','Bijlage-sleephandvat met dezelfde drag-and-dropbetekenis.'),
 '1ef650253bbc8d38':('edit.delete','onRemove verwijdert de rapportbijlage.'),
 '2032c6b14bfe25f2':('data.table','De tabelvariant van een veldgroep in de navigatie.'),
 '7077238accef5376':('form.field-group','De gewone veldgroepvariant in dezelfde navigatie.'),
 '85d08d25f9f540fe':('report.chapter-add','De navigatieknop roept ook addNewSection aan.'),
 'b34db0cf6fafae3e':('report.appendix-add','De navigatieknop roept ook addNewAppendix aan.'),
 'ac7ec27dc3e98db6':('ui.close','clearValidation sluit de validatiemelding.'),
 '7d03c095e06d96c0':('status.busy','Laadindicator bij het ophalen van projecten.'),
 '8d7dbb05dcfa2a76':('project.folder','Het doelproject in het verplaatsmenu is een projectmapindicator.'),
 '408a3085ed5ca969':('edit.delete','De rapportknop opent de bevestiging voor het betreffende rapport.'),
 'e30058b2f8ac7a82':('project.folder','Aanduiding naast een projectnaam in de projectkiezer.'),
 '13480987e22f9c48':('edit.delete','De projectverwijderknop roept onDelete aan.'),
 '77b16d826965ff26':('report.list-block','De concrete bullet_list-variant is het opsommingstype, geen willekeurige lijst.'),
}
EXCLUDED={
 'fcceb03e8d339055':'Geografische puntmarkering binnen de kaartinhoud; bewerkbare documentinhoud, geen vast bedieningsicoon.',
 '891b9468aa3de7d1':'OpenAEC-beeldmerk in de titelbalk.',
 'a96fc12d3e6755b7':'Ribbon-Plakken heeft hier geen onClick; geen actieve plakkenimplementatie aangetoond.',
 'd3d866709166d4ed':'Kopieer sectie heeft hier geen callback; geen werkende kopieeractie aangetoond.',
 '30324b834362212f':'Grote lege-staatillustratie bij de voorbladafbeelding.',
 '88e2d77118171890':'Grote lege-staatillustratie voor een leeg hoofdstuk.',
 '876d8ba29951349f':'Grote illustratie bij een ontbrekende API-verbinding; de tekst beschrijft de toestand.',
 '8e1b3f5f31ee1d51':'Grote lege-staatillustratie voor een nog niet gegenereerde PDF.',
 'eb6cc5317ba519b4':'Decoratieve grote plus in een lege hoofdstuklijst; de afzonderlijke toevoegknop is beoordeeld.',
 '78fe3bc54f3432ea':'Grote lege-staatillustratie in de rapportkiezer.',
}
# These dispatcher sites show a type-specific icon, not a generic new symbol.
DISPATCHERS={key:('report.text-block','report.calculation-block','report.check-block',
                 'report.table-block','report.spreadsheet-block','report.image-block',
                 'report.map-block','report.list-block','report.heading-block',
                 'report.spacer-block','report.page-break')
             for key in ('fa90755499b56af2','7bc3e4fd1c6bd550','a08f0e275de2975a','3e6719a977efb4a7')}


def glyph(c,letter,x,y,w,h,accent=False):
    contours=letter_contours(letter,'Medium')
    points=[p for ring in contours for p in ring]
    x0=min(p[0] for p in points);x1=max(p[0] for p in points)
    y0=min(p[1] for p in points);y1=max(p[1] for p in points)
    scale=c.size/24
    c.fills.append({'tone':'accent' if accent else 'primary',
                    'rings':[[(scale*(x+(px-x0)*w/(x1-x0)),scale*(y+h-(py-y0)*h/(y1-y0))) for px,py in ring] for ring in contours]})


def person(c,x=9):
    c.circle(x,6,3)
    c.line(arc_points(x,21,6,180,360,24),radius=0)


def sheet(c):page(c,3,2,18,20)


def table(c,spreadsheet=False):
    box(c,3,3,18,18)
    c.line([(3,8),(21,8)],True,radius=0)
    c.line([(3,14),(21,14)],radius=0)
    c.line([(10,3),(10,21)],radius=0)
    if spreadsheet:c.line([(16,3),(16,21)],True,radius=0)


def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key in {'account.login','account.logout'}:
        box(c,3,3,8,18)
        if key=='account.login':dimension_arrow(c,(22,12),(15,12),1.8)
        else:dimension_arrow(c,(15,12),(22,12),1.8)
    elif key=='account.profile':
        person(c,12)
    elif key=='account.admin':
        person(c,7.25);box(c,16,12,7,8,True)
        c.line([(17,12),(17,9),(22,9),(22,12)],True,radius=.7)
    elif key.startswith('report.') and key.split('.')[1].endswith('block'):
        kind=key.split('.')[1]
        if kind=='heading-block':glyph(c,'H',3,4,10,16);glyph(c,'2',15,10,7,10,True)
        elif kind=='table-block':table(c)
        elif kind=='spreadsheet-block':table(c,True)
        elif kind=='image-block':
            box(c,3,3,18,18);c.circle(8,8,2,True)
            c.line([(3,18),(9,12),(13,16),(17,11),(21,16)],True,radius=.5)
        elif kind=='map-block':
            c.line([(3,5),(9,2),(15,5),(21,2),(21,19),(15,22),(9,19),(3,22)],closed=True,radius=.4)
            c.line([(9,2),(9,19)],True,radius=0);c.line([(15,5),(15,22)],radius=0)
        elif kind=='list-block':
            for y in (5,12,19):c.circle(4,y,1.2,True,True);c.line([(9,y),(21,y)],radius=0)
        elif kind=='spacer-block':
            c.line([(3,12),(8,12)],radius=0);c.line([(16,12),(21,12)],radius=0)
            dimension_arrow(c,(12,9),(12,3),2);dimension_arrow(c,(12,15),(12,21),2)
        else:
            sheet(c)
            if kind=='text-block':
                for y,w in ((7,17),(12,17),(17,13)):c.line([(7,y),(w,y)],True,radius=0)
            elif kind=='calculation-block':
                c.line([(8,17),(10,7),(14,7)],True,radius=1);c.line([(7,11),(13,11)],True,radius=0)
                if not small:c.line([(15,13),(18,17)],radius=0);c.line([(15,17),(18,13)],radius=0)
            elif kind=='check-block':c.line([(7,12),(11,16),(18,8)],True,radius=.4)
    elif key=='report.page-break':
        c.line([(3,10),(3,3),(21,3),(21,10)],radius=.5)
        c.line([(3,16),(3,21),(21,21),(21,16)],radius=.5)
        for x in (3,10,17):c.line([(x,13),(x+4,13)],True,radius=0)
    elif key=='report.block-menu':
        for x,y in ((3,3),(14,3),(3,14)):box(c,x,y,7,7)
        c.plus(18,18,3.5,True)
    elif key in {'list.item-add','form.field-add','table.row-add'}:
        if key=='list.item-add':
            for y in (5,11,17):c.circle(4,y,1,filled=True);c.line([(8,y),(14,y)],radius=0)
            c.plus(19,18,3,True)
        elif key=='form.field-add':
            box(c,3,5,18,8);c.line([(6,9),(11,9)],radius=0);c.plus(17,19,3,True)
        else:
            box(c,3,3,18,12);c.line([(3,9),(21,9)],radius=0);c.line([(10,3),(10,15)],radius=0)
            c.plus(12,20,3,True)
    elif key in {'table.merge-cells','table.split-cells'}:
        box(c,2,4,20,16);c.line([(2,12),(22,12)],radius=0)
        if key=='table.merge-cells':
            c.line([(12,12),(12,20)],radius=0)
            dimension_arrow(c,(4,8),(9,8),1.5);dimension_arrow(c,(20,8),(15,8),1.5)
        else:
            c.line([(12,4),(12,20)],radius=0)
            dimension_arrow(c,(9,8),(4,8),1.5);dimension_arrow(c,(15,8),(20,8),1.5)
    elif key=='ui.dropdown':c.line([(5,8),(12,15),(19,8)],radius=.6)
    elif key=='content.drag':
        for x in (8,16):
            for y in (5,12,19):c.circle(x,y,1.5,x==16,True)
    elif key=='form.field-group':
        sheet(c)
        for y in (7,14):
            c.line([(6,y),(10,y)],radius=0);box(c,13,y-1.5,5,4,True)
    elif key in {'report.chapter-add','report.appendix-add','report.revision-add'}:
        page(c,2,3,10,18);c.plus(19,17,3,True)
        if key=='report.chapter-add':c.line([(5,7),(9,7)],True,radius=0)
        elif key=='report.appendix-add':c.line([(5,11),(9,11)],True,radius=0);c.line([(5,15),(9,15)],radius=0)
        else:c.line([(5,7),(9,7),(9,11),(5,11)],True,closed=True,radius=.3)
    elif key in {'report.properties','report.cover','report.colophon','report.options','report.catalog','report.validate'}:
        sheet(c)
        if key=='report.properties':
            for y,x in ((8,11),(15,15)):c.line([(7,y),(17,y)],radius=0);c.circle(x,y,1.8,True)
        elif key=='report.cover':
            box(c,7,6,10,7,True);c.line([(7,17),(17,17)],radius=0)
        elif key=='report.colophon':
            c.circle(12,8,2,True);c.line([(7,16),(17,16)],radius=0);c.line([(9,19),(15,19)],radius=0)
        elif key=='report.validate':
            c.paths.clear()
            box(c,2,2,10,20)
            c.line([(5,7),(9,7)],radius=0)
            c.line([(5,14),(6.5,16),(9,12)],radius=.5)
            c.circle(19,15.5,3,True)
            c.line([(21.2,17.7),(23,20)],True,radius=0)
        elif key=='report.options':
            for y in (8,15):
                box(c,7,y-2,4,4,True);c.line([(14,y),(18,y)],radius=0)
        else:
            c.line([(1,5),(1,23),(17,23)],radius=.5)
            for y in (7,12,17):c.line([(7,y),(17,y)],True,radius=0)
    elif key in {'report.move-project','report.unlink-project'}:
        c.line([(3,21),(3,6),(8,6),(11,9),(21,9),(21,21)],closed=True,radius=.6)
        if key=='report.move-project':dimension_arrow(c,(7,15),(18,15),2.5)
        else:c.line([(9,13),(15,19)],True,radius=0);c.line([(9,19),(15,13)],True,radius=0)
    elif key.startswith('view.report-'):
        mode=key.split('-')[-1]
        box(c,2,3,20,18);c.line([(2,7),(22,7)],radius=0)
        if mode=='split':
            c.line([(12,7),(12,21)],radius=0)
            c.line([(5,11),(9,11)],True,radius=0);c.line([(5,15),(9,15)],radius=0)
            box(c,15,10,4,8,True)
        elif mode=='editor':
            for y in (11,15,19):c.line([(6,y),(18 if y!=19 else 13,y)],True,radius=0)
        elif mode=='json':
            c.line([(9,10),(7,10),(7,13),(5,14),(7,15),(7,18),(9,18)],True,radius=.5)
            c.line([(15,10),(17,10),(17,13),(19,14),(17,15),(17,18),(15,18)],True,radius=.5)
        else:box(c,8,9,8,10,True)
    elif key=='location.select':
        c.line(arc_points(11,8,5,150,390,32)+[(11,20)],closed=True,radius=.5)
        c.circle(11,8,1.5);c.line([(16,18),(18,20),(22,15)],True,radius=.4)
    elif key=='geo.cadastral':
        c.line([(2,6),(7,3),(12,6),(12,19),(7,16),(2,19)],closed=True,radius=.5)
        c.line([(7,3),(7,16)],radius=0)
        c.line([(17,12),(23,14),(21,22),(16,20)],True,closed=True,radius=.4)
    elif key=='file.download':
        c.line([(3,16),(3,21),(21,21),(21,16)],radius=.6)
        dimension_arrow(c,(12,3),(12,16),3.5)
    elif key=='document.close':
        sheet(c)
        c.line([(8,8),(16,16)],True,radius=0);c.line([(8,16),(16,8)],True,radius=0)
    elif key=='server.storage':
        for y in (3,13):
            box(c,3,y,18,8);c.circle(7,y+4,.8,True,True)
    elif key=='file.local':
        sheet(c)
        c.line([(7,17),(17,17)],True,radius=0)
    elif key=='feedback.github-issue':
        page(c,2,5,11,17)
        c.line([(6,10),(11,10)],radius=0);c.line([(6,15),(10,15)],radius=0)
        dimension_arrow(c,(17,8),(22,3),1.8)
    return True
