use crate::model::*;
use std::collections::HashSet;

/// Commands die elke app via de vaste schil heeft en dus in quick access mogen staan.
pub const STANDARD_COMMANDS: &[&str] = &[
    "file.new", "file.open", "file.save", "file.save-as", "file.print", "edit.undo", "edit.redo",
];

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Issue {
    pub path: String,
    pub message: String,
}

/// Labels van de app zelf (alles wat niet met `openaec.` begint), per taal als puntsleutels.
#[derive(Debug, Default)]
pub struct AppLabels {
    pub nl: HashSet<String>,
    pub en: HashSet<String>,
}

impl AppLabels {
    pub fn from_json(nl: &str, en: &str) -> Result<Self, String> {
        Ok(Self { nl: flatten_json(nl)?, en: flatten_json(en)? })
    }
}

fn flatten_json(src: &str) -> Result<HashSet<String>, String> {
    let value: serde_json::Value = serde_json::from_str(src).map_err(|e| e.to_string())?;
    let mut out = HashSet::new();
    fn walk(v: &serde_json::Value, prefix: &str, out: &mut HashSet<String>) {
        match v {
            serde_json::Value::Object(map) => {
                for (k, vv) in map {
                    let key = if prefix.is_empty() { k.clone() } else { format!("{prefix}.{k}") };
                    walk(vv, &key, out);
                }
            }
            _ => {
                out.insert(prefix.to_string());
            }
        }
    }
    walk(&value, "", &mut out);
    Ok(out)
}

struct Checker<'a> {
    issues: Vec<Issue>,
    labels: Option<&'a AppLabels>,
    commands: HashSet<String>,
}

fn is_id(s: &str) -> bool {
    let mut chars = s.chars();
    matches!(chars.next(), Some('a'..='z')) && chars.all(|c| c.is_ascii_lowercase() || c.is_ascii_digit() || c == '-')
}

fn is_command(s: &str) -> bool {
    let parts: Vec<&str> = s.split('.').collect();
    parts.len() >= 2 && is_id(parts[0]) && parts[1..].iter().all(|p| !p.is_empty() && p.chars().all(|c| c.is_ascii_lowercase() || c.is_ascii_digit() || c == '-'))
}

impl<'a> Checker<'a> {
    fn err(&mut self, path: &str, message: impl Into<String>) {
        self.issues.push(Issue { path: path.to_string(), message: message.into() });
    }

    fn label(&mut self, path: &str, key: &str) {
        if let Some(shared) = key.strip_prefix("openaec.") {
            if !openaec_i18n::has_key(shared) {
                self.err(path, format!("onbekende gedeelde term {key}"));
            }
            return;
        }
        if let Some(labels) = self.labels {
            if !labels.nl.contains(key) { self.err(path, format!("label {key} ontbreekt in nl")); }
            if !labels.en.contains(key) { self.err(path, format!("label {key} ontbreekt in en")); }
        }
    }

    fn icon(&mut self, path: &str, id: &str) {
        if openaec_icons::Icon::from_id(id).is_none() {
            self.err(path, format!("onbekend icoon {id}"));
        }
    }

    fn command(&mut self, path: &str, cmd: &str) {
        if !is_command(cmd) { self.err(path, format!("ongeldige command-naam {cmd}")); }
        self.commands.insert(cmd.to_string());
    }

    fn item(&mut self, path: &str, item: &Item) {
        use ItemKind::*;
        // (command, icon, label, items, slot): Some(true)=verplicht, Some(false)=verboden, None=optioneel
        let rule: [Option<bool>; 5] = match item.kind {
            Large | Small | Toggle => [Some(true), Some(true), Some(true), Some(false), Some(false)],
            Dropdown => [Some(false), None, Some(true), Some(true), Some(false)],
            LargeDropdown => [Some(false), Some(true), Some(true), Some(true), Some(false)],
            Split => [Some(true), Some(true), Some(true), Some(true), Some(false)],
            Combo => [Some(true), None, Some(true), Some(false), Some(false)],
            Custom => [Some(false), Some(false), Some(false), Some(false), Some(true)],
        };
        let kind = match item.kind {
            Large => "large", Small => "small", Toggle => "toggle", Dropdown => "dropdown",
            LargeDropdown => "large-dropdown", Split => "split", Combo => "combo", Custom => "custom",
        };
        let present = [item.command.is_some(), item.icon.is_some(), item.label.is_some(), !item.items.is_empty(), item.slot.is_some()];
        for (i, name) in ["command", "icon", "label", "items", "slot"].iter().enumerate() {
            match (rule[i], present[i]) {
                (Some(true), false) => self.err(path, format!("{kind}: {name} is verplicht")),
                (Some(false), true) => self.err(path, format!("{kind}: {name} is niet toegestaan")),
                _ => {}
            }
        }
        if item.kind == Custom {
            if item.tooltip.is_some() { self.err(path, format!("{kind}: tooltip is niet toegestaan")); }
            if item.shortcut.is_some() { self.err(path, format!("{kind}: shortcut is niet toegestaan")); }
        }
        if let Some(c) = &item.command { self.command(path, c); }
        if let Some(i) = &item.icon { self.icon(path, i); }
        if let Some(l) = &item.label { self.label(path, l); }
        if let Some(t) = &item.tooltip { self.label(path, t); }
        for (n, e) in item.items.iter().enumerate() {
            let p = format!("{path}.items[{n}]");
            self.command(&p, &e.command);
            if let Some(i) = &e.icon { self.icon(&p, i); }
            self.label(&p, &e.label);
        }
    }

