"""Energy selection categories and controls, read at the pinned source commit.

Vectors are original. Choice categories preserve their field/route context;
status symbols do not become commands merely because their source is an icon.
"""
import math
from b2_second_series import box, lightning, cubic
from b2_workspace_completion import shield
from b2_energy_pile_audio import arc_points
from b2_frame_completion import circular_arrow
from b2_session_two import dimension_arrow
from b2_document_navigation import paperclip

GROUPS={85:'Projectbibliotheek',86:'Formulieren en bewerken',87:'Documenttypen en uitvoer',78:'Gebruiksfuncties en gebouwtypen',79:'Warmteopwekkers',80:'Lucht, water en zon',
        81:'Schilmaatregelen',82:'Reken- en gegevenstoestanden',83:'Rekenhulpen en navigatie',84:'Constructieopbouw en bewijs'}
GROUPS=dict(sorted(GROUPS.items()))
ROWS=[
(78,'building.housing','Woonfunctie','Categorie voor een woonfunctie of bestaand woongebouw; geen startpagina.','557ba88b42e736a9'),
(78,'building.utility','Utiliteitsgebouw','De categorie bestaande utiliteit kiezen of een utiliteitsopname beginnen.','46ae971402f19db5'),
(78,'building.new-housing','Nieuwbouw wonen','De projectcategorie nieuwbouw wonen kiezen; maakt niet zelfstandig een project.','bd5a1c1642d94579'),
(78,'building.new-utility','Nieuwbouw utiliteit','De projectcategorie nieuwbouw utiliteit kiezen; geen bestaand appartement.','70ab953ccee9427c'),
(78,'building.apartment','Appartement','De woningsoort appartement kiezen; de vervolgvelden bepalen verdieping en ligging.','ff10272b80dfc3e7'),
(78,'building.caravan','Woonwagen','De woningsoort caravan/woonwagen kiezen.','98d6997f65f98757'),
(78,'building.houseboat','Woonboot','De woningsoort woonboot kiezen; de ligplaatsdatum blijft een afzonderlijke keuze.','b5b36109b5cade16'),
(78,'building.office','Kantoorfunctie','buildingFunction office kiezen op de functiekaart.','fe9f032f89ac7a28'),
(78,'building.education','Onderwijsfunctie','buildingFunction education kiezen op de functiekaart.','07f17436d55238b1'),
(78,'building.healthcare','Zorgfunctie','buildingFunction healthcare kiezen op de functiekaart.','37604939470ca31f'),
(78,'building.retail','Winkelfunctie','buildingFunction retail kiezen op de functiekaart.','76d25d08261153e8'),
(78,'building.industrial','Industriefunctie','buildingFunction industrial kiezen; geen warmte-krachtkoppeling.','b1e1f77ca3f8baa3'),
(78,'building.other','Overige gebruiksfunctie','buildingFunction other kiezen; geen actiemenu openen.','e9f6992a08f4ad52'),
(79,'energy.fired-generator','Warmte uit verbranding','Categorie bij boiler/lokaal gestookte verwarming en gasgestookte warmwateropwekkers; veld en label benoemen de subtypekeuze.','7359d81277f71d3c'),
(79,'energy.heat-pump','Warmtepomp','De generatorsoort heat_pump kiezen voor verwarming of warm water.','f3400c35e00c29ba'),
(79,'energy.heat-network','Warmtenet','De opwekker district_heat of gekoppelde afleverset kiezen; het bronveld benoemt de functie.','db61e5dc7b4af3a8'),
(79,'energy.electric-generator','Elektrische opwekker','Een elektrisch direct verwarmingstoestel of doorstroomtoestel kiezen; geen elektriciteitsmeting starten.','7c830641bcf7b648'),
(79,'energy.biomass','Biomassaopwekker','De generatorsoort biomass kiezen.','bdc651b93614ab19'),
(79,'energy.chp','Warmte-krachtkoppeling','De generatorsoort chp kiezen; geen industriele gebruiksfunctie.','089371c50770eea2'),
(79,'energy.warm-air','Gasgestookte luchtverwarmer','De generatorsoort gas_air_heater kiezen; geen ventilatieprincipe.','e8b763b9c58559a2'),
(79,'energy.no-system','Geen installatie aanwezig','none_present bij verwarming of none bij warm water kiezen; geen blokkade van de applicatie.','e6a0175e6659fb24'),
(79,'energy.electric-storage','Elektrische voorraadboiler','De warmwatergenerator electric_boiler kiezen.','64fdb259d15b50cf'),
(79,'energy.collective-hot-water','Collectief warm water','De warmwatergenerator collective_unknown kiezen; geen appartementstype.','3410f17fec445ec4'),
(80,'ventilation.natural','Natuurlijke ventilatie','ventilation.principle natural kiezen.','24591f03ce4322e3'),
(80,'ventilation.extract','Mechanische afvoer','ventilation.principle mechanical_extract kiezen.','b2487bfdd199dc73'),
(80,'ventilation.supply','Mechanische toevoer','ventilation.principle mechanical_supply kiezen.','b2487bfdd199dc73'),
(80,'ventilation.balanced','Gebalanceerde ventilatie','ventilation.principle balanced kiezen; toe- en afvoer.','b2487bfdd199dc73'),
(80,'energy.heating-measure','Verwarmingsmaatregel','In SurveyMwa een maatregel van kind heating toevoegen; geen specifiek keteltype kiezen.','c8078703097ee3a5'),
(80,'energy.hot-water-measure','Warmwatermaatregel','In SurveyMwa een maatregel van kind hotWater toevoegen.','8d5f3f68dc1f00c1'),
(80,'energy.ventilation-measure','Ventilatiemaatregel','In SurveyMwa een maatregel van kind ventilation toevoegen.','0f9c487a6b9985dd'),
(80,'energy.pv-measure','PV-maatregel','In SurveyMwa een maatregel van kind pv toevoegen; geen licht thema.','dce1b9f63a847b87'),
(81,'envelope.roof-measure','Dakmaatregel','Een verbetermaatregel voor het dak toevoegen; geen startpagina.','078822babeb8756d'),
(81,'envelope.facade-measure','Gevelmaatregel','Een verbetermaatregel voor de gevel toevoegen; geen tegelweergave.','8ee54616bd4e5c47'),
(81,'envelope.floor-measure','Vloermaatregel','Een verbetermaatregel voor de vloer toevoegen; geen annotatielaag.','340b258e362ba15e'),
(81,'envelope.window-measure','Raammaatregel','Een verbetermaatregel voor ramen toevoegen; geen paneel verbergen.','a946a52c2a68381f'),
(82,'calculation.audit','Rekenkerncontrole','Vaste kop van de NTA-rekenkernaudit; geen IFC-validatie starten.','1f0f0ba95c5bb04d'),
(82,'status.unavailable','Rekenkern niet beschikbaar','Toestand bij een mislukte kernelvraag met technische details; geen hulpknop.','3d0c52ee94e02d5d'),
(82,'status.unverified','Niet geverifieerd','De unv-toestand van een indicatief, ongeverifieerd resultaat aanduiden.','f1eb114086c91e50'),
(82,'status.pending','Wacht op gegevens','De waiting-toestand van de registratiechecklist aanduiden; geen lopende berekening suggereren.','fc2e28180e207287'),
(82,'status.incomplete','Nog aan te vullen','Een open vereiste of onvolledige invoer aanduiden; geen verwijderactie.','e4cf71aa70571421'),
(82,'status.stale-result','Resultaat hoort bij eerdere invoer','StaleBanner meldt dat het getoonde resultaat bij eerdere gegevens hoort.','22cd49cb2d602f70'),
(82,'status.unknown','Soort niet bekend','Fallbackaanduiding voor een nog niet gespecificeerde generatorsoort.','a3c630e058959f8c'),
(83,'tool.uvalue','Rc/U-rekenhulp','De werkruimte tool/uvalue openen; nog geen projectberekening starten.','4a788dbae13f93a9'),
(83,'tool.thermal-bridge','Koudebrugrekenhulp','De werkruimte tool/thermal-bridge openen.','4a788dbae13f93a9'),
(83,'tool.heat-pump-sizing','Warmtepompdimensionering','De werkruimte tool/heat-pump-sizing openen.','ee8d229e37f0fc7e'),
(83,'ui.tools','Gereedschapmenu','Het gereedschapmenu met rekenhulpen en uitwisseling openen.','e873549e652feb6f'),
(83,'nav.go-to','Ga naar benoemde bestemming','Een object, stap of resultaat rechtstreeks openen via het benoemde doel; geen geschiedenis Vooruit.','ad5f359728162a30'),
(83,'data.apply-next','Toepassen en volgende','De ingevoerde wijzigingen toepassen en daarna naar de volgende stap gaan.','b952fc3269c81efe'),
(83,'calculation.recalculate','Project herberekenen','De berekening voor het huidige project uitvoeren of verversen; de Energy-bron ververst de kernel en berekent de indicatieve BENG-uitkomst met invoercontroles.','3a00cfe83ca46f9d'),
(84,'construction.layer-add','Constructielaag toevoegen','addLayer voegt een nieuwe materiaallaag toe in de Rc/U-rekenhulp.','3009b3422fc32fac'),
(84,'construction.layer-up','Constructielaag omhoog','moveLayer index -1 verwisselt de materiaallaag met de vorige laag.','e86937c4d504faef'),
(84,'construction.layer-down','Constructielaag omlaag','moveLayer index +1 verwisselt de materiaallaag met de volgende laag.','951b5ffd02c2bcb9'),
(84,'evidence.file','Bewijsbestand','Aanduiding voor gekoppelde bewijsbestanden of ontbrekend afbeeldingsvoorbeeld; geen PDF-bijlage invoegen.','24b1cfc9ce99fb9f'),
(84,'evidence.photo','Fotobewijs','Kopaanduiding bij bewijsbestanden van het type foto; opent geen camera.','205228d0d3c29b8c'),

(85,'project.archive','Project archiveren','onArchiveEntry id true zet het bibliotheekproject in het archief.','fb1898bc5baeb97d'),
(85,'project.restore','Project terugzetten','Het archiefkenmerk opheffen of een project uit de prullenbak terugzetten; label benoemt de container.','7aa3054c460facb0'),
(85,'project.archive-view','Archief bekijken','setFolder ARCHIVE toont de gearchiveerde bibliotheekprojecten.','747f78709a68525e'),
(85,'project.trash-view','Prullenbak bekijken','setFolder TRASH toont de weggegooide bibliotheekprojecten.','e585f92f87dce3ca'),
(85,'project.move-folder','Project in map plaatsen','onMoveEntry wijzigt de maptoewijzing, of maakt en kiest de opgegeven map.','949384b1895b01a2'),
(85,'project.folder-new','Bibliotheekmap maken','newFolder vraagt een naam en maakt de bibliotheekmap.','bc3549893e838a7e'),
(85,'project.library','Projectbibliotheek','De volledige projectbibliotheek tonen of het mapfilter ALL kiezen.','7d120ff0627cea4f'),
(85,'view.cards','Kaartweergave','chooseView cards toont de bibliotheek als projectkaarten.','24c392036496d263'),
(85,'view.list','Lijstweergave','chooseView list toont de bibliotheek als projectenlijst.','7091b122f758ece4'),
(85,'ui.more','Meer acties','Het contextmenu van project of bibliotheekmap openen; geen projectactie direct uitvoeren.','f66f94951225aa87'),
(85,'project.forget-recent','Uit recente bestanden','onForgetRecent verwijdert alleen de verwijzing uit de recentelijst; geen bestand wissen.','60ecf3f197c3eace'),
(86,'object.edit','Gegevens bewerken','De editor of het gegevensformulier van het benoemde onderdeel openen.','12fccfa42f0c1d69'),
(86,'object.add','Onderdeel toevoegen','Het toevoegen van een benoemd projectonderdeel starten, via invoerformulier of een nieuw standaarditem.','aa85854b8c78dc4e'),
(86,'data.apply','Invoer toepassen','De bewerkte invoer vastleggen in het actieve project of de gekozen bibliotheek; het label benoemt welke gegevens worden toegepast.','a50fb8d5141360ae'),
(86,'data.discard','Invoer verwerpen','Niet-toegepaste invoerwijzigingen verwerpen en de bewerkingsronde of het formulier terugzetten naar de opgeslagen toestand.','7d2416e0953012ea'),
(86,'evidence.unlink','Bewijskoppeling losmaken','onUnlink verbreekt de koppeling van het bewijs aan dit gegeven; geen bestand verwijderen.','e170d89836a2bf40'),
(86,'calculation.settings','Rekenvoorkeuren','Het paneel met rekenvoorkeuren openen; Energy gebruikt hiervoor het tabblad calculation.','aeff5f860c136110'),
(86,'calculation.advice','Maatwerkadvies berekenen','calculate berekent de huidige maatregelvarianten en pakketten voor het maatwerkadvies.','cedd5304a944cc34'),
(87,'calculation.performance','Energieprestatie-uitkomst','Het energieprestatiepaneel of de bijbehorende werkruimte aanduiden/openen; geen berekenopdracht.','12680fb8c2d731df'),
(87,'advice.workspace','Maatwerkadvies','Kopaanduiding bij het maatwerkadvies met maatregelen en pakketten.','3375bfcb20cb095e'),
(87,'data.pending-changes','Gewijzigde invoervelden','Vaste aanduiding bij de lijst nog toe te passen invoervelden; geen rapportopdracht.','a7332afe9f52683e'),
(87,'report.document','Rapportdocument','Documenttypeaanduiding bij het resultaatrapport in de uitvoerkeuzes.','880925311645947a'),
(87,'report.calculation-document','Berekeningsdocument','Documenttypeaanduiding bij het NTA-berekeningsrapport.','fc00eceb9f73957a'),
(87,'report.input-dossier','Invoerdossier','Documenttypeaanduiding bij het dossier met projectinvoer.','aa47c8c1c62b8c3c'),
(87,'report.project-dossier','Projectdossier','Documenttypeaanduiding bij het samengestelde projectdossier.','bc8da5e2f1781208'),
(87,'file.export-options','Uitvoerkeuzes openen','Het uitvoerkeuzemenu of -paneel openen voor document, project of annotatieselectie. De concrete uitvoerkeuze schrijft pas daarna een bestand.','d1d9de922703d58e'),
(87,'project.compare-reference','Referentieproject vergelijken','Het originele projectbestand kiezen, met het huidige project via assessRelabelWithRust vergelijken en de vergelijking bewaren.','83176ae90969514c'),
(87,'printer.properties','Printereigenschappen','handlePrinterProperties opent de eigenschappen van de geselecteerde printer.','12e8cecfc5b161f2'),
]
KEYS={k for _,k,_,_,_ in ROWS}
SEMANTIC={'status.unavailable':'error','status.unverified':'warning','status.pending':'text-secondary',
          'status.incomplete':'warning','status.stale-result':'warning','status.unknown':'text-secondary'}
