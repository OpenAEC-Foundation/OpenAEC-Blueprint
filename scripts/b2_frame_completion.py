"""Frame controls traced through mounted Svelte views and their callbacks."""
import math
from b2_second_series import box, cubic
from b2_session_two import dimension_arrow
from b2_energy_pile_audio import arc_points
from b2_bim_completion import cube

GROUPS={65:'Kozijnwerkruimtes',66:'Productie en toetsing',67:'Nieuwe kozijnen',
        68:'Kozijnvakken',69:'Vliesgevels en profielen',70:'Assistent en modeluitwisseling'}
ROWS=[
(65,'frame.editor','Kozijneditor','De 2D-kozijneditor openen via activeView editor.','4abb9addf40e06bd'),
(65,'frame.schedule','Kozijnstaat','De KozijnstaatView openen; geen staat direct exporteren.','9966e4d60fc33373'),
(65,'frame.production','Productiestaten','De ProductionListsView openen; geen productieplanning starten.','24e7a7bb1cedef83'),
(65,'frame.calculation','Kozijncalculatie','De CalculationView openen; geen berekening direct uitvoeren.','31a78c0b3b0e9bf0'),
(65,'frame.layout','Indelingswerkruimte','De daadwerkelijk gemonteerde LayoutProtoView openen.','b84bcc0b551a2706'),
(65,'profile.editor','Profielwerkruimte','De ProfileEditorView openen voor profielgeometrie.','1e745059b0e108e6'),
(65,'frame.energy','Kozijnenergie','De EnergyView openen; geen energielabel ophalen.','802cbcabb6e94118'),
(65,'frame.circularity','Circulariteit','De CircularityView openen voor materiaalhergebruik.','b57bf1ad08939dc0'),
(66,'frame.plausibility','Plausibiliteit','De PlausibilityView openen; geen directe validatiestart.','eec85273fb0c783a'),
(66,'frame.quotation','Kozijnoffertes','De QuotationView openen; geen PDF-export uitvoeren.','160a19e14817161f'),
(66,'bcf.workspace','BCF-werkruimte','De BcfView openen voor issues; geen issues verzenden.','8ceb9b19f510151c'),
(66,'frame.cnc','CNC-werkruimte','De CncView openen voor machinebewerkingen; geen G-code direct exporteren.','5df4f08f3a58a764'),
(66,'frame.procurement','Inkoopwerkruimte','De ProcurementView openen voor inkoopgegevens.','7d49f7690835651a'),
(66,'frame.combination','Kozijncombinaties','De CombinationView openen voor samengestelde kozijnen.','d9cc9f00996f1abd'),
(66,'validation.workspace','IDS-werkruimte','De IdsValidationView openen; geen IFC-validatie direct starten.','1f9c99b2cc0b785b'),
(66,'frame.certification','Certificeringswerkruimte','De CertificationView openen voor certificeringsgegevens.','184da85440380a24'),
(67,'frame.new','Nieuw leeg kozijn','createKozijn voegt een leeg kozijn van 1200 bij 1500 toe aan het project.','692b684b3818b4ac'),
(67,'frame.new-turn-tilt','Nieuw draaikiepkozijn','createFromTemplate single_turn_tilt maakt een nieuw draaikiepkozijn.','6450e39eab440eef'),
(67,'frame.new-double','Nieuw dubbel draaikiepkozijn','createFromTemplate double_turn_tilt maakt een nieuw dubbel kozijn.','85ecc65d8f4638dd'),
(67,'frame.new-sliding','Nieuwe schuifpui','createFromTemplate sliding_door maakt een nieuwe schuifpui.','58980f630cfa40ec'),
(67,'frame.new-door','Nieuwe voordeur','createFromTemplate front_door maakt een nieuw deurkozijn.','6c0261d544c81941'),
(67,'frame.new-top-hung','Nieuw klapraam','createFromTemplate klapraam maakt een nieuw klapraam.','a59659d5f8cfc727'),
(67,'frame.new-lift-slide','Nieuwe hefschuifpui','createFromTemplate hefschuif maakt een nieuwe hefschuifpui.','47af817f5d4f8498'),
(67,'frame.new-pivot','Nieuw pivotraam','createFromTemplate pivot maakt een nieuw pivotraam.','e8804e2725da710e'),
(67,'frame.new-french','Nieuw stolpkozijn','createFromTemplate stolp maakt een nieuw stolpkozijn.','59701edfd93a9cae'),
(68,'frame.column-add','Kozijnkolom toevoegen','addColumn verdeelt het actieve kozijn met een extra verticale stijl.','a97f10bb84fb4d5e'),
(68,'frame.row-add','Kozijnrij toevoegen','addRow verdeelt het actieve kozijn met een extra horizontale regel.','1a6dc6448cc7ce24'),
(68,'frame.cell-fixed','Vak met vast glas','quickSetPanel fixed wijzigt het geselecteerde kozijnvak in vast glas.','34816fc0b6df2043'),
(68,'frame.cell-turn-tilt','Vak draaikiep','quickSetPanel turn_tilt wijzigt het geselecteerde vak; geen nieuw kozijn.','1a1e88899b19fffa'),
(68,'frame.cell-sliding','Vak schuifraam','quickSetPanel sliding wijzigt het geselecteerde vak in een schuifraam.','2476187eeb8d2331'),
(68,'frame.cell-door','Vak deur','quickSetPanel door wijzigt het geselecteerde vak in een deur.','b220fc2a7f07bd5d'),
(68,'frame.cell-panel','Vak paneel','quickSetPanel panel wijzigt het geselecteerde vak in een dicht paneel.','cd1106c23c584861'),
(69,'curtain.new','Nieuwe lege vliesgevel','createVliesgevel maakt een nieuwe lege vliesgevel.','c9f198e90adbea1f'),
(69,'curtain.stick','Nieuwe stijl-regelgevel','createVgFromTemplate stick_system maakt een stijl-regelvliesgevel.','ef99d44253ccef06'),
(69,'curtain.unitized','Nieuwe elementengevel','createVgFromTemplate unitized maakt een elementenvliesgevel.','0b259892ce1766bc'),
(69,'profile.new','Nieuw profielconcept','profileEditor.newProfile reset de editor naar een nieuw profielconcept.','bd867bc242c3f605'),
(69,'profile.manage','Vormbeheer openen','De lintknop opent ShapeManager; niet dezelfde actie als een nieuw profielconcept.','d66140989dfbc464'),
(69,'profile.copy-as-new','Profiel als nieuw concept','Een kopie met id null en aangepaste naam in de editor laden; geen klembordactie.','76a6bdf9079c3e54'),
(69,'profile.point-delete','Profielpunten verwijderen','De editor in gereedschap delete zetten; volgende puntklikken verwijderen punten.','752e35b040dfa1bc'),
(69,'snap.grid','Aan raster snappen','profileEditor.toggleSnap schakelt geometrische rasteraantrekking.','ae4bb2be68b278f7'),
(70,'assistant.workspace','AI-assistent openen','Het AI-chatpaneel tonen; nog geen bericht versturen.','fa337f0066cd3629'),
(70,'chat.clear','Gesprek wissen','clearChat wist het assistentgesprek; projectgegevens blijven bestaan.','3455cc38621ca405'),
(70,'chat.send','Bericht versturen','handleSend controleert op lege invoer en stuurt de ingevoerde tekst via sendMessage.','c968df1d83cebf12'),
(70,'ifc.roundtrip-compare','IFC-rondgang vergelijken','Een IFC-bestand kiezen en compare_ifc_roundtrip met het actieve project aanroepen.','6104e8a1fb643771'),
(70,'ifc.compare-files','Twee IFC-bestanden vergelijken','Twee bestanden kiezen en compare_ifc_files aanroepen; geen projectrondgang.','0a7baf1a55a5cc99'),
(70,'integration.send-model','Model naar Blender sturen','send_to_blender aanroepen met het geselecteerde kozijn-id.','e1bb0384a9a8abb2'),
(70,'integration.test-connection','Verbinding testen','check_blender_connection aanroepen en het resultaat als melding tonen.','8f5d594a2e1c5311'),
]
KEYS={k for _,k,_,_,_ in ROWS}
ACCENT_FRONT={k:'De bepalende markering blijft ononderbroken voor de achterliggende contour.' for k in KEYS if k.startswith(('frame.new','frame.column','frame.row','profile.','snap.','ifc.','chat.','integration.'))}
REUSED={
'3fd748618fc6e8da':('bim.workspace','activeView viewer3d opent Viewer3D; modelwerkruimte, geen import.'),
'076ac40ba6843312':('field.dashboard','DashboardView toont projectstatistieken; dezelfde dashboardbetekenis met appcontext.'),
'eff6499eeb86894a':('planning.cut-list','App opent dezelfde CutOptimizationView als het al beoordeelde zaagplancontract.'),
'51270dc9bebf0453':('panel.left','toggleLeftPane vouwt het linkerpaneel in of uit.'),
'9cbc4bcf1e7ea9ab':('panel.right','toggleRightPane vouwt het rechterpaneel in of uit.'),
'a5e110368f9115b0':('panel.left','De 3D-layout gebruikt dezelfde toggleLeftPane.'),
'cc5c8f9bcd75df60':('panel.right','De 3D-layout gebruikt dezelfde toggleRightPane.'),
'8f7d2a7a5d7f656c':('assistant.workspace','Kopaanduiding van het geopende assistentpaneel.'),
'919f7ea7835cbd89':('ui.settings','showConfig opent assistentvoorkeuren; de paneelcontext bepaalt het bereik.'),
'c3ccdb8214deaed6':('ui.close','ShapeManager sluiten; geen appvenster sluiten.'),
'c024d75bbd5698ea':('view.fit','zoomToFit past het profiel aan het canvas aan.'),
'4c79b470a4839826':('view.search','Zoekveld filtert profielnamen in de bibliotheek.'),
'14326b70b845f242':('tree.expand','Categorie in de profielbibliotheek uitvouwen.'),
'2d43bef29022ba39':('profile.copy-as-new','Tweede profielcategorie gebruikt dezelfde kopie-als-concept-handler.'),
'771110594b9e75b1':('file.save','handleSave bewaart de aangepaste profielgegevens.'),
'bdec7ef69edada86':('transform.mirror','mirrorH spiegelt de profielgeometrie horizontaal.'),
'c201cb39da6c5c27':('transform.flip-vertical','mirrorV spiegelt de profielgeometrie verticaal.'),
'da26ee1b282c1b5c':('edit.undo','Profieleditor undo.'),'1c86a62216326396':('edit.redo','Profieleditor redo.'),
'0986b51d4fabac24':('file.new','fileNew maakt na de bewaarprompt een nieuw project.'),
'e579d0e9a2dc2108':('file.open','fileOpen kiest en opent een ofs-project.'),
'bd7276e1895c59f1':('file.save','fileSave bewaart het project.'),
'77719059da5ea488':('file.save-as','fileSaveAs kiest een nieuw projectpad.'),
'0f34a292b77eb780':('link.open-external','openExternal opent de GitHub-repository.'),
'dab3eb75c8b95359':('feedback.github-issue','openExternal opent de GitHub-issuepagina; publiceert geen issue.'),
'4cb0a7dbfcf98832':('ui.help','De wiki/documentatie extern openen.'),
'9c840cc547032cef':('file.new','De tweede menuplaats gebruikt fileNew.'),
'cd1c228f2bee599d':('file.open','De tweede menuplaats gebruikt fileOpen.'),
'9e4f56cb9b81bf12':('edit.duplicate','duplicateKozijn maakt een apart kozijn met nieuwe id.'),
'5945251fcf9858fd':('edit.delete','removeKozijn verwijdert na bevestiging het actieve kozijn.'),
'a26c153f76dd1a70':('file.import','importDxfProfile kiest DXF, leest profieldata en voegt die toe aan aangepaste profielen.'),
'3d41a189ceb5173a':('file.import','importCatalog kiest JSON/Excel/CSV en voegt de gelezen profielen toe.'),
'9dd341bd7227b9c9':('frame.column-add','De tweede lintplaats roept dezelfde handleAddColumn aan.'),
'c140b0a8a93187fb':('frame.row-add','De tweede lintplaats roept dezelfde handleAddRow aan.'),
'50deb09e1e5ddd2c':('ifc.export','exportIfc kiest een IFC-bestemming en roept export_ifc aan.'),
'32c3654690018ef3':('file.export','exportDxf schrijft het actieve kozijn als DXF.'),
'd275af3f7f68585a':('validation.workspace','De lintknop opent dezelfde IDS-werkruimte.'),
'2cff1b95d44336cb':('frame.certification','De lintknop opent dezelfde certificeringswerkruimte.'),
'1179442512810e44':('file.export','exportKozijnstaat pdf schrijft de kozijnstaat als PDF.'),
'baac16dc010e7d93':('file.export','exportKozijnstaat xlsx schrijft de kozijnstaat als Excel.'),
'b6f5a837506e1e7e':('file.export','exportWorkshop schrijft de werkplaatstekening als PDF.'),
'f42a893b23b04099':('file.export','exportGltf schrijft het geselecteerde kozijn als GLB.'),
'0c3df98490b746ad':('file.export','exportProduction pdf schrijft productiestaten als PDF.'),
'27ee1986c5fb94c1':('file.export','exportProduction xlsx schrijft productiestaten als Excel.'),
'97c4be3ac0b13fb1':('file.export','exportProduction csv schrijft productiestaten als CSV.'),
'0a82ceead64521ed':('file.export','exportCncGcode kiest de bestemming en roept export_cnc_gcode aan.'),
'2fb816292f6a7ecd':('file.export','exportLabels schrijft productie-etiketten als PDF.'),
'ce96bbb79b54cbd3':('planning.production','De lintknop opent de reeds beoordeelde PlanningView.'),
'0da9129d6b91bab5':('frame.cnc','De lintknop opent dezelfde CncView.'),
'b39a36952a112108':('frame.procurement','De lintknop opent dezelfde ProcurementView.'),
'8cbf0f25bc27d5d8':('edit.undo','Lint undo.'),'0ef3fae5ecb4b1ea':('edit.redo','Lint redo.'),
'f7ff97caf4fa51ce':('ui.close','Instellingendialoog sluiten.'),
'6ca893be0d3128ea':('ui.settings','Het tabblad met algemene appvoorkeuren openen.'),
'e12b82f420d58509':('ui.about','Het tabblad met appinformatie openen.'),
'ce361144227ecf70':('status.warning','Waarschuwing bij bedienbare vakken zonder hardwareSet; geen hardware toevoegen.'),
'77854d8ee80c5c34':('ui.settings','Titelbalk opent instellingen.'),
'5748cdbb110a1e91':('edit.undo','Titelbalk undo.'),'ce38decfb82f328b':('edit.redo','Titelbalk redo.'),
'72fe306a5da72031':('window.minimize','Titelbalk minimize.'),
'ce65c4197a7fe9fd':('window.restore','Titelbalk unmaximize.'),
'ee7cd73a72cf210a':('window.maximize','Titelbalk maximize.'),
'd24653775a0d3ce3':('ui.close','toast.dismiss sluit de melding; geen venstersluiting.'),
}
EXCLUDED={r:'Frame-beeldmerk of favicon; geen vast bedieningsicoon.' for r in ('d332c85db73c39f3','6af5d304b4fb2190','b2c4334d838905b2','24d9d2cb6a4e3423')}


