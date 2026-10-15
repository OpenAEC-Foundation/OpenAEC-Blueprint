//! Native rendition of the proposed ribbon groups in design/harmonized-template.html.
//! FEM/BIM SVGs are review drafts, supplied as application-owned vectors.
use super::*;

macro_rules! planner_source_icon {
    ($name:literal) => {
        CommandIcon::Svg(include_bytes!(concat!(
            "../../../harmonization/library-icons/lucide-static/0.575.0/",
            $name,
            ".svg"
        )))
    };
}
macro_rules! pdf_image_icon {
    ($name:literal) => {
        CommandIcon::Svg(include_bytes!(concat!("../../../design/pdf-image-icons/", $name, ".svg")))
    };
}
macro_rules! pdf_arrange_icon {
    ($name:literal) => {
        CommandIcon::Svg(include_bytes!(concat!("../../../design/pdf-arrange-icons/", $name, ".svg")))
    };
}
macro_rules! pdf_format_icon {
    ($name:literal) => {
        CommandIcon::Svg(include_bytes!(concat!("../../../design/pdf-format-icons/", $name, ".svg")))
    };
}

#[derive(Debug, Clone, Copy)]
pub(super) struct PileViewState {
    pub symbol_scale: f32,
    pub utilization_minimum: f32,
    pub utilization_maximum: f32,
    pub foreground: usize,
}
impl Default for PileViewState {
    fn default() -> Self {
        Self { symbol_scale: 100.0, utilization_minimum: 20.0, utilization_maximum: 80.0, foreground: 0 }
    }
}

#[derive(Debug, Clone, Copy)]
pub(super) struct FrameViewState {
    pub template: usize,
    pub lod: usize,
    pub theme: usize,
}
impl Default for FrameViewState {
    fn default() -> Self { Self { template: 0, lod: 1, theme: 0 } }
}

#[derive(Debug, Clone, Copy)]
pub(super) struct PdfImageState {
    pub crop: bool,
    pub grayscale: bool,
    pub brightness: f32,
    pub contrast: f32,
}
impl Default for PdfImageState {
    fn default() -> Self { Self { crop: false, grayscale: false, brightness: 100.0, contrast: 100.0 } }
}

#[derive(Debug, Clone, Copy, Default)]
pub(super) struct PdfArrangeState { pub align_target: usize }

#[derive(Debug, Clone)]
pub(super) struct PdfFormatState {
    pub style: usize,
    pub fill: usize,
    pub stroke: usize,
    pub fill_color: iced::Color,
    pub stroke_color: iced::Color,
    pub line_width: String,
    pub border: usize,
    pub blend: usize,
    pub opacity: f32,
    pub arrow_start: usize,
    pub arrow_end: usize,
    pub layer: usize,
    pub symbol_stamp: bool,
}
impl Default for PdfFormatState {
    fn default() -> Self {
        Self { style: usize::MAX, fill: 0, stroke: 5, fill_color: iced::Color::WHITE,
            stroke_color: iced::Color::BLACK, line_width: "1".into(), border: 0,
            blend: 0, opacity: 100.0, arrow_start: 0, arrow_end: 1, layer: 0,
            symbol_stamp: false }
    }
}
impl PdfFormatState {
    pub fn select_style(&mut self, index: usize) {
        const COLORS: [&str; 10] = ["#ff0000", "#800080", "#4b0082", "#0066cc", "#008000",
            "#e6a817", "#000000", "#ff0000", "#800080", "#7b68ee"];
        self.style = index.min(9);
        self.stroke_color = pdf_color(COLORS[self.style]);
        self.stroke = PDF_FORMAT_PALETTE.iter().position(|hex| *hex == COLORS[self.style]).unwrap_or(usize::MAX);
        self.fill_color = if self.style >= 7 {
            iced::Color { a: if self.style == 9 { 0.15 } else { 0.08 }, ..self.stroke_color }
        } else { iced::Color::WHITE };
        self.fill = usize::MAX;
        self.border = 0;
    }
    pub fn select_fill(&mut self, index: usize) {
        self.fill = index.min(PDF_FORMAT_PALETTE.len() - 1);
        self.fill_color = pdf_color(PDF_FORMAT_PALETTE[self.fill]);
        self.style = usize::MAX;
    }
    pub fn select_stroke(&mut self, index: usize) {
        self.stroke = index.min(PDF_FORMAT_PALETTE.len() - 1);
        self.stroke_color = pdf_color(PDF_FORMAT_PALETTE[self.stroke]);
        self.style = usize::MAX;
    }
}

#[cfg(test)]
pub(super) fn studio_tabs(studio: &StudioLayout, selected: Option<&str>) -> Vec<RibbonTab<Action>> {
    studio_tabs_with_controls(studio, selected, PileViewState::default(), FrameViewState::default(), PdfImageState::default(), PdfArrangeState::default(), PdfFormatState::default())
}

pub(super) fn studio_tabs_with_controls(
    studio: &StudioLayout,
    selected: Option<&str>,
    pile: PileViewState,
    frame: FrameViewState,
    pdf_image: PdfImageState,
    pdf_arrange: PdfArrangeState,
    pdf_format: PdfFormatState,
) -> Vec<RibbonTab<Action>> {
    studio
        .tabs
        .iter()
        .filter(|tab| tab.as_str() != "Bestand")
        .map(|tab| RibbonTab {
            id: tab.to_lowercase(),
            label: if studio.optional_tabs.contains(tab) {
                format!("{tab} · optioneel")
            } else {
                tab.clone()
            },
            groups: (studio.id == "field").then(Vec::new)
                .or_else(|| pdf_groups(studio, tab, selected, pdf_image, pdf_arrange, pdf_format.clone()))
                .or_else(|| pointcloud_groups(studio, tab, selected))
                .or_else(|| cad_groups(studio, tab, selected))
                .or_else(|| extension_2d_groups(studio, tab, selected))
                .or_else(|| planner_groups(studio, tab, selected))
                .or_else(|| frame_groups(studio, tab, selected, frame))
                .or_else(|| calc_groups(studio, tab, selected))
                .or_else(|| geotech_groups(studio, tab, selected))
                .or_else(|| heatloss_groups(studio, tab, selected))
                .or_else(|| calculations_groups(studio, tab, selected))
                .or_else(|| reports_groups(studio, tab, selected))
                .or_else(|| validator_groups(studio, tab, selected))
                .or_else(|| pile_groups(studio, tab, selected, pile))
                .or_else(|| domain_groups(studio, tab, selected))
                .unwrap_or_else(|| base_groups(tab, selected)),
        })
        .collect()
}