ACCENT_FRONT={k:'De bepalende accentmarkering blijft zichtbaar voor de omringende contour.' for k in KEYS if k.startswith(('energy.','ventilation.','envelope.','construction.','data.','nav.'))}
ACCENT_FRONT.update({k:'De bepalende markering ligt voor de contour.' for k in ('building.housing','calculation.audit','ui.tools','project.compare-reference')})
ACCENT_FRONT['object.edit']='De potloodcontour blijft ononderbroken voor de documentrand.'
REUSED={};EXCLUDED={};DISPATCHERS={};DISPATCH_EVIDENCE={}


def reuse(ids,key,reason):
    for rid in ids.split():REUSED[rid]=(key,reason)


def dispatch(ids,targets,reason):
    for rid in ids.split():DISPATCHERS[rid]=targets;DISPATCH_EVIDENCE[rid]=reason


reuse('fd22d7836d1f747a 2bb0fbbe5c54e60b 12fbfe4f9eb64cd3 d15ffed9e1eddbcb 22b922c95b15cdf7 b5454528358d42c0 ff39c0d0faa838ba','status.warning','Respectievelijk oude normeditie, waarschuwingen, ontbrekende registratiegereedheid of expliciete warning-severity; bronconditie gelezen.')
reuse('b8af12a46719f0d9 b1cfe158ef6679f8 de5ead209503f9d7','status.incomplete','Onvolledige kernelinvoer of nog ontbrekend bewijs in een open checklist; geen verwijdering en geen algemene berekenfout.')
reuse('1a36bf8c51838e3a dc79d87bd77bd3ca 4f1b835ca41e7c80 5fae2925dd315d35 9299a955d7ea34ed 46533946b238ebd8 55dcd7241085f63f ab5a3f85c0f81c63','status.error','Invalid/error/failsLimit of err-severity duidt een fout of afgekeurde uitkomst aan; geen sluitactie.')
reuse('42ebd5adc97f6ad4','status.unavailable','Dezelfde kernel-unavailable-toestand in het prestatiepaneel.')
reuse('8b3f0af4226975ca','status.pending','Dezelfde waiting-checklisttoestand bij herlabelen.')
reuse('99d1bec1aa8dde4d','status.unknown','Fallback bij een warmwatergeneratorkeuze zonder specifiek soorticoon.')
reuse('42d6aa9a52e36fb8 cc7c222a91672fe4 181b8e3d4e451b80 f848fd9c6bf3696d 49c3fbe5accaab92 ff849a411a56d082 b5487c25ee8705d5 58874ede188092fa 68a618ed2f81603e df8d8892e499f40b 2a8aa1221cade423 190f88f6c87550c4 5e76e5cb4194ad37 7d0ced403b3d2d54','status.success','Gekopieerd, stap voltooid, controle zonder fouten, bewijs compleet of registratie gereed: een toestand, geen zelfstandige opdracht.')
reuse('642ee2c51a6a72aa d03f97175cbb24c3 4f5d044581b442a5 9f53c1db3a1903cf 18bf33d69963634a','status.info','Informatieve toelichting of expliciete info-severity bij tabel, resultaat of toast.')
reuse('c6195b698eb3dfdf','ui.about','Instellingentab about, geen informatieve procesmelding.')
reuse('e7c8e5a51f7ba89d','nav.back','De vorige formulierstap via go(here-1), geen undo.')
reuse('e8d03b69ef180c8a 4280370a2c03a2cf 094a116a432912fa c509803cf4856270 2916bb67d3944c67 730c4023dee18e42','nav.go-to','De benoemde gegevenslocatie, installatiestap, fout, resultaat of workflowstap via navigate/goTo openen.')
reuse('18671083c9ed700d 6db1d4c87659be37','ui.help','Het routegebonden handleidinghoofdstuk of het algemene handboek openen.')
reuse('1434df7fd440e446 5123c3cb8a329580','bim.workspace','navigate building/model3d toont de 3D-modelwerkruimte.')
reuse('58d913051c54e501 abc9ff231da9c37b 458572d66eb8119d 919f339b3fc44bc3 721e378b8b712033','ifc.export','exportModelIFC schrijft modelgeometrie; exportIFC schrijft BENG/IFC-gegevens na beoordeling van de kernuitkomst. Scope staat in het label.')
reuse('e82b25964f914f17','building.apartment','KindIcon toont een bibliotheekitem met dwelling apartment; geen nieuwbouw-utiliteitskeuze.')
reuse('0e31872880322b29 cf57ccfa78644e55','building.utility','Utiliteitsopname starten of de categorie bestaand utiliteitsproject kiezen/aanduiden.')
reuse('2912083354b635b6 6919371794c4e52c e9f89a45e0a43ff0 04b8e2a52996b7c1 7187d258e3af2d6e 594f660182bf0c0d','building.housing','Woningsoort grondgebonden of projectcategorie bestaand wonen kiezen/aanduiden; label bepaalt de gegevensscope.')
reuse('b2be7cc75242f426 088d6957152bc3ce','building.new-housing','Categorie nieuwbouw wonen in bibliotheek of nieuw-projectkeuze.')
reuse('dbcaaeba91e8c9c6 891a44ca82761be5','building.caravan','Dezelfde woonwagenkeuze of bibliotheekaanduiding.')
reuse('47e214b9e8da9faf 9c6f9266b69b65ad','building.houseboat','Dezelfde woonbootkeuze of bibliotheekaanduiding; datum blijft in vervolgvelden.')
reuse('865cb0f9161ab796','energy.heat-pump','Warmwateropwekker heat_pump gebruikt dezelfde fysieke toestelcategorie.')
reuse('4f4bb09620b021ca','energy.heat-network','De warmwaterkeuzes district_heat en delivery_set_from_heating gebruiken de warmtenet-/afleversetcategorie.')
reuse('41e0a5ebe77ef95a','energy.electric-generator','De direct elektrische warmwatergenerator, onderscheiden van de voorraadboiler.')
reuse('700ceda93f17e830','energy.no-system','Bij warm water kiest none expliciet afwezigheid van een installatie.')
reuse('9bf21e4958aee099 f6103f119190d95c','energy.fired-generator','Lokaal gestookte verwarming of gasgestookte warmwatergenerator; veld en subtype staan in het label.')
reuse('37d1b2cefa930e84','edit.copy','copyResult schrijft de Rc/U-resultaattekst naar navigator.clipboard; de tijdelijke Check is de gekopieerd-toestand.')
reuse('1d6fc1ce6b1ce7c5','edit.duplicate','onDuplicateEntry maakt direct een nieuw bibliotheekexemplaar; geen klembord.')
reuse('2441ef471ee21567','window.restore','De Copy-vorm verschijnt alleen in de gemaximaliseerde titelbalk; klik toggleMaximize herstelt het venster.')
reuse('7d0cc157266ba4b1 30c6406bfec4477a 8df935c30beff88a','file.new','onNewProject/newProject opent de nieuwe-projectstroom; het is geen nieuw onderdeel binnen het model.')
reuse('b8b4ab2965641edb','file.open','Het DocumentTabs-menu kiest een bestaand projectbestand.')
reuse('0607448890a43aff 138e8b7ac914e20b','file.save','onSaveProject bewaart het actieve projectdocument.')
reuse('36f6e93a5b4484ff db4778f24cfd9ac0 1f22db09b5648752','ui.settings','Algemene appvoorkeuren openen of het tabblad general aanduiden.')
reuse('72f0b793bb0e47f1','ui.tools','Chevron is onderdeel van dezelfde Gereedschap-menuknop.')
reuse('883b34719cc32c7b','ui.file-menu','De chevron opent het Bestandmenu; geen algemene keuzelijst met veldwaarden.')
reuse('30e196bc32898f9c 7ba47aad8fc33b84','ui.feedback','openFeedback toont het feedbackvenster, geen documentnotitie.')
reuse('4d18a4747df10a6e e6eb3c53d1df2314','panel.right','De buitenste Preview/Properties-zijbalk invouwen; de embedded variant toont deze knop niet.')
reuse('5a50b45144946df1 af56a9796fe47425 8eb6da1c6b760aa0','evidence.file','Aanduiding van gekoppeld bewijs of een bewijsreferentie in een gegevensveld; geen PDF-bijlage toevoegen.')
reuse('58c3dbf958e35612 b9454576d674cc1c 9f20f7c24ed4e769 3f401abfff8a58a9','view.search','Adres zoeken, opdrachten/velden zoeken of de gebouwonderdelenlijst doorzoeken; geen zoom- of filter-only-opdracht.')
reuse('c0ed31fdb4467d67','edit.undo','shared.undo neemt de laatste toegepaste invoerwijziging terug, geen standaardwaarden ophalen.')
reuse('2da0231baf370b90 97826fd79d62e687 d6b0ced42e7d6e07 6d3965f67bcd9d41','file.print','Het afdrukvoorbeeld openen of handlePrint uitvoeren; label en dialoog onderscheiden voorbereiden en afdrukken.')
reuse('b028de755e5b05d7','view.zoom-out','handleZoomOut verkleint alleen het afdrukvoorbeeld.')
reuse('86c396d64cd4d516','view.zoom-in','handleZoomIn vergroot alleen het afdrukvoorbeeld.')
reuse('73f1f6adfb6e68fd d10ab2c5d37a08f9 d57061815624686d f74ec5d2568dea91 74e85a35a89bc743 285d2d2b5ab3dbb8 0dfccccd4f3b3374 259a6fc5fdd0da32','file.import','De concrete UNIEC3- of VABI-projectbestandkeuze starten; bestandsformaat staat in het label.')
reuse('7a4a1defd5c689b3 0f5b491e4ae1de99 3f4ea09a0dbfd0b4 cb3a789e9a59404a','edit.delete','De geselecteerde warmtepomp, het bewerkte object, de materiaallaag of de adviesmaatregel verwijderen; scope in label/bevestiging.')
reuse('4f1b835ca41e7c80','status.error','failsLimit in de statusbalk is een niet-gehaalde grenswaarde, geen sluiten.')
reuse('2dac37608e640883 f3aae1180d3024c4','ui.close','Het inspectiepaneel of de toastmelding sluiten.')
reuse('efad7dbd5affbcda','window.close','De native titelbalk sluit het applicatievenster; browservariant verbergt native vensterknoppen.')
reuse('74f9700a5289de63','document.close','onCloseActiveTab sluit het huidige projecttabblad; de applicatie blijft bestaan.')