def frame(c):box(c,3,3,18,18)


def profile(c,accent=False):
    c.line([(4,3),(10,3),(10,9),(20,9),(20,15),(10,15),(10,21),(4,21)],accent,closed=True,radius=.4)


def chat(c):
    c.line([(3,3),(21,3),(21,17),(9,17),(3,22)],closed=True,radius=.6)


def window_type(c,kind):
    frame(c)
    if kind=='double':c.line([(12,3),(12,21)],radius=0)
    if kind=='turn-tilt':
        # Two opening indicators in separate lanes, without crossing triangles.
        c.line([(7,10),(10,13),(7,16)],True,radius=0)
        c.line([(13,7),(15,10),(17,7)],True,radius=0)
    elif kind in {'double','french'}:
        c.line([(6.8,7.5),(8,12),(6.8,16.5)],True,radius=0)
        c.line([(17.2,7.5),(16,12),(17.2,16.5)],True,radius=0)
    elif kind=='sliding':
        dimension_arrow(c,(7,9),(16,9),1.2)
        dimension_arrow(c,(17,15),(8,15),1.2)
    elif kind=='lift-slide':
        dimension_arrow(c,(7,16),(12,16),1.2)
        dimension_arrow(c,(16.2,16),(16.2,7),1)
    elif kind=='door':
        c.line([(7,17),(7,7),(17,7),(17,17)],True,radius=.3)
        c.circle(14,13,.7,True,True)
    elif kind=='top-hung':c.line([(7,7),(12,17),(17,7)],True,radius=0)
    elif kind=='pivot':
        c.line([(12,7),(12,17)],True,radius=0)
        c.line([(8,9),(16,15)],True,radius=0)
    elif kind=='fixed':
        c.line([(7,17),(17,7)],True,radius=0)
        if c.size!=16:c.line([(11,18),(18,11)],True,radius=0)
    elif kind=='panel':
        box(c,7,7,10,10,True)
        c.line([(7,12),(17,12)],True,radius=0)


