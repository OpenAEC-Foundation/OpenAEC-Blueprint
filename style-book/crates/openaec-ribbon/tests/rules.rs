use openaec_ribbon::*;

fn fixture(name: &str) -> String {
    std::fs::read_to_string(format!("{}/tests/fixtures/{name}", env!("CARGO_MANIFEST_DIR"))).unwrap()
}

fn messages(issues: Vec<Issue>) -> Vec<String> {
    issues.into_iter().map(|i| format!("{}: {}", i.path, i.message)).collect()
}

/// Ribbon met precies een groep en de opgegeven items (inline-tabel-bron), zonder app-labels.
fn ribbon_with(items: &str) -> String {
    format!(
        "app = \"t\"\nformat = 1\n\n[[tab]]\nid = \"home\"\nlabel = \"openaec.action.paste\"\n\n  [[tab.group]]\n  id = \"g\"\n  label = \"openaec.action.paste\"\n  items = [ {items} ]\n"
    )
}

fn check(src: &str) -> Vec<String> {
    messages(validate_ribbon(&parse_ribbon(src).expect("parse"), None))
}

fn field(name: &str) -> String {
    match name {
        "command" => "command = \"a.b\"",
        "icon" => "icon = \"edit/paste\"",
        "label" => "label = \"openaec.action.paste\"",
        "items" => "items = [ { command = \"a.c\", label = \"openaec.action.copy\" } ]",
        "slot" => "slot = \"s\"",
        other => panic!("onbekend veld {other}"),
    }
    .to_string()
}

fn item(kind: &str, fields: &[&str]) -> String {
    let mut parts = vec![format!("type = \"{kind}\"")];
    parts.extend(fields.iter().map(|f| field(f)));
    format!("{{ {} }}", parts.join(", "))
}

const ALL: [&str; 5] = ["command", "icon", "label", "items", "slot"];

/// (type, verplicht, verboden); alle overige velden zijn optioneel.
const RULES: &[(&str, &[&str], &[&str])] = &[
    ("large", &["command", "icon", "label"], &["items", "slot"]),
    ("small", &["command", "icon", "label"], &["items", "slot"]),
    ("toggle", &["command", "icon", "label"], &["items", "slot"]),
    ("dropdown", &["label", "items"], &["command", "slot"]),
    ("large-dropdown", &["icon", "label", "items"], &["command", "slot"]),
    ("split", &["command", "icon", "label", "items"], &["slot"]),
    ("combo", &["command", "label"], &["items", "slot"]),
    ("custom", &["slot"], &["command", "icon", "label", "items"]),
];

#[test]
fn regeltabel_dekt_elk_itemtype() {
    for (kind, required, forbidden) in RULES {
        // Minimaal geldig item.
        let found = check(&ribbon_with(&item(kind, required)));
        assert!(found.is_empty(), "{kind}: minimaal item moet geldig zijn: {found:?}");

        // Elk verplicht veld weglaten.
        for missing in *required {
            let fields: Vec<&str> = required.iter().copied().filter(|f| f != missing).collect();
            let found = check(&ribbon_with(&item(kind, &fields)));
            let expected = format!("{kind}: {missing} is verplicht");
            assert!(found.len() == 1 && found[0].ends_with(&expected), "{kind} zonder {missing}: {found:?}");
        }

        // Elk verboden veld toevoegen.
        for extra in *forbidden {
            let mut fields = required.to_vec();
            fields.push(extra);
            let found = check(&ribbon_with(&item(kind, &fields)));
            let expected = format!("{kind}: {extra} is niet toegestaan");
            assert!(found.len() == 1 && found[0].ends_with(&expected), "{kind} met {extra}: {found:?}");
        }

        // Optionele velden (niet verplicht, niet verboden) zijn toegestaan.
        for optional in ALL.iter().filter(|f| !required.contains(f) && !forbidden.contains(f)) {
            let mut fields = required.to_vec();
            fields.push(optional);
            let found = check(&ribbon_with(&item(kind, &fields)));
            assert!(found.is_empty(), "{kind} met optioneel {optional}: {found:?}");
        }
    }
}

#[test]
fn tooltip_en_shortcut_zijn_toegestaan_behalve_bij_custom() {
    for (kind, required, _) in RULES.iter().filter(|(k, _, _)| *k != "custom") {
        let base = item(kind, required);
        let cut = base.rfind(" }").unwrap();
        let with = format!("{}, tooltip = \"openaec.action.copy\", shortcut = \"Ctrl+V\" }}", &base[..cut]);
        let found = check(&ribbon_with(&with));
        assert!(found.is_empty(), "{kind}: {found:?}");
    }
    let custom = "{ type = \"custom\", slot = \"s\", tooltip = \"openaec.action.copy\", shortcut = \"Ctrl+V\" }";
    let found = check(&ribbon_with(custom));
    assert!(found.iter().any(|m| m.ends_with("custom: tooltip is niet toegestaan")), "{found:?}");
    assert!(found.iter().any(|m| m.ends_with("custom: shortcut is niet toegestaan")), "{found:?}");
}

#[test]
fn tooltip_wordt_als_label_gevalideerd() {
    let src = ribbon_with("{ type = \"large\", command = \"a.b\", icon = \"edit/paste\", label = \"openaec.action.paste\", tooltip = \"app.tip.ontbreekt\" }");
    let labels = AppLabels::from_json("{}", "{}").unwrap();
    let found = messages(validate_ribbon(&parse_ribbon(&src).unwrap(), Some(&labels)));
    assert!(found.iter().any(|m| m.contains("app.tip.ontbreekt") && m.contains("ontbreekt in nl")), "{found:?}");
    assert!(found.iter().any(|m| m.contains("app.tip.ontbreekt") && m.contains("ontbreekt in en")), "{found:?}");

    let src = ribbon_with("{ type = \"large\", command = \"a.b\", icon = \"edit/paste\", label = \"openaec.action.paste\", tooltip = \"openaec.nope\" }");
    let found = check(&src);
    assert!(found.iter().any(|m| m.contains("onbekende gedeelde term openaec.nope")), "{found:?}");
}