dispatch('b2487bfdd199dc73',('ventilation.extract','ventilation.supply','ventilation.balanced'),'De drie mechanische VENTILATION_ICONS-varianten delen Fan, maar schrijven verschillende principle-waarden; natural heeft zijn eigen Wind-bronplaats.')
reuse('d1c30235599cf3e4','status.unknown','De fallback in ChoiceCards wordt alleen gebruikt als een ventilatieprincipe geen specifieke icoonvariant heeft; de vier bekende principes zijn afzonderlijk toegewezen.')
dispatch('4a788dbae13f93a9',('tool.uvalue','tool.thermal-bridge'),'TOOL_STEP bevat twee Calculator-routes: uvalue en thermal-bridge. heat-pump-sizing heeft de afzonderlijke Flame-variant.')
EXCLUDED['f0a0b79ddd9c536b']='Statisch GripVertical tussen de omhoog/omlaagknoppen; geen draggable, pointer- of sleephandler aan de grip in de UValue-tabel.'
EXCLUDED['3622c84b7c31c29a']='Dynamische kompasnaald in gebouwdata, geroteerd naar de Orientation-waarde; geen vaste bedieningsfunctie of objectrotatie.'
EXCLUDED['cd56e925cd879e5e']='Applicatiefavicon, geen vast bedieningsicoon.'
EXCLUDED['db80f1c649513fe2']='Native applicatiebeeldmerk, geen vast bedieningsicoon.'