/// Public Tauri/Solid PDF ribbon at f754cb7c9d9a. Image and Arrange use
/// native review controls; PDF document editing remains outside this atlas.
fn pdf_groups(studio: &StudioLayout, tab: &str, selected: Option<&str>, image: PdfImageState, arrange: PdfArrangeState, format: PdfFormatState) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "pdf" { return None; }
    if tab == "Schikken" { return Some(pdf_arrange_groups(selected, arrange)); }
    if tab == "Opmaak" { return Some(pdf_format_groups(selected, format)); }
    let spec: &[(&str, &[&str])] = match tab {
        "Start" => &[("Document", &["Nieuw", "Naar CAD", "IFC-report", "E-mail", "Raster-PDF"]),
            ("Hulpmiddelen", &["Hand", "Selecteren"]), ("Beeld", &["Inzoomen", "Uitzoomen", "Breedte passend", "Pagina passend"]),
            ("Navigeren", &["Eerste", "Vorige", "Volgende", "Laatste"]), ("Zoeken", &["Zoeken"]),
            ("Instellingen", &["Voorkeuren", "Vorige versie"])],
        "Beeld" => &[("Paginaweergave", &["Enkel", "Doorlopend", "Boek", "Naast elkaar"]),
            ("Weergave", &["Dunne lijnen", "Leesmodus"]), ("Panelen", &["Navigatie", "Eigenschappen", "Annotaties", "Lagen"]),
            ("Weergave", &["Weergavekeuzes · controls"]), ("Vergelijken", &["PDF's vergelijken"]),
            ("Venster", &["Volledig scherm", "Toetsaanslagen"])],
        "Tekenen" => &[("Selectie", &["Selecteren", "Hand", "Alles selecteren", "Deselecteren"]),
            ("Tekenen", &["Vormkiezer · controls"]), ("Lijn", &["Lijnkeuzes · controls"]),
            ("Knipsel", &["Vectorknipsel", "Plak knipsel"]), ("Schaal", &["Schaalgebied", "Schaalgebied op pagina"]),
            ("Annoteren", &["Oppervlakte", "Lengte", "Maatlijn", "Hoek", "Coördinaat"]),
            ("Wijzigen", &["Verplaatsen", "Kopiëren", "Spiegelen H", "Spiegelen V", "Reeks"]),
            ("Bewerken", &["Inkorten", "Verlengen", "Verschuiven", "Afronden", "Afkanten"]),
            ("Klembord", &["Plakken", "Plakken op plaats", "Knippen", "Kopiëren", "Verwijderen"]),
            ("Verzameling", &["Aanmaken", "Ontleden"])],
        "Annotatie" => &[("Tekening", &["Markeren"]), ("Tekst", &["Tekstvak", "Bijschrift", "Notitie"]),
            ("Stempel", &["Stempel", "Handtekening", "Parametrisch symbool"]),
            ("Redactie", &["Redigeren", "Toepassen"]), ("Eigenschappen", &["Annotatie-eigenschappen · controls"]),
            ("Bewerken", &["Pagina wissen", "Alles wissen"]),
            ("METEN", &["Afstand", "Oppervlakte", "Omtrek", "Hoek"]), ("HOEVEELHEDEN", &["Hoeveelheden"])],
        "PDF bewerken & samenvoegen" => &[("Bewerken", &["Tekst bewerken", "Tekst toevoegen", "Tekst herkennen (OCR)", "Bijsnijden"]),
            ("Pagina's", &["Invoegen", "Verwijderen", "Extraheren", "Volgorde"]),
            ("Combineren", &["Samenvoegen", "PDF's vergelijken"]),
            ("Watermerk", &["Watermerk", "Koptekst/voettekst", "Beheren"])],
        "Help" => &[("Instellingen", &["Extensies", "Bestandskoppelingen"]),
            ("Help", &["Sneltoetsen", "Over", "Wat is nieuw", "Updates", "Diagnose"])],
        "Afbeelding" => &[("Bijsnijden", &[]), ("Beeldbewerking", &[])],
        _ => return None,
    };
    let mut groups: Vec<RibbonGroup<Action>> = spec.iter().map(|(label, items)| RibbonGroup { label: (*label).into(), commands: items.iter().map(|name| {
        let id = format!("pdf:{tab}:{name}");
        let icon = if name.contains("PDF") || name.contains("Nieuw") { Icon::New }
            else if name.contains("Zoek") { Icon::Search }
            else if name.contains("Afstand") || name.contains("Oppervlakte") || name.contains("Hoek") || name.contains("Maat") { Icon::Measure }
            else if name.contains("Export") || name.contains("Samenvoegen") { Icon::Export }
            else if name.contains("Eigenschap") || name.contains("keuze") || name.contains("controls") { Icon::Settings }
            else if name.contains("Pagina") || name.contains("Beeld") || name.contains("Volledig") { Icon::Fit }
            else { Icon::Grid };
        Command::new(*name, icon, Action::SelectPreviewCommand(id.clone())).selected(selected == Some(id.as_str()))
    }).collect() }).collect();
    if tab == "Afbeelding" {
        groups[0].commands.push(Command::new("Croppen", pdf_image_icon!("cropIcon"), Action::PdfCrop).selected(image.crop));
        groups[1].commands.push(Command::new("Grijswaarden", pdf_image_icon!("grayscaleIcon"), Action::PdfGrayscale).selected(image.grayscale));
        groups[1].commands.push(Command::new("Herstellen", pdf_image_icon!("resetAdjustIcon"), Action::PdfResetImage));
        groups[1].commands.push(Command::new("Beeldregelaars", Icon::Settings, Action::PdfResetImage)
            .control(RibbonControl::Sliders { minimum: 0.0, maximum: 200.0, step: 1.0, unit: "%", width: 226.0,
                items: vec![
                    RibbonSlider { label: "Helderheid".into(), icon: pdf_image_icon!("brightnessIcon"), value: image.brightness, on_change: Action::PdfBrightness },
                    RibbonSlider { label: "Contrast".into(), icon: pdf_image_icon!("contrastIcon"), value: image.contrast, on_change: Action::PdfContrast },
                ] }));
    }
    Some(groups)
}

/// All six ArrangeTab groups and their UI-used SVGs at f754cb7c9d9a.
fn pdf_arrange_groups(selected: Option<&str>, arrange: PdfArrangeState) -> Vec<RibbonGroup<Action>> {
    let group = |label: &str, actions: Vec<(&str, &str, CommandIcon)>| RibbonGroup {
        label: label.into(),
        commands: actions.into_iter().map(|(id, label, icon)| {
            let id = format!("pdf:Schikken:{id}");
            Command::new(label, icon, Action::SelectPreviewCommand(id.clone()))
                .selected(selected == Some(id.as_str()))
        }).collect(),
    };
    let mut groups = vec![
        group("Uitlijning", vec![
            ("align-left", "Links", pdf_arrange_icon!("alignLeftIcon")),
            ("align-center", "Midden", pdf_arrange_icon!("alignCenterIcon")),
            ("align-right", "Rechts", pdf_arrange_icon!("alignRightIcon")),
            ("align-top", "Boven", pdf_arrange_icon!("alignTopIcon")),
            ("align-middle", "Midden", pdf_arrange_icon!("alignMiddleIcon")),
            ("align-bottom", "Onder", pdf_arrange_icon!("alignBottomIcon")),
        ]),
        group("Verdelen", vec![
            ("space-h", "Horiz. verd.", pdf_arrange_icon!("distSpaceHIcon")),
            ("space-v", "Vert. verd.", pdf_arrange_icon!("distSpaceVIcon")),
            ("dist-left", "Links", pdf_arrange_icon!("distLeftIcon")),
            ("dist-top", "Boven", pdf_arrange_icon!("distTopIcon")),
            ("dist-center", "Midden", pdf_arrange_icon!("distCenterIcon")),
            ("dist-middle", "Midden", pdf_arrange_icon!("distMiddleIcon")),
            ("dist-right", "Rechts", pdf_arrange_icon!("distRightIcon")),
            ("dist-bottom", "Onder", pdf_arrange_icon!("distBottomIcon")),
        ]),
        group("Grootte", vec![
            ("same-size", "Zelfde grootte", pdf_arrange_icon!("sameSize16Icon")),
            ("same-width", "Zelfde breedte", pdf_arrange_icon!("sameSize16Icon")),
            ("same-height", "Zelfde hoogte", pdf_arrange_icon!("sameSize16Icon")),
        ]),
        group("Draaien", vec![
            ("rotate-ccw", "90° linksom", pdf_arrange_icon!("rotateCcwIcon")),
            ("rotate-cw", "90° rechtsom", pdf_arrange_icon!("rotateCwIcon")),
            ("rotate-180", "180°", pdf_arrange_icon!("rotate180Icon")),
        ]),
        group("Spiegelen", vec![
            ("flip-h", "Horizontaal", pdf_arrange_icon!("flipHIcon")),
            ("flip-v", "Verticaal", pdf_arrange_icon!("flipVIcon")),
        ]),
        group("Z-volgorde", vec![
            ("bring-forward", "Naar voren", pdf_arrange_icon!("bringForwardIcon")),
            ("bring-front", "Naar voorgrond", pdf_arrange_icon!("bringToFrontIcon")),
            ("send-backward", "Naar achteren", pdf_arrange_icon!("sendBackwardIcon")),
            ("send-back", "Naar achtergrond", pdf_arrange_icon!("sendToBackIcon")),
        ]),
    ];
    groups[0].commands.push(Command::new("Uitlijnen op", Icon::Grid, Action::PdfAlignTarget(arrange.align_target))
        .control(RibbonControl::Select { options: vec![
            ("Uitlijnen op selectie".into(), Action::PdfAlignTarget(0)),
            ("Uitlijnen op laatst geselecteerde".into(), Action::PdfAlignTarget(1)),
        ], selected: arrange.align_target, width: 220.0, show_label: false }));
    groups
}