def circular_arrow(c,x,y,r,start,end,head=2.4):
    c.line(arc_points(x,y,r,start,end),True,radius=0)
    t=math.radians(end);tip=(x+r*math.cos(t),y+r*math.sin(t))
    ux,uy=-math.sin(t),math.cos(t)
    c.line([(tip[0]-head*ux-head*uy,tip[1]-head*uy+head*ux),tip,
            (tip[0]-head*ux+head*uy,tip[1]-head*uy-head*ux)],True,radius=0)


def extend(c,key):
    if key not in KEYS:return False
    small=c.size==16
    if key.startswith('frame.new'):
        kind=key.removeprefix('frame.new-') if key!='frame.new' else ''
        window_type(c,kind)
        # New-object marker outside a reduced window motif.
        s=c.size/24
        for p in c.paths:p['points']=[(.73*x,.73*y) for x,y in p['points']]
        for p in c.circles:p.update(x=p['x']*.73,y=p['y']*.73,r=p['r']*.73)
        c.plus(19,19,3,True)
    elif key.startswith('frame.cell-'):window_type(c,key.removeprefix('frame.cell-'))
    elif key=='frame.editor':
        box(c,2,8,14,14)
        c.line([(2,15),(9,15),(9,22)],radius=0)
        dimension_arrow(c,(22,2),(18,6),1.8)
    elif key=='frame.schedule':
        box(c,3,3,18,18)
        c.line([(3,9),(21,9)],True,radius=0)
        c.line([(9,9),(9,21)],radius=0)
        for y in (13,17):c.line([(3,y),(21,y)],radius=0)
    elif key=='frame.production':
        c.line([(3,21),(3,10),(9,6),(9,10),(15,6),(15,12),(21,12),(21,21)],closed=True,radius=.4)
        for x in (7,12,17):c.line([(x,16),(x,18)],True,radius=0)
    elif key=='frame.calculation':
        box(c,4,2,16,20);box(c,7,5,10,4,True)
        for x,y in ((8,13),(16,13),(8,18),(16,18)):c.circle(x,y,.8,False,True)
    elif key=='frame.layout':
        frame(c);c.line([(3,10),(21,10)],radius=0)
        c.line([(10,10),(10,21)],True,radius=0)
        c.line([(10,16),(21,16)],True,radius=0)
    elif key in {'profile.editor','profile.new','profile.manage','profile.copy-as-new'}:
        profile(c)
        if key=='profile.editor':c.line([(14,3),(20,3)],True,radius=0)
        else:
            for p in c.paths:p['points']=[(.7*x,.7*y) for x,y in p['points']]
            if key=='profile.new':c.plus(19,19,3,True)
            elif key=='profile.copy-as-new':box(c,10,10,11,12,True)
            else:
                c.circle(19,18,3,True);c.line([(19,13),(19,15)],True,radius=0);c.line([(19,21),(19,23)],True,radius=0)
    elif key=='frame.energy':
        frame(c)
        c.line([(13,5),(8,13),(12,13),(10,19),(17,10),(13,10)],True,closed=True,radius=.2)
    elif key=='frame.circularity':
        # A reusable panel inside the return cycle, rather than an energy bolt.
        box(c,8,7,8,10)
        c.line([(8,12),(16,12)],radius=0)
        circular_arrow(c,12,12,10,220,490,2)
    elif key in {'frame.plausibility','validation.workspace'}:
        frame(c)
        if key=='frame.plausibility':
            c.line([(12,6),(12,13)],True,radius=0);c.circle(12,17,.8,True,True)
        else:
            c.line([(7,7),(10,10),(17,5)],True,radius=.3)
            for y in (14,18):c.line([(7,y),(17,y)],radius=0)
    elif key=='frame.quotation':
        box(c,4,2,16,20)
        for y in (6,10):c.line([(8,y),(16,y)],radius=0)
        c.line([(8,16),(16,16)],True,radius=0);c.line([(12,13),(12,19)],True,radius=0)
    elif key=='bcf.workspace':
        chat(c)
        for y in (8,12):c.line([(7,y),(17,y)],True,radius=0)
    elif key=='frame.cnc':
        c.line([(3,21),(21,21),(21,4),(3,4)],radius=.5)
        c.line([(12,4),(12,10),(9,10),(12,15),(15,10),(12,10)],True,radius=.2)
        c.line([(6,18),(18,18)],radius=0)
    elif key=='frame.procurement':
        c.line([(3,11),(21,11),(19,22),(5,22)],closed=True,radius=.7)
        cubic(c,[(8,7),(8,1),(16,1),(16,7)],True)
    elif key=='frame.combination':
        box(c,2,5,8,14);box(c,14,5,8,14)
        c.line([(8,12),(16,12)],True,radius=0)
    elif key=='frame.certification':
        c.circle(12,9,6)
        c.line([(8,14),(6,22),(12,19),(18,22),(16,14)],radius=.4)
        c.line([(9,9),(11,11),(15,7)],True,radius=.3)
    elif key in {'frame.column-add','frame.row-add'}:
        frame(c)
        # An inset divider and a detached add marker share one layout.
        for path in c.paths:path['points']=[(.72*x,.72*y) for x,y in path['points']]
        if key=='frame.column-add':c.line([(8.64,5),(8.64,12.3)],True,radius=0)
        else:c.line([(5,8.64),(12.3,8.64)],True,radius=0)
        c.plus(20,20,2.5,True)
    elif key.startswith('curtain.'):
        frame(c)
        if key!='curtain.new':
            for x in (9,15):c.line([(x,3),(x,21)],True,radius=0)
            c.line([(3,12),(21,12)],True,radius=0)
            if key=='curtain.unitized':
                for x in (9,15):
                    for y in (6,18):c.circle(x,y,1.6,False,True)
        else:c.plus(12,12,3,True)
    elif key=='profile.point-delete':
        c.line([(4,21),(4,5),(14,5)],radius=0)
        for x,y in ((4,21),(4,5),(14,5)):c.circle(x,y,1.3,filled=True)
        c.line([(16,14),(22,20)],True,radius=0)
        c.line([(16,20),(22,14)],True,radius=0)
    elif key=='snap.grid':
        # Snap to one explicit grid intersection; reserve clear space around it.
        for t in (5,19):
            c.line([(t,3),(t,21)],radius=0)
            c.line([(3,t),(21,t)],radius=0)
        for a,b in ((3,8),(16,21)):
            c.line([(12,a),(12,b)],radius=0)
            c.line([(a,12),(b,12)],radius=0)
        c.circle(12,12,1.75,True,filled=True)
    elif key=='assistant.workspace':
        chat(c)
        c.circle(8,8,.8,True,True);c.circle(16,8,.8,True,True)
        c.line([(8,12),(16,12)],True,radius=0)
    elif key=='chat.clear':
        chat(c);c.line([(8,7),(16,13)],True,radius=0);c.line([(8,13),(16,7)],True,radius=0)
    elif key=='chat.send':
        c.line([(2,3),(22,12),(2,21),(7,12)],closed=True,radius=.4)
        c.line([(7,12),(22,12)],True,radius=0)
    elif key in {'ifc.roundtrip-compare','ifc.compare-files','integration.send-model'}:
        cube(c)
        for p in c.paths:p['points']=[(.65*x,.65*y) for x,y in p['points']]
        if key=='ifc.roundtrip-compare':
            circular_arrow(c,16,17,5,0,270,1.7)
        elif key=='ifc.compare-files':
            box(c,12,11,10,11)
            c.line([(15,15),(20,15)],True,radius=0);c.line([(15,18),(20,18)],True,radius=0)
        else:dimension_arrow(c,(13,19),(22,19),2.5)
    elif key=='integration.test-connection':
        c.line([(3,7),(8,7),(11,10),(13,10),(16,7),(21,7)],radius=.4)
        c.line([(3,17),(8,17),(11,14),(13,14),(16,17),(21,17)],radius=.4)
        c.line([(7,21),(11,23),(18,18)],True,radius=.3)
    return True