reuse('9e2bfee2068a33b5 5411291f0babdbe6 e1f188996483aa79 e073dedb141d5ea9 9340be98103fac8d 8587079c01ce7c1c a889059bbc21d103 a910b1870e55f8a9 19fb8a9db74bcbf2 4d00a2a1e1646fcd 93527a4ecb77ab94 64070b22cbeb5293 0f56ae37707100de','file.export','De concrete callback schrijft het benoemde rapport, invoerdossier, projectdossier, UNIEC3 of VABI. Het label bepaalt gegevensscope en formaat; geen algemene download van een al bestaand bestand.')
reuse('17a0d20af0bdda89','building.apartment','De appartementcategorie in DWELLING_GROUPS van Nieuw project.')
reuse('a0c6a969a83e7f8b','building.new-utility','De expliciete utility-nieuwbouwkeuze in het fallbackmenu van de bibliotheek.')
dispatch('b3aa18bdcbdbbafb',('building.utility','building.new-utility'),'KindIcon gebruikt Building2 voor zowel bestaande als nieuwe utiliteitsprojecten; entry.kind en het label bepalen de categorie.')
reuse('afec93fd5289e7a8','project.folder','Het gekozen bibliotheekmapfilter tonen, geen projectbestand direct openen.')
reuse('b5626d9a26eb54b6','file.open','Deze FolderOpen staat daadwerkelijk bij onOpenProject op regel 284, naast het aparte importmenu; broncontext gecorrigeerd.')
reuse('0e0df51bc83c1f0c','project.library','ALL in de mapkolom heft het mapfilter op; geen kaartweergaveknop.')
reuse('82b4747e44cabaf6 e0a0d42ffb81682d 79a00b14595687b0','ui.more','Het contextmenu van een projectrij of bibliotheekmap openen.')
reuse('5d6c446d9da489fb a93b6f8cfa74cf02 a0b1a2c758baf922 5f02654954f48416','object.edit','Registratiebewijs, projectgegevens of de adviesmaatregel bewerken; het label noemt het concrete gegevensformulier.')
reuse('cade7f1ebf466089 410ac41682924861 9bdd4756c63c5045 790534999c5071c3','object.add','Het benoemde nieuwe onderdeel toevoegen of het bijbehorende invoerformulier openen: warmtepomp, maatregel, raamtype of installatie.')
reuse('534e47a32210105c acf34328c1f1e262 0848e03116041310 67bf105c5aabf701','file.new','Een nieuw project van de gekozen categorie starten; geen onderdeel binnen het actieve model.')
reuse('4bb73fe467829fcd','advice.workspace','Dezelfde vaste kopaanduiding van het maatwerkadviespaneel.')
reuse('9f346af348ab5a24 b7532ad9dbb1ffe0 a07a29e46fc1c7e1','edit.delete','Een project naar de prullenbak verplaatsen of definitief verwijderen volgens de benoemde menuactie; bevestiging en herstelbaarheid blijven expliciet in de app.')
reuse('a83c6a10221ac8b2','edit.clear-all','clearTrash vraagt bevestiging en leegt de projectprullenbak; de scope is alle weggegooide bibliotheekprojecten.')
dispatch('fb1898bc5baeb97d',('project.archive','project.restore'),'De Archive-menuactie wisselt op entry.archived tussen onArchiveEntry true en false. Het label en de toestand bepalen de richting.')
EXCLUDED['61a5cd76a4cd7a7f']='Grote EmptyState-illustratie bij een nog niet gestart maatwerkadvies; de afzonderlijke startknop heeft geen icoon en de kleine paneelkop is apart beoordeeld.'
EXCLUDED['c913e2dda861a13e']='Vaste decoratieve FolderPlus in de bibliotheektoelichting, geen recente-verwijzing verwijderen en geen mappenknop.'