pub(super) const PDF_FORMAT_PALETTE: [&str; 42] = [
    "#ffffff", "#d9d9d9", "#999999", "#666666", "#333333", "#000000",
    "#f4cccc", "#ea9999", "#e06666", "#ff0000", "#cc0000", "#660000",
    "#fce5cd", "#f9cb9c", "#ffff00", "#ffd966", "#f1c232", "#bf9000",
    "#d9ead3", "#b6d7a8", "#93c47d", "#00ff00", "#38761d", "#274e13",
    "#d0e0e3", "#a2c4c9", "#76a5af", "#00ffff", "#45818e", "#134f5c",
    "#c9daf8", "#6d9eeb", "#4a86e8", "#0000ff", "#1155cc", "#073763",
    "#d9d2e9", "#b4a7d6", "#9900ff", "#ff00ff", "#a64d79", "#741b47",
];

pub(super) fn pdf_color(hex: &str) -> iced::Color {
    let part = |range| u8::from_str_radix(&hex[range], 16).expect("pinned PDF palette hex");
    iced::Color::from_rgb8(part(1..3), part(3..5), part(5..7))
}

/// FormatTab values and order at f754cb7c9d9a. Commands select a review
/// state; document editing and conditional symbol-insert behavior live in PDF.
fn pdf_format_groups(selected: Option<&str>, format: PdfFormatState) -> Vec<RibbonGroup<Action>> {
    let preview = |id: &str, label: &str, icon: CommandIcon| {
        let key = format!("pdf:Opmaak:{id}");
        Command::new(label, icon, Action::SelectPreviewCommand(key.clone()))
            .selected(selected == Some(key.as_str()))
    };
    let style_names = ["Rood", "Paars", "Indigo", "Blauw", "Groen", "Geel", "Zwart",
        "Rood bewolkt", "Paars bewolkt", "Indigo bewolkt"];
    let style_colors = ["#ff0000", "#800080", "#4b0082", "#0066cc", "#008000", "#e6a817",
        "#000000", "#ff0000", "#800080", "#7b68ee"];
    let styles = style_names.into_iter().enumerate().map(|(index, label)| {
        let color = pdf_color(style_colors[index]);
        openaec_ui::RibbonSwatch { label: label.into(), color,
            background: if index >= 7 { iced::Color { a: 0.15, ..color } } else { iced::Color::WHITE },
            message: Action::PdfFormatStyle(index) }
    }).collect();
    let colors = |action: fn(usize) -> Action| PDF_FORMAT_PALETTE.iter().enumerate()
        .map(|(index, hex)| (hex.to_string(), pdf_color(hex), action(index))).collect();
    let pick = |label: &str, choices: &[&str], index: usize, action: fn(usize) -> Action, width: f32| {
        Command::new(label, Icon::Settings, action(index)).control(RibbonControl::Select {
            options: choices.iter().enumerate().map(|(i, label)| (label.to_string(), action(i))).collect(),
            selected: index, width, show_label: true })
    };
    let arrows = ["Geen", "Open", "Gesloten", "Stealth", "Ruit", "Cirkel", "Vierkant", "Schuine streep"];
    let mut groups = Vec::new();
    if format.symbol_stamp {
        groups.push(RibbonGroup { label: "Symbooltype".into(), commands: vec![
            preview("edit-type", "Type bewerken", pdf_format_icon!("editTypeIcon"))] });
    }
    groups.extend([
        RibbonGroup { label: "Stijlen".into(), commands: vec![
            Command::new("Stijlgalerij", Icon::Grid, Action::PdfFormatStyle(0))
                .control(RibbonControl::StyleGallery { items: styles, selected: format.style }),
            preview("more-styles", "Meer", Icon::Grid.into()),
        ] },
        RibbonGroup { label: "Kleur".into(), commands: vec![
            Command::new("Vulkleur", Icon::Grid, Action::PdfFormatFill(format.fill))
                .control(RibbonControl::ColorSelect { options: colors(Action::PdfFormatFill), selected: format.fill,
                    current: format.fill_color, width: 126.0 }),
            Command::new("Lijnkleur", Icon::Grid, Action::PdfFormatStroke(format.stroke))
                .control(RibbonControl::ColorSelect { options: colors(Action::PdfFormatStroke), selected: format.stroke,
                    current: format.stroke_color, width: 126.0 }),
        ] },
        RibbonGroup { label: "Lijn & dekking".into(), commands: vec![
            Command::new("Breedte", Icon::Measure, Action::PdfFormatLineWidth(format.line_width.clone()))
                .control(RibbonControl::Number { value: format.line_width.clone(), on_change: Action::PdfFormatLineWidth,
                    width: 90.0, show_label: true }),
            pick("Rand", &["Doorgetrokken", "Gestreept", "Gestippeld"], format.border, Action::PdfFormatBorder, 114.0),
            pick("Mengen", &["Normaal", "Vermenigvuldigen"], format.blend, Action::PdfFormatBlend, 125.0),
            Command::new("Dekking", Icon::Settings, Action::PdfFormatOpacity(format.opacity))
                .control(RibbonControl::Slider { minimum: 0.0, maximum: 100.0, value: format.opacity,
                    step: 1.0, unit: "%", on_change: Action::PdfFormatOpacity }),
        ] },
        RibbonGroup { label: "Pijlen".into(), commands: vec![
            pick("Begin", &arrows, format.arrow_start, Action::PdfFormatArrowStart, 120.0),
            pick("Einde", &arrows, format.arrow_end, Action::PdfFormatArrowEnd, 120.0),
        ] },
        RibbonGroup { label: "Gereedschap".into(), commands: vec![
            preview("style-tools", "Stijlhulpmiddelen", pdf_format_icon!("styleToolsIcon")),
            preview("reset-location", "Locatie herstellen", pdf_format_icon!("resetLocationIcon")),
        ] },
        RibbonGroup { label: "Eigenschappen".into(), commands: vec![
            preview("open-properties", "Openen", pdf_format_icon!("openPropertiesIcon")),
            preview("hide-annotation", "Verbergen", pdf_format_icon!("hideAnnotationIcon")),
            pick("Laag", &["Geen"], format.layer, Action::PdfFormatLayer, 100.0),
        ] },
    ]);
    groups
}

/// The current native Pointcloud branch has one Start ribbon with ten panels.
fn pointcloud_groups(studio: &StudioLayout, tab: &str, selected: Option<&str>) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "pointcloud" || tab != "Start" { return None; }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = vec![
        ("Bestand", vec![("Openen", Open.into()), ("Scanmap openen", planner_source_icon!("FolderOpen"))]),
        ("Navigatie", vec![("Alles passend", Fit.into()), ("Inzoomen", planner_source_icon!("ZoomIn")), ("Uitzoomen", planner_source_icon!("ZoomOut")), ("Selectie passend", Fit.into()), ("Pannen", planner_source_icon!("MoveHorizontal"))]),
        ("Selectie", vec![("Punt kiezen", Search.into()), ("Kaderselectie", Grid.into()), ("Selectie wissen", Close.into()), ("Punten verwijderen", planner_source_icon!("Trash2")), ("Selectie exporteren", Export.into())]),
        ("Snedebox", vec![("Snedebox", planner_source_icon!("Square")), ("Passend op selectie", Fit.into()), ("Box resetten", planner_source_icon!("RotateCcw"))]),
        ("Oppervlak", vec![("Mesh", planner_source_icon!("Boxes")), ("Gesloten mesh", Cube.into()), ("Terrein", planner_source_icon!("Map")), ("Vlakken", Grid.into())]),
        ("Tekening", vec![("Mesh naar plan", planner_source_icon!("FileText")), ("Doorsnedetekening", planner_source_icon!("FileText")), ("Blad", planner_source_icon!("FileText"))]),
        ("Meten", vec![("Afstand", Measure.into()), ("Oppervlakte", Measure.into())]),
        ("Annotatie", vec![("Notitie", planner_source_icon!("FileText")), ("Lijn tekenen", planner_source_icon!("Pen"))]),
        ("Index", vec![("Index bouwen", planner_source_icon!("DatabaseBackup")), ("LOD verversen", planner_source_icon!("RefreshCw"))]),
        ("Export", vec![("Puntenwolk exporteren", Export.into())]),
    ];
    Some(spec.into_iter().map(|(label, items)| RibbonGroup { label: label.into(), commands: items.into_iter().map(|(name, icon)| {
        let id = format!("pointcloud:{tab}:{name}");
        Command::new(name, icon, Action::SelectPreviewCommand(id.clone())).selected(selected == Some(id.as_str()))
    }).collect() }).collect())
}