#[test]
fn ongeldige_namen_en_formaat() {
    let found = check(&ribbon_with("{ type = \"large\", command = \"Slecht\", icon = \"edit/paste\", label = \"openaec.action.paste\" }"));
    assert!(found.iter().any(|m| m.contains("ongeldige command-naam Slecht")), "{found:?}");

    let found = check(&ribbon_with(&item("large", &["command", "icon", "label"])).replace("id = \"home\"", "id = \"Home\""));
    assert!(found.iter().any(|m| m.contains("ongeldig tab-id Home")), "{found:?}");

    let found = check(&ribbon_with(&item("large", &["command", "icon", "label"])).replace("format = 1", "format = 2"));
    assert!(found.iter().any(|m| m.contains("onbekend formaat 2")), "{found:?}");
}

#[test]
fn dubbel_tab_id_over_include_heen() {
    let src = ribbon_with(&item("large", &["command", "icon", "label"]))
        .replace("id = \"home\"", "id = \"viewer3d\"")
        .replace("format = 1\n", "format = 1\ninclude = [\"openaec:viewer3d\"]\n");
    let found = check(&src);
    assert!(found.iter().any(|m| m.contains("dubbele tab-id viewer3d")), "{found:?}");
}

#[test]
fn onbekende_gedeelde_term() {
    let src = ribbon_with(&item("large", &["command", "icon", "label"])).replace("label = \"openaec.action.paste\"\n\n  [[tab.group]]", "label = \"openaec.bestaat.niet\"\n\n  [[tab.group]]");
    let found = check(&src);
    assert!(found.iter().any(|m| m.contains("onbekende gedeelde term openaec.bestaat.niet")), "{found:?}");
}

#[test]
fn label_ontbreekt_alleen_in_en() {
    let nl = fixture("app-nl.json");
    let labels = AppLabels::from_json(&nl, "{}").unwrap();
    let file = parse_ribbon(&fixture("valid.toml")).unwrap();
    let found = messages(validate_ribbon(&file, Some(&labels)));
    assert!(found.iter().any(|m| m.contains("ontbreekt in en")), "{found:?}");
    assert!(!found.iter().any(|m| m.contains("ontbreekt in nl")), "{found:?}");
}

#[test]
fn onbekend_icoon_op_menu_entry() {
    let src = fixture("valid.toml").replace(
        "{ command = \"insert.table.grid\", label = \"app.cmd.table.grid\" }",
        "{ command = \"insert.table.grid\", icon = \"edit/bestaat-niet\", label = \"app.cmd.table.grid\" }",
    );
    let labels = AppLabels::from_json(&fixture("app-nl.json"), &fixture("app-en.json")).unwrap();
    let found = messages(validate_ribbon(&parse_ribbon(&src).unwrap(), Some(&labels)));
    assert!(found.iter().any(|m| m.contains("items[0]") && m.contains("onbekend icoon edit/bestaat-niet")), "{found:?}");
}

#[test]
fn quick_access_zonder_include_is_een_fout() {
    let src = fixture("valid.toml").replace("include = [\"openaec:viewer3d\"]\n", "");
    let labels = AppLabels::from_json(&fixture("app-nl.json"), &fixture("app-en.json")).unwrap();
    let found = messages(validate_ribbon(&parse_ribbon(&src).unwrap(), Some(&labels)));
    assert!(found.iter().any(|m| m.contains("quick_access") && m.contains("view.fit-all")), "{found:?}");
    assert!(!found.iter().any(|m| m.contains("file.save") || m.contains("edit.undo")), "{found:?}");
}

#[test]
fn gedeelde_tab_staat_alleen_openaec_labels_toe() {
    let base = "shared = \"demo\"\nformat = 1\n\n[[tab]]\nid = \"demo\"\nlabel = \"openaec.ribbon.tab.viewer3d\"\n\n  [[tab.group]]\n  id = \"g\"\n  label = \"openaec.ribbon.group.file\"\n  items = [\n    ITEM,\n  ]\n";
    let shared_issues = |item: &str| messages(validate_shared(&parse_shared(&base.replace("ITEM", item)).expect("parse")));

    let ok = shared_issues("{ type = \"large\", command = \"view.load-model\", icon = \"view/load-model\", label = \"openaec.command.view.load-model\" }");
    assert!(ok.is_empty(), "{ok:?}");

    let entry = shared_issues("{ type = \"dropdown\", label = \"openaec.command.view.orbit\", items = [ { command = \"view.orbit\", label = \"app.eigen\" } ] }");
    assert!(entry.iter().any(|m| m.contains("alleen openaec.*-labels")), "{entry:?}");

    let tip = shared_issues("{ type = \"large\", command = \"view.orbit\", icon = \"view/orbit\", label = \"openaec.command.view.orbit\", tooltip = \"app.eigen\" }");
    assert!(tip.iter().any(|m| m.contains("alleen openaec.*-labels")), "{tip:?}");
}

#[test]
fn gedeelde_tab_naam_moet_een_id_zijn() {
    let src = "shared = \"Slecht Naam\"\nformat = 1\n\n[[tab]]\nid = \"demo\"\nlabel = \"openaec.ribbon.tab.viewer3d\"\n";
    let found = messages(validate_shared(&parse_shared(src).unwrap()));
    assert!(found.iter().any(|m| m.contains("ongeldige naam voor gedeelde tab Slecht Naam")), "{found:?}");
}