def cubic_points(points,n=24):
    a,b,c,d=points
    return [tuple((1-t)**3*a[j]+3*(1-t)**2*t*b[j]+3*(1-t)*t*t*c[j]+t**3*d[j] for j in (0,1)) for t in (i/n for i in range(n+1))]


def flame(c,x=12,y=12,w=8,h=14):
    segments=[[(12,3),(13,7),(18,10),(17,15)],[(17,15),(16,21),(7,21),(7,15)],[(7,15),(7,12),(9,10),(10,8)],[(10,8),(9,12),(13,12),(12,3)]]
    scale=c.size/24
    ring=[(scale*(x+(px-12)*w/10),scale*(y+(py-12)*h/18)) for seg in segments for px,py in cubic_points(seg)[:-1]]
    c.fills.append({'tone':'accent','rings':[ring]})


def droplet(c,x,y,w,h):
    segments=[[(0,-.5),(-.12,-.25),(-.5,.03),(-.5,.18)],[(-.5,.18),(-.5,.65),(.5,.65),(.5,.18)],[(.5,.18),(.5,.03),(.12,-.25),(0,-.5)]]
    c.line([(x+px*w,y+py*h) for seg in segments for px,py in cubic_points(seg)[:-1]],True,closed=True,radius=0)


def hall(c):
    c.line([(3,21),(3,9),(10,4),(10,9),(17,4),(17,10),(21,10),(21,21)],closed=True,radius=.35)
    scale=c.size/24
    c.fills.append({'tone':'accent','rings':[[(x*scale,y*scale) for x,y in ((9,12),(15,12),(15,17),(9,17))]]})