/// Current core module registry and ribbon group titles in OpenCADStudio.
/// Commands below are a compact review sample; plugins can add more tabs.
fn cad_groups(studio: &StudioLayout, tab: &str, selected: Option<&str>) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "cad" { return None; }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Tekenen" => vec![
            ("Draw", vec![("Line", planner_source_icon!("Pen")), ("Polyline", planner_source_icon!("GitBranch")), ("Circle", planner_source_icon!("Circle")), ("Arc", planner_source_icon!("Compass"))]),
            ("Modify", vec![("Move", planner_source_icon!("MoveHorizontal")), ("Copy", planner_source_icon!("Copy")), ("Rotate", planner_source_icon!("RotateCw"))]),
            ("Annotation", vec![("Text", planner_source_icon!("FileText")), ("Dimension", Measure.into())]),
            ("Layers", vec![("Layers", planner_source_icon!("Layers"))]),
            ("Block", vec![("Create Block", Cube.into()), ("Insert Block", Import.into())]),
            ("Properties", vec![("Match Properties", planner_source_icon!("Pencil"))]),
            ("Groups", vec![("Group", planner_source_icon!("Boxes")), ("Ungroup", planner_source_icon!("Boxes"))]),
            ("Clipboard", vec![("Paste", planner_source_icon!("ClipboardCheck"))]),
            ("Measure", vec![("Measure", Measure.into())]),
        ],
        "Parametrisch" => vec![("Geometric", vec![("Constraints", planner_source_icon!("GitBranch"))]), ("Dimensional", vec![("Linear", Measure.into())]), ("Manage", vec![("Parameters", Settings.into())])],
        "Model" => vec![("Create", vec![("Box", Cube.into())]), ("Boolean", vec![("Union", planner_source_icon!("Boxes"))]), ("Edges", vec![("Fillet Edge", planner_source_icon!("RotateCw"))])],
        "Invoegen" => vec![("Reference", vec![("Attach Underlay", Import.into())]), ("Block", vec![("Insert Block", Import.into())]), ("Block Definition", vec![("Create Block", Cube.into())]), ("Import", vec![("Import", Import.into())]), ("Content", vec![("Content", Open.into())])],
        "Annoteren" => vec![("Text", vec![("Multiline Text", planner_source_icon!("FileText"))]), ("Dimensions", vec![("Dimension", Measure.into())]), ("Centerlines", vec![("Centerline", planner_source_icon!("Minus"))]), ("Leaders", vec![("Multileader", planner_source_icon!("GitBranch"))]), ("Tables", vec![("Table", Grid.into())]), ("Markup", vec![("Revision Cloud", planner_source_icon!("Circle"))]), ("Annotation Scaling", vec![("Add Current Scale", Fit.into())])],
        "Beeld" => vec![("Viewport Tools", vec![("Viewport", Grid.into())]), ("Navigate", vec![("Zoom", Search.into())]), ("Model Viewports", vec![("Model Viewport", Grid.into())]), ("Preset", vec![("Views", Cube.into())]), ("Palettes", vec![("Properties", PanelLeft.into())]), ("Interface", vec![("File Tabs", PanelLeft.into())]), ("Plot", vec![("Page Setup", Settings.into())])],
        "Beheren" => vec![("Customization", vec![("Tool Palettes", Grid.into())]), ("Cleanup", vec![("Purge", planner_source_icon!("Eraser"))]), ("Application", vec![("Options", Settings.into())])],
        _ => return None,
    };
    Some(spec.into_iter().map(|(label, items)| RibbonGroup { label: label.into(), commands: items.into_iter().map(|(name, icon)| {
        let id = format!("cad:{tab}:{name}");
        Command::new(name, icon, Action::SelectPreviewCommand(id.clone())).selected(selected == Some(id.as_str()))
    }).collect() }).collect())
}

/// AEC extension at fd22965ed28a: two added tabs and two buttons in host IFC.
/// The inaccessible host's other tabs and chrome are intentionally absent.
fn extension_2d_groups(studio: &StudioLayout, tab: &str, selected: Option<&str>) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "2d" { return None; }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "AEC" => vec![
            ("Elements", vec![("IfcBeam", planner_source_icon!("Columns3")), ("IfcWall", planner_source_icon!("Square")), ("IfcSlab", planner_source_icon!("LayoutGrid")), ("IfcPile", planner_source_icon!("Compass")), ("IfcColumn", planner_source_icon!("Columns3")), ("CPT", planner_source_icon!("Activity")), ("IfcSpace", planner_source_icon!("Square"))]),
            ("Annotations", vec![("Slab Label", planner_source_icon!("FileText")), ("IfcGrid", Grid.into()), ("2DLevel", Measure.into()), ("Section/Detail", planner_source_icon!("FileText"))]),
            ("Connections", vec![("Join", planner_source_icon!("GitBranch"))]),
            ("Reference", vec![("PDF Underlay", Import.into())]),
            ("Properties", vec![("Materials", Settings.into()), ("IfcTypes", Settings.into()), ("Wall Systems", Settings.into()), ("Project", Open.into())]),
        ],
        "Pile Plan" => vec![
            ("Place", vec![("IfcPile", planner_source_icon!("Compass")), ("CPT", planner_source_icon!("Activity")), ("Puntniveau", Measure.into()), ("Pile Symbols", planner_source_icon!("Map"))]),
            ("CPT Data", vec![("Parse CPT", Import.into())]),
        ],
        "IFC" => vec![("IFCX · in host-IFC", vec![("Export IFCX", Export.into()), ("Copy IFCX", planner_source_icon!("Copy"))])],
        _ => return None,
    };
    Some(spec.into_iter().map(|(label, items)| RibbonGroup { label: label.into(), commands: items.into_iter().map(|(name, icon)| {
        let id = format!("2d:{tab}:{name}");
        Command::new(name, icon, Action::SelectPreviewCommand(id.clone())).selected(selected == Some(id.as_str()))
    }).collect() }).collect())
}