    fn tabs(&mut self, prefix: &str, tabs: &[Tab], seen_tabs: &mut HashSet<String>) {
        for tab in tabs {
            let tp = format!("{prefix}tab[{}]", tab.id);
            if !is_id(&tab.id) { self.err(&tp, format!("ongeldig tab-id {}", tab.id)); }
            if !seen_tabs.insert(tab.id.clone()) { self.err(&tp, format!("dubbele tab-id {}", tab.id)); }
            self.label(&tp, &tab.label);
            let mut seen_groups = HashSet::new();
            for group in &tab.groups {
                let gp = format!("{tp}.group[{}]", group.id);
                if !is_id(&group.id) { self.err(&gp, format!("ongeldig groep-id {}", group.id)); }
                if !seen_groups.insert(group.id.clone()) { self.err(&gp, format!("dubbele groep-id {}", group.id)); }
                self.label(&gp, &group.label);
                for (n, item) in group.items.iter().enumerate() {
                    self.item(&format!("{gp}.items[{n}]"), item);
                }
            }
        }
    }
}

pub fn validate_ribbon(file: &RibbonFile, labels: Option<&AppLabels>) -> Vec<Issue> {
    let mut c = Checker { issues: vec![], labels, commands: HashSet::new() };
    if file.format != 1 { c.err("format", format!("onbekend formaat {}", file.format)); }
    if !is_id(&file.app) { c.err("app", format!("ongeldige app-id {}", file.app)); }
    let mut seen_tabs = HashSet::new();
    for inc in &file.include {
        match inc.strip_prefix("openaec:").and_then(crate::shared_tab_source) {
            Some(src) => match crate::parse_shared(src) {
                Ok(shared) => c.tabs(&format!("include[{inc}]."), &shared.tabs, &mut seen_tabs),
                Err(e) => c.err("include", format!("{inc}: {e}")),
            },
            None => c.err("include", format!("onbekende gedeelde tab {inc}")),
        }
    }
    c.tabs("", &file.tabs, &mut seen_tabs);
    if let Some(qa) = &file.quick_access {
        for cmd in &qa.items {
            if !c.commands.contains(cmd) && !STANDARD_COMMANDS.contains(&cmd.as_str()) {
                c.err("quick_access", format!("command {cmd} staat niet in de ribbon en is geen standaard-command"));
            }
        }
    }
    c.issues
}

pub fn validate_shared(file: &SharedTabFile) -> Vec<Issue> {
    let mut c = Checker { issues: vec![], labels: None, commands: HashSet::new() };
    if file.format != 1 { c.err("format", format!("onbekend formaat {}", file.format)); }
    if !is_id(&file.shared) { c.err("shared", format!("ongeldige naam voor gedeelde tab {}", file.shared)); }
    for tab in &file.tabs {
        let all_shared = std::iter::once(&tab.label)
            .chain(tab.groups.iter().map(|g| &g.label))
            .chain(tab.groups.iter().flat_map(|g| g.items.iter().flat_map(|i| {
                i.label.iter().chain(i.tooltip.iter()).chain(i.items.iter().map(|e| &e.label))
            })))
            .all(|l| l.starts_with("openaec."));
        if !all_shared { c.err(&format!("tab[{}]", tab.id), "gedeelde tabs gebruiken alleen openaec.*-labels"); }
    }
    c.tabs("", &file.tabs, &mut HashSet::new());
    c.issues
}