def tower(c,balconies=False):
    box(c,8,2,12,20)
    c.line([(2,22),(2,12),(8,12),(8,22)],closed=True,radius=.5)
    if balconies:
        for y in (7,11,15):c.line([(11,y),(17,y)],True,radius=0)
    else:
        scale=c.size/24
        for x in (11.5,16.5):
            for y in (6,11,16):c.fills.append({'tone':'accent','rings':[[(px*scale,py*scale) for px,py in ((x-1,y-1),(x+1,y-1),(x+1,y+1),(x-1,y+1))]]})


def vent_fan(c):
    c.circle(8,12,5)
    for a in (0,120,240):
        t=math.radians(a);c.line([(8,12),(8+4*math.cos(t),12+4*math.sin(t))],radius=0)


def house(c):
    c.line([(3,10),(12,3),(21,10),(21,21),(3,21)],closed=True,radius=.4)
    c.line([(9,17),(9,13),(15,13),(15,17)],radius=.3)


def block(c,tall=False):
    box(c,5 if tall else 3,2 if tall else 5,14 if tall else 18,20 if tall else 16)
    for x in ((9,15) if tall else (7,12,17)):
        for y in (9,15):c.circle(x,y,.7,True,True)


def bolt(c,accent=True):
    lightning(c,accent=accent)


def question(c,accent=True):
    pts=arc_points(12,8,3,180,400,28)+[(12,13),(12,14)]
    c.line(pts,accent,radius=.5);c.circle(12,18,.8,accent,True)


def calculator(c,x,y,w,h,accent=False):
    box(c,x,y,w,h,accent)
    c.line([(x+w*.28,y+h*.27),(x+w*.72,y+h*.27)],accent,radius=0)
    for px in (.3,.7):
        for py in (.58,.8):c.circle(x+w*px,y+h*py,.5,accent,True)


def tank(c):box(c,6,2,12,20)


def flow(c,start,end,y):dimension_arrow(c,(start,y),(end,y),2)