/// Open Frame Studio shell ribbon at eb77f9e4c5d3, including source selects.
fn frame_groups(studio: &StudioLayout, tab: &str, selected: Option<&str>, frame: FrameViewState) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "frame" { return None; }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Home" => vec![
            ("Sjabloon", vec![("Opslaan als sjabloon", Save.into()), ("Sjabloon verwijderen", Close.into())]),
            ("Nieuw kozijn", vec![("Leeg", New.into()), ("Draaikiep", planner_source_icon!("Square")), ("Dubbel", planner_source_icon!("LayoutGrid")), ("Schuifpui", planner_source_icon!("Square")), ("Voordeur", planner_source_icon!("Square"))]),
            ("Bewerken", vec![("Kolom toevoegen", planner_source_icon!("Columns3")), ("Rij toevoegen", planner_source_icon!("LayoutGrid")), ("Dupliceren", planner_source_icon!("Copy")), ("Verwijderen", planner_source_icon!("Trash2"))]),
            ("Importeren", vec![("Nieuw profiel", New.into()), ("Profiel DXF", Import.into()), ("Catalogus", Open.into())]),
        ],
        "Invoegen" => vec![
            ("Onderverdeling", vec![("Kolom", planner_source_icon!("Columns3")), ("Rij", planner_source_icon!("LayoutGrid"))]),
            ("Paneel type", vec![("Vast glas", planner_source_icon!("Square")), ("Draaikiep", planner_source_icon!("Square")), ("Paneel", planner_source_icon!("Square"))]),
            ("Vliesgevel", vec![("Leeg", New.into()), ("Stijl-regel", Grid.into()), ("Element", Cube.into())]),
        ],
        "IFC / Export" => vec![
            ("Kozijn exporteren", vec![("IFC", Export.into()), ("DXF", Export.into())]),
            ("IFC Import", vec![("IFC Import", Import.into()), ("IFC Roundtrip", planner_source_icon!("GitCompareArrows")), ("IFC vergelijken", planner_source_icon!("GitCompareArrows"))]),
            ("Validatie", vec![("IDS Validatie", Check.into()), ("Certificering", Check.into())]),
            ("Project exporteren", vec![("Kozijnstaat PDF", Export.into()), ("Kozijnstaat Excel", Export.into())]),
            ("Werkplaats", vec![("Tekening PDF", Export.into())]),
            ("3D Export", vec![("glTF/GLB", Export.into())]),
            ("Blender / Bonsai", vec![("Naar Blender", Export.into()), ("Verbinding testen", Check.into())]),
        ],
        "Productie" => vec![
            ("Productiestaten exporteren", vec![("PDF", Export.into()), ("Excel", Export.into()), ("CSV", Export.into())]),
            ("CNC / Labels", vec![("CNC G-code", Export.into()), ("Labels PDF", Export.into())]),
            ("Planning / Optimalisatie", vec![("Zaagplan", planner_source_icon!("BarChart3")), ("Planning", planner_source_icon!("CalendarDays")), ("CNC", Export.into()), ("Inkoop", Open.into())]),
        ],
        "Beeld" => vec![
            ("Ongedaan maken", vec![("Ongedaan", Undo.into()), ("Opnieuw", Redo.into())]),
            ("Zoom", vec![("Inzoomen", planner_source_icon!("ZoomIn")), ("Uitzoomen", planner_source_icon!("ZoomOut"))]),
            ("Thema", vec![]),
        ],
        _ => return None,
    };
    let mut groups: Vec<RibbonGroup<Action>> = spec.into_iter().map(|(label, items)| RibbonGroup { label: label.into(), commands: items.into_iter().map(|(name, icon)| {
        let id = format!("frame:{tab}:{name}");
        Command::new(name, icon, Action::SelectPreviewCommand(id.clone())).selected(selected == Some(id.as_str()))
    }).collect() }).collect();
    match tab {
        "Home" => {
            let templates = ["Standaard 67mm Meranti", "Standaard 67mm Accoya", "Zwaar 78mm Meranti", "Passief 90mm Meranti",
                "Kunststof 82mm VEKA Softline", "Kunststof 88mm Kömmerling", "Aluminium 77mm Reynaers CS 77", "Aluminium 75mm Schüco AWS 75.SI+"];
            groups[0].commands.insert(0, Command::new("Sjabloon kiezen", Grid, Action::FrameTemplate(frame.template))
                .control(RibbonControl::Select { options: templates.iter().enumerate().map(|(index, name)| ((*name).into(), Action::FrameTemplate(index))).collect(),
                    selected: frame.template, width: 192.0, show_label: false }));
        }
        "IFC / Export" => {
            groups[0].commands.push(Command::new("IFC LOD", Export, Action::FrameLod(frame.lod))
                .control(RibbonControl::Select { options: ["LOD 200", "LOD 300", "LOD 400"].iter().enumerate()
                    .map(|(index, name)| ((*name).into(), Action::FrameLod(index))).collect(), selected: frame.lod, width: 112.0, show_label: false }));
        }
        "Beeld" => {
            groups[2].commands.push(Command::new("Thema kiezen", Settings, Action::FrameTheme(frame.theme))
                .control(RibbonControl::Select { options: ["Standaard", "Licht", "Donker", "Blauw", "Amber Navy", "Warm Ember", "Hoog contrast"]
                    .iter().enumerate().map(|(index, name)| ((*name).into(), Action::FrameTheme(index))).collect(),
                    selected: frame.theme, width: 192.0, show_label: false }));
        }
        _ => {}
    }
    Some(groups)
}

/// Pile Plan ribbon on ffe979d3b859, including its live view controls.
fn pile_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
    pile: PileViewState,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "pile" {
        return None;
    }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Plan" => vec![
            ("Project", vec![("Projectinformatie", planner_source_icon!("FolderOpen"))]),
            ("Inspecteren", vec![("Belastinglocaties", planner_source_icon!("Map")), ("Sonderingen", planner_source_icon!("Compass"))]),
            ("Selecteren", vec![("Kaderselectie", planner_source_icon!("Square"))]),
            ("Instellingen", vec![("Sonderingsinstellingen", Settings.into()), ("Kosteninstellingen", Settings.into()), ("Groeperingsinstellingen", Settings.into())]),
            ("Vergrendelen", vec![("Locaties vergrendelen", planner_source_icon!("Lock"))]),
            ("Optimalisatie", vec![("Uitvoeren", planner_source_icon!("Play"))]),
        ],
        "Weergave" => vec![
            ("Symbolen", vec![]),
            ("Benutting", vec![]),
            ("Voorgrond", vec![]),
            ("Grid", vec![("Grid tonen", Grid.into())]),
            ("Gebieden", vec![("Puntniveaugebieden tonen", planner_source_icon!("LayoutGrid")), ("Groepen tonen", planner_source_icon!("Boxes"))]),
            ("Vensters", vec![("Verkenner tonen", PanelLeft.into()), ("Eigenschappen tonen", PanelRight.into())]),
        ],
        _ => return None,
    };
    let mut groups: Vec<RibbonGroup<Action>> = spec.into_iter().map(|(label, items)| RibbonGroup {
        label: label.into(),
        commands: items.into_iter().map(|(name, icon)| {
            let id = format!("pile:{tab}:{name}");
            Command::new(name, icon, Action::SelectPreviewCommand(id.clone()))
                .selected(selected == Some(id.as_str()))
        }).collect(),
    }).collect();
    if tab == "Weergave" {
        groups[0].commands.push(Command::new("Symboolgrootte", Icon::Measure, Action::PileSymbolScale(pile.symbol_scale))
            .control(RibbonControl::Slider { minimum: 10.0, maximum: 200.0, value: pile.symbol_scale, step: 1.0, unit: "%", on_change: Action::PileSymbolScale }));
        groups[1].commands.push(Command::new("Gewenst bereik", Icon::Measure, Action::PileUtilizationMinimum(pile.utilization_minimum))
            .control(RibbonControl::Range { minimum: 0.0, maximum: 100.0, lower: pile.utilization_minimum, upper: pile.utilization_maximum, step: 1.0, unit: "%",
                on_lower: Action::PileUtilizationMinimum, on_upper: Action::PileUtilizationMaximum }));
        groups[2].commands.push(Command::new("Voorgrond", Icon::Grid, Action::PileForeground(pile.foreground))
            .control(RibbonControl::Segmented { options: vec![("Belasting-\nlocaties".into(), Action::PileForeground(0)), ("Sonderingen".into(), Action::PileForeground(1))], selected: pile.foreground }));
    }
    Some(groups)
}

/// BIM Validator viewer ribbon on 8f837dd9a56e; disconnected BCF state shown.
fn validator_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "validator" {
        return None;
    }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Start" => vec![
            ("Project", vec![("Opslaan", Save.into()), ("Opslaan als", planner_source_icon!("SaveAll")), ("Openen", Open.into())]),
            ("Modellen", vec![("Toevoegen IFC", Import.into()), ("Verwijder", planner_source_icon!("Trash2"))]),
            ("Validatie", vec![("Valideer", Check.into()), ("IDS Standaard", planner_source_icon!("ListTree")), ("Reset", planner_source_icon!("RotateCcw"))]),
            ("BCF", vec![("Export BCF", Export.into()), ("Sync", planner_source_icon!("RefreshCw")), ("Inloggen", planner_source_icon!("Lock"))]),
        ],
        "Beeld" => vec![
            ("Panelen", vec![("Modellen", PanelLeft.into()), ("Validatie", PanelRight.into())]),
            ("3D Beeld", vec![("Passend", Fit.into()), ("Reset", planner_source_icon!("RotateCcw"))]),
            ("Doorsnede", vec![("Snijvlak X", planner_source_icon!("Columns3")), ("Snijvlak Y", planner_source_icon!("Columns3")), ("Snijvlak Z", planner_source_icon!("Columns3")), ("Wis snijvlakken", planner_source_icon!("Eraser"))]),
        ],
        _ => return None,
    };
    Some(spec.into_iter().map(|(label, items)| RibbonGroup {
        label: label.into(),
        commands: items.into_iter().map(|(name, icon)| {
            let id = format!("validator:{tab}:{name}");
            Command::new(name, icon, Action::SelectPreviewCommand(id.clone()))
                .selected(selected == Some(id.as_str()))
        }).collect(),
    }).collect())
}

