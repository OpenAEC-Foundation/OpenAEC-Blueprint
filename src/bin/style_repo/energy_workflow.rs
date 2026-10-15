//! Review data from Open Energy Studio at e9a485db4ac695ff502a48cd2ded50dec5b5a1a6.
//! Main navigation: src/components/shell/WorkflowNav.tsx.
//! New-build questions: src/core/navigation/buildFlow.ts.
//! Existing-building questions: src/core/survey/surveyFlow.ts.
//! These are layout labels, not Energy calculations or form implementations.

use openaec_ui::Language;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EnergyMode {
    NewBuildResidential,
    NewBuildUtility,
    ExistingResidential,
    ExistingUtility,
}

impl EnergyMode {
    pub const ALL: [Self; 4] = [
        Self::NewBuildResidential,
        Self::NewBuildUtility,
        Self::ExistingResidential,
        Self::ExistingUtility,
    ];

    pub fn label(self, language: Language) -> &'static str {
        match self {
            Self::NewBuildResidential => language.text("Nieuwbouw · woning", "New build · residential"),
            Self::NewBuildUtility => language.text("Nieuwbouw · utiliteit", "New build · utility"),
            Self::ExistingResidential => language.text("Bestaande bouw · woning", "Existing · residential"),
            Self::ExistingUtility => language.text("Bestaande bouw · utiliteit", "Existing · utility"),
        }
    }

    pub fn existing(self) -> bool {
        matches!(self, Self::ExistingResidential | Self::ExistingUtility)
    }

    pub fn utility(self) -> bool {
        matches!(self, Self::NewBuildUtility | Self::ExistingUtility)
    }

    pub fn steps(self, language: Language) -> Vec<EnergyStep> {
        let l = language;
        if self.existing() {
            let mut survey = if self.utility() {
                vec![l.text("Gebouw", "Building"), l.text("Rekenzones", "Calculation zones")]
            } else {
                vec![l.text("Woning", "Dwelling")]
            };
            survey.extend([
                l.text("Gevels", "Walls"),
                l.text("Dak en vloer", "Roof and floor"),
                l.text("Verwarming", "Heating"),
                l.text("Warm water", "Hot water"),
                l.text("Ventilatie", "Ventilation"),
                l.text("Koeling", "Cooling"),
                l.text("Zonnepanelen", "Solar panels"),
            ]);
            return vec![
                EnergyStep::new(l.text("Opname", "Survey"), survey),
                EnergyStep::new(l.text("Controle", "Check"), vec![]),
                EnergyStep::new(l.text("Label en rapport", "Label and report"), vec![]),
                EnergyStep::new(l.text("Maatwerkadvies", "Tailored advice"), vec![]),
                EnergyStep::new(l.text("Registratie", "Registration"), vec![]),
                EnergyStep::more(l.text("Herlabelen", "Relabel")),
            ];
        }
        let building = vec![
            l.text("Schil", "Envelope"),
            l.text("Rekenzones", "Calculation zones"),
            l.text("Constructies", "Constructions"),
            l.text("Koudebruggen", "Thermal bridges"),
            l.text("Luchtdichtheid", "Air tightness"),
            l.text("Onverwarmde ruimten", "Unheated spaces"),
        ];
        let mut installations = vec![
            l.text("Verwarming", "Heating"),
            l.text("Warm water", "Hot water"),
            l.text("Ventilatie", "Ventilation"),
            l.text("Koeling", "Cooling"),
        ];
        if self.utility() {
            installations.extend([
                l.text("Bevochtiging", "Humidification"),
                l.text("Verlichting", "Lighting"),
            ]);
        }
        installations.push(l.text("Opwekking", "Generation"));
        if self.utility() {
            installations.push("BACS");
        }
        vec![
            EnergyStep::new(l.text("Project", "Project"), vec![]),
            EnergyStep::new(l.text("Gebouw", "Building"), building),
            EnergyStep::new(l.text("Installaties", "Installations"), installations),
            EnergyStep::new(l.text("Controle", "Check"), vec![]),
            EnergyStep::new(l.text("Resultaten en rapport", "Results and report"),
                            vec![l.text("Resultaten", "Results"), l.text("Rapport", "Report")]),
            EnergyStep::new(l.text("Registratie", "Registration"), vec![]),
        ]
    }
}

pub struct EnergyStep {
    pub label: &'static str,
    pub subs: Vec<&'static str>,
    pub more: bool,
}

impl EnergyStep {
    fn new(label: &'static str, subs: Vec<&'static str>) -> Self {
        Self { label, subs, more: false }
    }
    fn more(label: &'static str) -> Self {
        Self { label, subs: vec![], more: true }
    }
}
