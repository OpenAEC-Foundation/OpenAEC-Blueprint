use openaec_ribbon::*;

fn fixture(name: &str) -> String {
    std::fs::read_to_string(format!("{}/tests/fixtures/{name}", env!("CARGO_MANIFEST_DIR"))).unwrap()
}

fn labels() -> AppLabels {
    AppLabels::from_json(&fixture("app-nl.json"), &fixture("app-en.json")).unwrap()
}

fn issues(src: &str) -> Vec<String> {
    let file = parse_ribbon(src).expect("parse");
    validate_ribbon(&file, Some(&labels())).into_iter().map(|i| format!("{}: {}", i.path, i.message)).collect()
}

#[test]
fn geldige_ribbon_heeft_geen_fouten() {
    assert_eq!(issues(&fixture("valid.toml")), Vec::<String>::new());
}

#[test]
fn onbekend_veld_is_een_parsefout() {
    let src = fixture("valid.toml").replace("icon = \"edit/paste\"", "icn = \"edit/paste\"");
    let err = parse_ribbon(&src).unwrap_err();
    assert!(err.contains("icn"), "{err}");
}

#[test]
fn onbekend_icoon_en_ontbrekend_label() {
    let src = fixture("valid.toml")
        .replace("icon = \"edit/cut\"", "icon = \"edit/bestaat-niet\"")
        .replace("label = \"app.cmd.table\"", "label = \"app.cmd.ontbreekt\"");
    let found = issues(&src);
    assert!(found.iter().any(|m| m.contains("edit/bestaat-niet") && m.contains("onbekend icoon")), "{found:?}");
    assert!(found.iter().any(|m| m.contains("app.cmd.ontbreekt") && m.contains("ontbreekt in nl")), "{found:?}");
}

#[test]
fn verplichte_en_verboden_velden_per_type() {
    let src = fixture("valid.toml").replace(
        "{ type = \"custom\", slot = \"layer-combo\" }",
        "{ type = \"custom\", slot = \"layer-combo\", label = \"app.group.custom\" }, { type = \"large\", command = \"x.y\", label = \"app.group.custom\" }",
    );
    let found = issues(&src);
    assert!(found.iter().any(|m| m.contains("custom") && m.contains("label is niet toegestaan")), "{found:?}");
    assert!(found.iter().any(|m| m.contains("icon is verplicht")), "{found:?}");
}

#[test]
fn dubbele_ids_onbekende_include_en_quick_access() {
    let src = fixture("valid.toml")
        .replace("include = [\"openaec:viewer3d\"]", "include = [\"openaec:viewer3d\", \"openaec:bestaat-niet\"]")
        .replace("id = \"custom\"", "id = \"clipboard\"")
        .replace("\"view.fit-all\"]", "\"view.fit-all\", \"nergens.gedefinieerd\"]");
    let found = issues(&src);
    assert!(found.iter().any(|m| m.contains("openaec:bestaat-niet")), "{found:?}");
    assert!(found.iter().any(|m| m.contains("dubbele groep-id clipboard")), "{found:?}");
    assert!(found.iter().any(|m| m.contains("nergens.gedefinieerd")), "{found:?}");
}

#[test]
fn gedeelde_tabs_zijn_geldig() {
    for (name, src) in SHARED_TABS {
        let file = parse_shared(src).unwrap_or_else(|e| panic!("{name}: {e}"));
        assert_eq!(file.shared, *name);
        assert!(validate_shared(&file).is_empty(), "{name}: {:?}", validate_shared(&file));
    }
}