/// Reports Studio ribbon at 818e58118c0f: Start, Invoegen and Beeld.
fn reports_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "reports" {
        return None;
    }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Start" => vec![
            ("Klembord", vec![("Plakken", planner_source_icon!("ClipboardCheck")), ("Kopieer sectie", planner_source_icon!("Copy"))]),
            ("Blokken", vec![("Tekst", planner_source_icon!("FileText")), ("Berekening", planner_source_icon!("Hash")), ("Toets", Check.into()), ("Tabel", Grid.into()), ("Spreadsheet", Grid.into()), ("Afbeelding", planner_source_icon!("FilePlus2")), ("Kaart", planner_source_icon!("Map"))]),
            ("Pagina", vec![("Witruimte", planner_source_icon!("Minus")), ("Pagina-einde", planner_source_icon!("FilePlus2"))]),
            ("Controle", vec![("Valideren", Check.into())]),
            ("Uitvoer", vec![("PDF Genereren", Export.into()), ("Download PDF", Export.into())]),
        ],
        "Invoegen" => vec![
            ("Secties", vec![("Nieuw hoofdstuk", New.into()), ("Nieuwe bijlage", New.into())]),
            ("Inhoud", vec![("Tekst", planner_source_icon!("FileText")), ("Berekening", planner_source_icon!("Hash")), ("Toets", Check.into()), ("Tabel", Grid.into()), ("Afbeelding", planner_source_icon!("FilePlus2")), ("Kaart", planner_source_icon!("Map"))]),
        ],
        "Beeld" => vec![
            ("Weergave", vec![("Editor", planner_source_icon!("Pen")), ("Gesplitst", planner_source_icon!("Columns3")), ("JSON", planner_source_icon!("FileCode")), ("Preview", planner_source_icon!("Eye"))]),
            ("Panelen", vec![("Zijpaneel", PanelLeft.into())]),
        ],
        _ => return None,
    };
    Some(spec.into_iter().map(|(label, items)| RibbonGroup {
        label: label.into(),
        commands: items.into_iter().map(|(name, icon)| {
            let id = format!("reports:{tab}:{name}");
            Command::new(name, icon, Action::SelectPreviewCommand(id.clone()))
                .selected(selected == Some(id.as_str()))
        }).collect(),
    }).collect())
}

/// Calculations has only Start and an intentionally empty IFC tab.
fn calculations_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "calculations" {
        return None;
    }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Start" => vec![
            ("Bestand", vec![("Nieuw", New.into()), ("Bladeren…", Open.into()), ("Opslaan", Save.into())]),
            ("Bewerken", vec![("Ongedaan", Undo.into()), ("Opnieuw", Redo.into())]),
            ("Invoegen", vec![("Module", planner_source_icon!("Puzzle")), ("Afbeelding", planner_source_icon!("FilePlus2"))]),
            ("Exporteren", vec![("Voorbeeld", planner_source_icon!("Eye")), ("PDF blad", Export.into()), ("Rapport (PDF)", Export.into())]),
        ],
        "IFC" => vec![],
        _ => return None,
    };
    Some(spec.into_iter().map(|(label, items)| RibbonGroup {
        label: label.into(),
        commands: items.into_iter().map(|(name, icon)| {
            let id = format!("calculations:{tab}:{name}");
            Command::new(name, icon, Action::SelectPreviewCommand(id.clone()))
                .selected(selected == Some(id.as_str()))
        }).collect(),
    }).collect())
}

/// Heatloss uses route-linked tabs; the IFC ribbon is intentionally empty.
fn heatloss_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "heatloss" {
        return None;
    }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Vertrekken" => vec![
            ("Vertrekken", vec![("Nieuw vertrek", New.into())]),
            ("Zones", vec![("Zones beheren", planner_source_icon!("Building2"))]),
            ("Berekening", vec![("Bereken", planner_source_icon!("Play"))]),
        ],
        "Constructies" => vec![("Constructies", vec![("Nieuwe constructie", New.into()), ("Catalogus", planner_source_icon!("BookOpen"))])],
        "Modeller" => vec![
            ("Bewerken", vec![("Ongedaan", Undo.into()), ("Opnieuw", Redo.into()), ("Leeg", planner_source_icon!("Trash2"))]),
            ("Selectie", vec![("Selecteer", planner_source_icon!("CircleDot"))]),
            ("Vormen", vec![("Rechthoek", planner_source_icon!("Square")), ("Polygoon", planner_source_icon!("Diamond")), ("Cirkel", planner_source_icon!("Circle"))]),
            ("Bouwelementen", vec![("Raam", planner_source_icon!("Columns3")), ("Deur", planner_source_icon!("PanelRight"))]),
        ],
        "IFC" => vec![],
        "Resultaten" => vec![("Rapport", vec![("Genereer rapport", planner_source_icon!("FileText"))]), ("Export", vec![("Export JSON", Export.into())])],
        "Rapport" => vec![("Rapport", vec![("Genereren", planner_source_icon!("FileText")), ("Download PDF", Export.into())])],
        _ => return None,
    };
    Some(spec.into_iter().map(|(label, items)| RibbonGroup {
        label: label.into(),
        commands: items.into_iter().map(|(name, icon)| {
            let id = format!("heatloss:{tab}:{name}");
            Command::new(name, icon, Action::SelectPreviewCommand(id.clone()))
                .selected(selected == Some(id.as_str()))
        }).collect(),
    }).collect())
}

/// Source-aligned Geotechniek ribbon samples at 8182b48afc3f. IFC and
/// Berekeningen are dynamic status/list surfaces, represented as placeholders.
fn geotech_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "geotech" {
        return None;
    }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Home" => vec![
            ("Project", vec![("Projectinfo", Settings.into())]),
            ("Weergave", vec![("Zoom -", planner_source_icon!("ZoomOut")), ("Passend", Fit.into())]),
        ],
        "Kaart" => vec![("Kaart", vec![("Meten", Measure.into()), ("Exporteer als afbeelding", Export.into())])],
        "Rapport" => vec![("Output", vec![("Genereer PDF", Export.into()), ("Open PDF", Open.into())])],
        "Situatietekening" => vec![
            ("Selecteer", vec![("Selecteren", planner_source_icon!("CircleDot"))]),
            ("Bewerken", vec![("Verplaatsen", planner_source_icon!("MoveHorizontal")), ("Kopiëren", planner_source_icon!("Copy")), ("Roteren", planner_source_icon!("RotateCw")), ("Verwijderen", planner_source_icon!("Trash2")), ("Trim", planner_source_icon!("Scissors")), ("Mirror", planner_source_icon!("GitCompareArrows"))]),
            ("Plaatsen", vec![("Sondering", planner_source_icon!("Compass")), ("Boring", planner_source_icon!("Compass")), ("Lijn", planner_source_icon!("Minus")), ("Maatlijn", Measure.into()), ("Vlak", planner_source_icon!("Square")), ("Opmerking", planner_source_icon!("Pen"))]),
            ("Overlay", vec![("Image/PDF import", Import.into()), ("Kader (SVG)", planner_source_icon!("Square")), ("Wis alles", planner_source_icon!("Eraser"))]),
            ("Export", vec![("Exporteer DWG", Export.into()), ("Exporteer PDF", Export.into()), ("Print", planner_source_icon!("Printer"))]),
        ],
        "Berekeningen" => vec![("Projectberekeningen", vec![("Dynamische berekeningenlijst", Grid.into())])],
        "IFC" => vec![("Automatisch gegenereerd", vec![("Live IFC4x3 + IFCX", Cube.into())])],
        _ => return None,
    };
    Some(spec.into_iter().map(|(label, items)| RibbonGroup {
        label: label.into(),
        commands: items.into_iter().map(|(name, icon)| {
            let id = format!("geotech:{tab}:{name}");
            Command::new(name, icon, Action::SelectPreviewCommand(id.clone()))
                .selected(selected == Some(id.as_str()))
        }).collect(),
    }).collect())
}