def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key.startswith('building.'):
        kind=key.split('.')[1]
        if kind in {'housing','new-housing'}:house(c)
        elif kind in {'utility','new-utility'}:hall(c)
        elif kind in {'office','apartment'}:tower(c,kind=='apartment')
        elif kind=='caravan':
            c.line([(2,16),(2,6),(18,6),(18,16),(22,16)],radius=.5)
            box(c,5,9,5,4,True);c.circle(7,18,2);c.circle(17,18,2)
        elif kind=='houseboat':
            c.line([(2,15),(5,15),(5,5),(17,5),(20,8),(20,15),(22,15),(19,21),(5,21)],closed=True,radius=.5)
            c.line([(5,15),(20,15)],radius=0)
            scale=c.size/24
            for x in (8,14):c.fills.append({'tone':'accent','rings':[[(px*scale,py*scale) for px,py in ((x,8),(x+3,8),(x+3,12),(x,12))]]})
        elif kind=='education':
            c.line([(2,8),(12,3),(22,8),(12,13)],closed=True,radius=.3)
            c.line([(6,10),(6,17),(12,20),(18,17),(18,10)],radius=.3)
            c.line([(22,8),(22,18)],True,radius=0)
        elif kind=='healthcare':
            box(c,3,5,18,16);c.plus(12,11,3,True);c.line([(9,21),(9,18),(15,18),(15,21)],radius=.3)
        elif kind=='retail':
            c.line([(3,10),(3,21),(21,21),(21,10)],radius=.4)
            c.line([(2,10),(5,3),(19,3),(22,10)],closed=True,radius=.3)
            for x in (8,16):c.line([(x,3),(x,10)],True,radius=0)
        elif kind=='industrial':
            c.line([(3,21),(3,10),(9,6),(9,10),(15,6),(15,12),(21,12),(21,21)],closed=True,radius=.3)
            for x in (7,12,17):c.line([(x,16),(x,18)],True,radius=0)
        elif kind=='other':
            box(c,3,5,18,16)
            for x in (7,12,17):c.circle(x,13,.9,True,True)
        if kind in {'housing','new-housing'}:c.paths[-1]['tone']='accent'
        if kind.startswith('new-'):
            for p in c.paths:p['points']=[(.7*x,.7*y) for x,y in p['points']]
            for p in c.circles:p.update(x=p['x']*.7,y=p['y']*.7,r=p['r']*.7)
            for fill in c.fills:fill['rings']=[[(.7*x,.7*y) for x,y in ring] for ring in fill['rings']]
            c.plus(19,19,3,True)
    elif key.startswith('energy.'):
        kind=key.split('.')[1]
        if kind=='fired-generator':
            tank(c)
            flame(c)
        elif kind=='heat-pump':
            box(c,3,4,12,17)
            for y in (8,12,16):c.line([(6,y),(12,y)],radius=0)
            dimension_arrow(c,(21,20),(21,5),1.8)
        elif kind=='heat-network':
            c.line([(3,6),(3,12),(21,12),(21,18)],radius=.4)
            c.line([(12,3),(12,21)],True,radius=0)
            for x,y in ((3,4),(21,20)):c.circle(x,y,2)
        elif kind in {'electric-generator','electric-storage'}:
            if kind=='electric-storage':tank(c)
            else:box(c,3,4,18,17)
            bolt(c)
        elif kind=='biomass':
            c.line([(12,2),(4,13),(8,13),(3,19),(21,19),(16,13),(20,13)],closed=True,radius=.3)
            c.line([(12,14),(12,23)],True,radius=0)
        elif kind=='chp':
            c.line([(3,21),(3,9),(10,4),(10,9),(17,4),(17,21)],closed=True,radius=.3)
            lightning(c,11,14.5,6,9)
        elif kind=='warm-air':
            box(c,2,2,13,20);flame(c,8.5,12,6,13)
            for y in (7,12,17):c.line([(19,y),(23,y)],radius=0)
        elif kind=='no-system':
            c.line([(5,5),(19,19)],radius=0);c.line([(5,19),(19,5)],radius=0)
        elif kind=='collective-hot-water':
            c.line([(2,21),(2,6),(7,6),(7,3),(12,3),(12,21)],closed=True,radius=.4)
            for y in (9,13,17):c.line([(5,y),(9,y)],radius=0)
            droplet(c,19,14.5,7,12)
        elif kind=='heating-measure':
            box(c,3,9,18,11)
            for x in (8,13,18):c.line([(x,9),(x,20)],radius=0)
            for x in (6,18):c.line([(x,20),(x,23)],radius=0)
            for x in (7,12,17):
                c.line(cubic_points([(x,6),(x-2,4.5),(x+2,3.5),(x,2)]),True,radius=0)
        elif kind=='hot-water-measure':
            c.line([(4,21),(4,11),(7,8),(15,8),(19,11)],radius=2)
            c.line([(8,8),(8,3)],radius=0)
            c.line([(4.5,3),(11.5,3)],radius=0)
            c.line([(1.5,21),(7,21)],radius=0)
            droplet(c,19,18.5,6,7)
        elif kind=='ventilation-measure':
            box(c,3,3,18,18);c.circle(12,12,6)
            for a in (0,120,240):
                t=math.radians(a);c.line([(12,12),(12+5*math.cos(t),12+5*math.sin(t))],True,radius=0)
        elif kind=='pv-measure':
            c.line([(3,12),(17,12),(21,21),(1,21)],closed=True,radius=.4)
            c.line([(8,12),(7,21)],radius=0);c.line([(12,12),(14,21)],radius=0)
            c.line([(2,16.5),(19,16.5)],radius=0)
            c.circle(18,5,1.8,True,True)
            for a in (0,90,180,270):
                t=math.radians(a)
                c.line([(18+3.2*math.cos(t),5+3.2*math.sin(t)),(18+3.6*math.cos(t),5+3.6*math.sin(t))],True,radius=0)
    elif key.startswith('ventilation.'):
        kind=key.split('.')[1]
        if kind=='natural':
            box(c,3,5,10,14)
            for x in (6.5,9.5):c.line([(x,8),(x,16)],radius=0)
        else:vent_fan(c)
        if kind in {'natural','extract'}:dimension_arrow(c,(17,12),(23,12),1.4)
        elif kind=='supply':dimension_arrow(c,(23,12),(17,12),1.4)
        else:
            dimension_arrow(c,(17,8),(23,8),1.4)
            dimension_arrow(c,(23,16),(17,16),1.4)
    elif key.startswith('envelope.'):
        kind=key.split('.')[1]
        if kind=='roof-measure':house(c);c.line([(3,10),(12,3),(21,10)],True,radius=.4)
        elif kind=='facade-measure':
            box(c,3,3,18,18)
            for y in (9,15):c.line([(3,y),(21,y)],True,radius=0)
            for x,y in ((9,3),(15,9),(9,15)):c.line([(x,y),(x,y+6)],radius=0)
        elif kind=='floor-measure':
            c.line([(3,8),(16,3),(22,8),(9,13)],True,closed=True,radius=.3)
            c.line([(3,14),(9,19),(22,14)],radius=.3)
            c.line([(3,18),(9,23),(22,18)],radius=.3)
        else:
            box(c,3,2,18,19)
            c.line([(12,2),(12,21)],radius=0)
            c.line([(3,22.5),(21,22.5)],radius=0)
            c.line([(6,10),(9,6)],True,radius=0)
            c.line([(15,16),(18,12)],True,radius=0)

    elif key.startswith('project.'):
        kind=key.split('.')[1]
        if kind in {'archive','restore','archive-view'}:
            box(c,3,7,18,14);box(c,2,3,20,4)
            if kind=='archive-view':c.line([(9,11),(15,11)],True,radius=0)
            elif kind=='archive':dimension_arrow(c,(12,9),(12,18),2.5)
            else:dimension_arrow(c,(12,18),(12,9),2.5)
        elif kind=='trash-view':
            c.line([(5,6),(6,21),(18,21),(19,6)],closed=True,radius=.4)
            c.line([(3,6),(21,6)],radius=0);c.line([(9,6),(9,3),(15,3),(15,6)],True,radius=.4)
        elif kind in {'move-folder','folder-new'}:
            c.line([(3,21),(3,5),(9,5),(12,9),(21,9),(21,21)],closed=True,radius=.5)
            if kind=='folder-new':c.plus(13,15,3,True)
            else:dimension_arrow(c,(7,15),(18,15),2.5)
        elif kind=='library':
            for x,y in ((3,3),(14,3),(3,14),(14,14)):box(c,x,y,7,7,x==14 and y==3)
        elif kind=='compare-reference':
            box(c,2,2,7,10);box(c,15,2,7,10)
            dimension_arrow(c,(5,17),(19,17),1.6)
            dimension_arrow(c,(19,21),(5,21),1.6)
        elif kind=='forget-recent':
            c.circle(9,10,6);c.line([(9,6),(9,10),(12,12)],radius=.3)
            c.line([(14,20),(22,20)],True,radius=0);c.line([(3,20),(9,20)],radius=0)
    elif key in {'view.cards','view.list'}:
        if key=='view.cards':
            for x in (2,14):
                box(c,x,3,8,18)
                c.line([(x+2.5,15),(x+5.5,15)],radius=0)
                c.line([(x+2.5,18),(x+5.5,18)],radius=0)
                scale=c.size/24
                c.fills.append({'tone':'accent','rings':[[(px*scale,py*scale) for px,py in ((x+2.5,6),(x+5.5,6),(x+5.5,11),(x+2.5,11))]]})
        else:
            for y in (5,12,19):
                c.circle(4,y,1,True,True);c.line([(9,y),(21,y)],radius=0)
    elif key=='ui.more':
        c.line([(3,5),(21,5),(21,19),(3,19)],closed=True,radius=.6)
        for x in (7,12,17):c.circle(x,12,.8,True,True)
    elif key in {'object.edit','object.add'}:
        box(c,2,3,10,18)
        if key=='object.add':c.plus(19,15,3,True)
        else:
            c.line([(16,20),(16.5,16),(20.5,10),(23,12),(19,18)],True,closed=True,radius=.5)
    elif key in {'data.apply','data.discard'}:
        box(c,2,3,10,18)
        for y in (7,11):c.line([(5,y),(9,y)],radius=0)
        if key=='data.apply':c.line([(16,16),(18.5,19),(23,12)],True,radius=.5)
        else:circular_arrow(c,19.5,16.5,3,0,270,1.3)
    elif key=='evidence.unlink':
        paperclip(c)
        c.line([(17,15),(23,21)],True,radius=0);c.line([(17,21),(23,15)],True,radius=0)
    elif key=='calculation.settings':
        calculator(c,2,3,11,18)
        for y in (7,16):c.line([(17,y),(23,y)],True,radius=0)
        c.line([(19,5.5),(19,8.5)],True,radius=0);c.line([(21,14.5),(21,17.5)],True,radius=0)
    elif key=='calculation.advice':
        c.line([(2,19),(2,9),(6.5,5),(11,9),(11,19)],closed=True,radius=.7)
        c.line([(5,18),(5,14),(8,14),(8,18)],radius=.4)
        calculator(c,16,7,7,14,True)
    elif key in {'calculation.performance','advice.workspace'}:
        box(c,4,3,16,18)
        if key=='calculation.performance':
            c.line([(7,17),(7,12)],True,radius=0);c.line([(12,17),(12,8)],True,radius=0);c.line([(17,17),(17,11)],True,radius=0)
        else:
            box(c,8,1.5,8,4)
            c.line([(7,12),(10,15),(17,8)],True,radius=.3)
    elif key=='data.pending-changes':
        box(c,2,2,10,20)
        for y in (7,12,17):c.line([(5,y),(9,y)],radius=0)
        c.circle(19,17,2.5,True,True)
    elif key.startswith('report.'):
        kind=key.split('.')[1]
        if kind=='project-dossier':
            box(c,3,7,18,14)
            c.line([(8,7),(8,3),(16,3),(16,7)],radius=1)
            c.line([(3,12),(21,12)],radius=0)
            c.line([(10,16),(14,16)],True,radius=0)
        else:
            c.line([(4,22),(4,2),(14,2),(20,8),(20,22)],closed=True,radius=.4)
            c.line([(14,2),(14,8),(20,8)],radius=.3)
            if kind=='document':
                for y in (12,16,19):c.line([(8,y),(16,y)],True,radius=0)
            elif kind=='calculation-document':
                c.line([(8,13),(16,13)],True,radius=0)
                for x in (9,15):c.circle(x,17.5,.65,True,True)
            else:
                box(c,7,11,10,8,True);c.line([(7,15),(17,15)],True,radius=0)
    elif key=='file.export-options':
        box(c,2,3,10,18)
        for y in (7,12,17):c.line([(5,y),(9,y)],radius=0)
        dimension_arrow(c,(16,9),(23,9),2)
        for x in (17,20,23):c.circle(x,18,.7,True,True)
    elif key=='printer.properties':
        c.line([(7,15),(3,15),(3,7),(21,7),(21,15),(17,15)],radius=1)
        box(c,7,2,10,5);box(c,7,11,10,6)
        for x in (3,15):c.line([(x,22),(x+6,22)],True,radius=0)
        c.line([(5,20.5),(5,23)],True,radius=0)
        c.line([(19,20.5),(19,23)],True,radius=0)
    elif key.startswith('status.'):
        kind=key.split('.')[1]
        if kind=='pending':c.circle(12,12,9);c.line([(12,6),(12,12),(17,15)],True,radius=.3)
        elif kind=='incomplete':
            c.line(arc_points(12,12,9,0,260),radius=0)
            for a in (290,320,350):c.circle(12+9*math.cos(math.radians(a)),12+9*math.sin(math.radians(a)),.7,True,True)
        elif kind in {'unknown','unverified'}:
            if kind=='unknown':c.circle(12,12,10)
            else:shield(c)
            question(c)
        elif kind=='unavailable':
            box(c,5,5,14,14)
            for x in (8,16):c.line([(x,2),(x,5)],radius=0);c.line([(x,19),(x,22)],radius=0)
            c.line([(8,8),(16,16)],True,radius=0);c.line([(8,16),(16,8)],True,radius=0)
        else:
            box(c,2,2,10,18);c.line([(5,6),(9,6)],radius=0)
            c.circle(19,17,3.5,True);c.line([(19,15),(19,17),(21,18)],True,radius=.5)
    elif key=='calculation.audit':
        box(c,2,2,10,19)
        for y in (6,10):c.line([(5,y),(9,y)],radius=0)
        c.circle(19,15.5,3,True);c.line([(21.2,17.7),(23,20)],True,radius=0)
    elif key=='calculation.recalculate':
        calculator(c,8.5,7.5,7,10)
        circular_arrow(c,12,12,10.5,215,505,1.7)
    elif key.startswith('tool.'):
        name=key.split('.')[1]
        if name=='uvalue':
            box(c,3,3,19,18)
            for x in (8,13):c.line([(x,3),(x,21)],radius=0)
            for y in (7,12,17):c.line([(17,y),(19,y)],True,radius=0)
        elif name=='thermal-bridge':
            c.line([(3,3),(9,3),(9,15),(21,15),(21,21),(3,21)],closed=True,radius=1.2)
            c.line([(13,4),(13,11),(20,11)],True,radius=2)
        else:
            box(c,2,3,20,18);c.circle(8.5,12,3.5)
            dimension_arrow(c,(17,17),(17,7),1.4)
    elif key=='ui.tools':
        # An original open-jaw wrench: circular head joined to a diagonal handle.
        pts=[(16,1.5),(16,6),(17,7),(21.5,7)]
        pts+=arc_points(16,7,5.5,0,90,12)[1:]
        pts += [(6,22),(2,18),(10.5,7)]
        pts+=arc_points(16,7,5.5,180,270,12)[1:-1]
        c.line(pts,closed=True,radius=1.7)
        c.line([(16,1.5),(16,6),(17,7),(21.5,7)],True,radius=1.7)
    elif key=='nav.go-to':
        c.line([(12,3),(21,3),(21,21),(12,21)],radius=.5)
        dimension_arrow(c,(2,12),(16,12),3)
    elif key=='data.apply-next':
        c.line([(3,10),(7,14),(13,6)],radius=.4)
        dimension_arrow(c,(12,19),(22,19),2.5)
    elif key.startswith('construction.'):
        for y in (4,10,16):box(c,3,y,12,4)
        name=key.split('.')[1]
        if name=='layer-add':c.plus(20,12,2.5,True)
        elif name=='layer-up':dimension_arrow(c,(20,20),(20,4),2)
        else:dimension_arrow(c,(20,4),(20,20),2)
    elif key=='evidence.file':
        paperclip(c)
        c.line([(17,5),(21,5),(21,20),(17,20)],True,radius=.3)
    elif key=='evidence.photo':
        box(c,3,3,18,18);c.circle(8,8,2)
        c.line([(3,18),(9,12),(13,16),(18,10),(21,13)],True,radius=.3)
    if key in SEMANTIC:
        # A status inherits one semantic currentColor, including in standalone SVG.
        for collection in (c.paths,c.circles,c.fills):
            for part in collection:part['tone']='primary'
    return True