/// Source-aligned command samples from Calc's ribbon components at b47042704efa.
/// Experimental and contextual tab visibility is recorded in app-layouts.json.
fn calc_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "calc" {
        return None;
    }
    use Icon::*;
    let spec: Vec<(&str, Vec<(&str, CommandIcon)>)> = match tab {
        "Begroting" => vec![
            (
                "Regels",
                vec![
                    ("Hoofdstuk", planner_source_icon!("FilePlus2")),
                    ("Begr.post", planner_source_icon!("FileText")),
                    ("Bew.post", planner_source_icon!("ClipboardCheck")),
                    ("Rekenregel", planner_source_icon!("ListOrdered")),
                    ("Tekstregel", planner_source_icon!("FileType")),
                    ("Witregel", planner_source_icon!("ListTree")),
                    ("Verwijder", planner_source_icon!("Trash2")),
                ],
            ),
            (
                "Klembord",
                vec![
                    ("Plakken", planner_source_icon!("ClipboardCheck")),
                    ("Knippen", planner_source_icon!("Scissors")),
                    ("Kopiëren", planner_source_icon!("Copy")),
                ],
            ),
            (
                "Geschiedenis",
                vec![("Ongedaan", Undo.into()), ("Opnieuw", Redo.into())],
            ),
            ("Panelen", vec![("Hoeveelheid", Settings.into())]),
            (
                "Weergave",
                vec![
                    ("UI-1", Grid.into()),
                    ("UI-2", Grid.into()),
                    ("Simple", Grid.into()),
                    ("Inklappen", planner_source_icon!("ChevronsDownUp")),
                ],
            ),
            ("Prijzen", vec![("Prijzen %", Settings.into())]),
            (
                "Wijzigingen",
                vec![
                    ("Bijhouden", planner_source_icon!("ListOrdered")),
                    ("Wis markeringen", planner_source_icon!("Eraser")),
                    ("Hele regel", Grid.into()),
                    ("Alleen cel", Grid.into()),
                ],
            ),
            ("Project", vec![("Projectgegevens", Settings.into())]),
            (
                "Varianten",
                vec![
                    ("Varianten", planner_source_icon!("GitBranch")),
                    ("Optieset", planner_source_icon!("Layers")),
                ],
            ),
        ],
        "Rapportage" => vec![
            (
                "Rapportage",
                vec![
                    ("Opdrachtgever", planner_source_icon!("FileText")),
                    ("Intern", planner_source_icon!("FileText")),
                    ("Nacalculatie", planner_source_icon!("FileText")),
                ],
            ),
            (
                "Weergave",
                vec![
                    ("Hoeveelheden", Grid.into()),
                    ("Staand", planner_source_icon!("FileText")),
                    ("Liggend", planner_source_icon!("FileText")),
                ],
            ),
            (
                "Afdrukken",
                vec![("Afdrukken", planner_source_icon!("Printer"))],
            ),
            (
                "Export",
                vec![
                    ("PDF Export", Export.into()),
                    ("Excel Export", Export.into()),
                    ("IFC Export", Export.into()),
                ],
            ),
        ],
        "Spreadsheet" => vec![
            (
                "Werkbladen",
                vec![
                    ("Nieuw blad", New.into()),
                    ("Verwijder", planner_source_icon!("Trash2")),
                ],
            ),
            (
                "Opmaak",
                vec![
                    ("Vet", planner_source_icon!("FileType")),
                    ("Cursief", planner_source_icon!("FileType")),
                    ("Links", planner_source_icon!("IndentDecrease")),
                    ("Midden", planner_source_icon!("Columns3")),
                    ("Rechts", planner_source_icon!("IndentIncrease")),
                ],
            ),
            (
                "Getal",
                vec![
                    ("Valuta (€)", planner_source_icon!("Gauge")),
                    ("Percentage (%)", planner_source_icon!("Gauge")),
                    ("+Decimaal", planner_source_icon!("Plus")),
                    ("-Decimaal", planner_source_icon!("Minus")),
                ],
            ),
            (
                "Tekstgrootte",
                vec![
                    ("Groter", planner_source_icon!("ZoomIn")),
                    ("Kleiner", planner_source_icon!("ZoomOut")),
                ],
            ),
        ],
        "IFC" => vec![(
            "Rapport",
            vec![("Genereer", planner_source_icon!("FileText"))],
        )],
        "Offerte" => vec![
            (
                "Secties",
                vec![
                    ("Technisch", New.into()),
                    ("Opties", New.into()),
                    ("Vrij", New.into()),
                    ("Meerwerk", New.into()),
                ],
            ),
            (
                "Document",
                vec![
                    ("Gegevens", Settings.into()),
                    ("Termijnen", Settings.into()),
                    ("Garanties", Settings.into()),
                ],
            ),
            ("Export", vec![("PDF offerte", Export.into())]),
        ],
        "Tekstopmaak" => vec![
            (
                "Tekststijl",
                vec![
                    ("Vet", planner_source_icon!("FileType")),
                    ("Cursief", planner_source_icon!("FileType")),
                    ("Onderstr.", planner_source_icon!("FileType")),
                ],
            ),
            (
                "Grootte",
                vec![
                    ("Groter", planner_source_icon!("ZoomIn")),
                    ("Kleiner", planner_source_icon!("ZoomOut")),
                ],
            ),
            (
                "Uitlijning",
                vec![
                    ("Links", planner_source_icon!("IndentDecrease")),
                    ("Midden", planner_source_icon!("Columns3")),
                    ("Rechts", planner_source_icon!("IndentIncrease")),
                ],
            ),
        ],
        "3D" | "PDF" => vec![("Experimenteel", vec![("Nog niet beschikbaar", Help.into())])],
        _ => return None,
    };
    Some(
        spec.into_iter()
            .map(|(label, items)| RibbonGroup {
                label: label.into(),
                commands: items
                    .into_iter()
                    .map(|(name, icon)| {
                        let id = format!("calc:{tab}:{name}");
                        Command::new(name, icon, Action::SelectPreviewCommand(id.clone()))
                            .selected(selected == Some(id.as_str()))
                    })
                    .collect(),
            })
            .collect(),
    )
}

/// The Planner groups follow its source ribbon registry at commit 5a65f6b865a7.
/// Only shared action meanings are canonical; domain vectors remain review assets.
fn planner_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    if studio.id != "planner" {
        return None;
    }
    use Icon::*;
    let file: (&str, &[(&str, CommandIcon)]) = (
        "Bestand",
        &[
            ("Nieuw", New.into()),
            ("Openen", Open.into()),
            ("Opslaan", Save.into()),
            ("Opslaan als", planner_source_icon!("SaveAll")),
            ("Recent", planner_source_icon!("Clock")),
            ("Exporteren", Export.into()),
        ],
    );
    let edit: (&str, &[(&str, CommandIcon)]) = (
        "Bewerken",
        &[
            ("Ongedaan", Undo.into()),
            ("Opnieuw", Redo.into()),
            ("Verwijderen", planner_source_icon!("Trash2")),
        ],
    );
    let tasks: (&str, &[(&str, CommandIcon)]) = (
        "Taken",
        &[
            ("Taak", planner_source_icon!("Plus")),
            ("Mijlpaal", planner_source_icon!("Milestone")),
            ("Relatie", planner_source_icon!("Link")),
            ("Splitsen", planner_source_icon!("Scissors")),
        ],
    );
    let schedule: (&str, &[(&str, CommandIcon)]) =
        ("Planning", &[("Berekenen", planner_source_icon!("Play"))]);
    let progress: (&str, &[(&str, CommandIcon)]) = (
        "Voortgang",
        &[
            ("Voortgang importeren", planner_source_icon!("FileUp")),
            ("Voortgang exporteren", planner_source_icon!("FileDown")),
        ],
    );
    let spec: Vec<(&str, &[(&str, CommandIcon)])> = match tab {
        "Start" => vec![
            file,
            edit,
            tasks,
            schedule,
            (
                "Zoom",
                &[
                    ("Inzoomen", planner_source_icon!("ZoomIn")),
                    ("Uitzoomen", planner_source_icon!("ZoomOut")),
                ],
            ),
        ],
        "Planning" => vec![
            (
                "Planning",
                &[
                    ("Berekenen", planner_source_icon!("Play")),
                    ("Project verplaatsen", planner_source_icon!("CalendarClock")),
                    ("Waarschuwingen", planner_source_icon!("AlertTriangle")),
                ],
            ),
            (
                "Relaties",
                &[
                    ("Relatie", planner_source_icon!("Link")),
                    ("Splitsen", planner_source_icon!("Scissors")),
                ],
            ),
            (
                "Traceren",
                &[
                    ("Voorgangers", planner_source_icon!("MoveHorizontal")),
                    ("Opvolgers", planner_source_icon!("MoveHorizontal")),
                ],
            ),
            (
                "Kalender",
                &[("Kalender", planner_source_icon!("Calendar"))],
            ),
            (
                "Structuur",
                &[
                    ("Codevelden", planner_source_icon!("Tags")),
                    ("WBS automatisch", planner_source_icon!("Hash")),
                    ("WBS hernummeren", planner_source_icon!("ListOrdered")),
                    ("Inspringen", planner_source_icon!("IndentIncrease")),
                    ("Uitspringen", planner_source_icon!("IndentDecrease")),
                ],
            ),
            (
                "Basislijnen",
                &[("Basislijnen", planner_source_icon!("LayoutGrid"))],
            ),
            progress,
        ],
        "Resources" => vec![
            (
                "Resourcebeheer",
                &[
                    ("Resources", planner_source_icon!("Users")),
                    ("Resourcedock", CommandIcon::Canonical(PanelRight)),
                    ("Nieuwe resource", planner_source_icon!("Plus")),
                ],
            ),
            (
                "Toewijzing",
                &[("Toewijzen", planner_source_icon!("Users"))],
            ),
            (
                "Histogram",
                &[("Histogram", planner_source_icon!("BarChart3"))],
            ),
            (
                "Nivelleren",
                &[
                    ("Nivelleren", planner_source_icon!("Scale")),
                    ("Wissen", planner_source_icon!("Eraser")),
                ],
            ),
            (
                "Overbezetting",
                &[("Indicator", planner_source_icon!("AlertTriangle"))],
            ),
        ],
        "Weergave" => vec![
            (
                "Tijdschaal",
                &[("Tijdschaal", planner_source_icon!("CalendarDays"))],
            ),
            (
                "Overzicht",
                &[
                    ("Inklappen", planner_source_icon!("ChevronsDownUp")),
                    ("Uitklappen", planner_source_icon!("ChevronsUpDown")),
                ],
            ),
            ("Layout", &[("Layout", planner_source_icon!("LayoutGrid"))]),
            (
                "Presentatie",
                &[("Presentatie", planner_source_icon!("Eye"))],
            ),
            (
                "Panelen",
                &[
                    ("Eigenschappen", CommandIcon::Canonical(PanelRight)),
                    ("Resources", planner_source_icon!("Users")),
                ],
            ),
            (
                "Overlays",
                &[
                    ("Basislijn", planner_source_icon!("LayoutGrid")),
                    ("Voortgangslijn", planner_source_icon!("TrendingUp")),
                ],
            ),
        ],
        "Instellingen" => vec![
            (
                "Project",
                &[
                    ("Projectinformatie", planner_source_icon!("Info")),
                    ("Projectinstellingen", CommandIcon::Canonical(Settings)),
                ],
            ),
            (
                "Kalender",
                &[("Kalender", planner_source_icon!("Calendar"))],
            ),
            (
                "Sneltoetsen",
                &[("Sneltoetsen", planner_source_icon!("Keyboard"))],
            ),
        ],
        "Tabel" => vec![
            file,
            edit,
            tasks,
            schedule,
            (
                "Traceren",
                &[
                    ("Voorgangers", planner_source_icon!("MoveHorizontal")),
                    ("Opvolgers", planner_source_icon!("MoveHorizontal")),
                ],
            ),
            (
                "Kolommen",
                &[("Kolommen", planner_source_icon!("Columns3"))],
            ),
            progress,
        ],
        "IFC" => vec![("IFC", &[("IFC-informatie", planner_source_icon!("Info"))])],
        "Rapport" => vec![
            (
                "Rapportage",
                &[("Afdrukvoorbeeld", planner_source_icon!("Printer"))],
            ),
            progress,
        ],
        "AI" => vec![
            ("Server", &[("Server", planner_source_icon!("Settings"))]),
            ("Verbinding", &[("Verbinden", planner_source_icon!("Plug"))]),
            (
                "Veiligheid",
                &[("Veiligheid", planner_source_icon!("AlertTriangle"))],
            ),
            (
                "Activiteit",
                &[("Activiteit", planner_source_icon!("Activity"))],
            ),
        ],
        _ => return None,
    };
    Some(
        spec.into_iter()
            .map(|(label, items)| RibbonGroup {
                label: label.into(),
                commands: items
                    .iter()
                    .map(|(name, icon)| {
                        let id = format!("planner:{tab}:{name}");
                        Command::new(*name, *icon, Action::SelectPreviewCommand(id.clone()))
                            .selected(selected == Some(id.as_str()))
                    })
                    .collect(),
            })
            .collect(),
    )
}

fn base_groups(tab: &str, selected: Option<&str>) -> Vec<RibbonGroup<Action>> {
    use Icon::*;
    let spec: &[(&str, &[(&str, Icon)])] = match tab {
        "Start" => &[
            (
                "Project",
                &[("Nieuw", New), ("Openen", Open), ("Opslaan", Save)],
            ),
            (
                "Gegevens",
                &[("Importeren", Import), ("Exporteren", Export)],
            ),
            ("Navigatie", &[("Zoeken", Search), ("Passend", Fit)]),
            (
                "Schermen",
                &[("Weergave", Cube), ("Eigenschappen", PanelRight)],
            ),
        ],
        "Weergave" => &[
            (
                "Navigatie",
                &[("Passend", Fit), ("Weergave", Cube), ("Lagen", PanelLeft)],
            ),
            (
                "Vensters",
                &[("Eigenschappen", PanelRight), ("Instellingen", Settings)],
            ),
        ],
        "Help" => &[(
            "Ondersteuning",
            &[("Help", Help), ("Instellingen", Settings)],
        )],
        _ => &[
            (tab, &[("Nieuw", New), ("Openen", Open), ("Maat", Measure)]),
            (
                "Bewerken",
                &[("Zoeken", Search), ("Eigenschappen", PanelRight)],
            ),
            ("Uitvoer", &[("Exporteren", Export), ("Passend", Fit)]),
        ],
    };
    spec.iter()
        .map(|(label, items)| RibbonGroup {
            label: (*label).into(),
            commands: items
                .iter()
                .map(|(name, icon)| {
                    let id = format!("{tab}:{name}");
                    Command::new(*name, *icon, Action::SelectPreviewCommand(id.clone()))
                        .selected(selected == Some(id.as_str()))
                })
                .collect(),
        })
        .collect()
}

fn domain_groups(
    studio: &StudioLayout,
    tab: &str,
    selected: Option<&str>,
) -> Option<Vec<RibbonGroup<Action>>> {
    let wanted: &[&str] = match (studio.id.as_str(), tab) {
        ("fem", "Geometrie") => &["Geometrie"],
        ("fem", "Randvoorwaarden") => &["Randvoorwaarden"],
        ("fem", "Belastingen") => &["Belastingen"],
        ("fem", "Net" | "Berekenen") => &["Net & berekening"],
        ("fem", "Resultaten") => &["Resultaten"],
        ("bim", "Modelleren") => &[
            "Project & referenties",
            "Bouwdelen",
            "Bewerken & informatie",
        ],
        ("bim", "Documenteren" | "Coördineren") => &["Documentatie & coördinatie"],
        _ => return None,
    };
    let mut groups: Vec<RibbonGroup<Action>> = Vec::new();
    for proposal in proposals()
        .iter()
        .filter(|item| item.domain == studio.id && wanted.contains(&item.group.as_str()))
    {
        let short = proposal.id.rsplit('.').next().unwrap_or_default();
        if studio.id == "fem"
            && tab == "Net"
            && !["mesh", "mesh-refine", "mesh-quality"].contains(&short)
        {
            continue;
        }
        if studio.id == "fem"
            && tab == "Berekenen"
            && ["mesh", "mesh-refine", "mesh-quality"].contains(&short)
        {
            continue;
        }
        let coordination = [
            "clash",
            "clearance",
            "bcf-issue",
            "ids-check",
            "ifc-export",
            "revision",
            "section-box",
        ]
        .contains(&short);
        if studio.id == "bim"
            && ((tab == "Documenteren" && coordination) || (tab == "Coördineren" && !coordination))
        {
            continue;
        }
        let bytes = domain_drafts::ALL
            .iter()
            .find(|(id, _)| *id == proposal.id)
            .expect("every proposal has a review SVG")
            .1;
        let command = Command::new(
            proposal.label.clone(),
            CommandIcon::Svg(bytes),
            Action::SelectPreviewCommand(proposal.id.clone()),
        )
        .selected(selected == Some(proposal.id.as_str()));
        match groups
            .iter_mut()
            .find(|group| group.label == proposal.group)
        {
            Some(group) => group.commands.push(command),
            None => groups.push(RibbonGroup {
                label: proposal.group.clone(),
                commands: vec![command],
            }),
        }
    }
    Some(groups)
}
