use openaec_ribbon::*;
use std::process::ExitCode;

fn read(path: &str) -> Result<String, String> {
    std::fs::read_to_string(path).map_err(|e| format!("{path}: {e}"))
}

fn report(name: &str, issues: &[Issue]) -> bool {
    for i in issues {
        eprintln!("{name}: {}: {}", i.path, i.message);
    }
    issues.is_empty()
}

fn run(args: &[String]) -> Result<bool, String> {
    match args.first().map(String::as_str) {
        Some("check") => {
            let file = args.get(1).ok_or("gebruik: openaec-ribbon check <ribbon.toml> [--nl <nl.json> --en <en.json>]")?;
            let opt = |flag: &str| args.iter().position(|a| a == flag).and_then(|i| args.get(i + 1));
            let labels = match (opt("--nl"), opt("--en")) {
                (Some(nl), Some(en)) => Some(AppLabels::from_json(&read(nl)?, &read(en)?)?),
                (None, None) => {
                    eprintln!("let op: app-labels niet gecontroleerd (geef --nl en --en mee)");
                    None
                }
                _ => return Err("--nl en --en horen samen".into()),
            };
            let ribbon = parse_ribbon(&read(file)?).map_err(|e| format!("{file}: {e}"))?;
            Ok(report(file, &validate_ribbon(&ribbon, labels.as_ref())))
        }
        Some("check-shared") => {
            let dir = args.get(1).ok_or("gebruik: openaec-ribbon check-shared <map>")?;
            let mut ok = true;
            let mut entries: Vec<_> = std::fs::read_dir(dir).map_err(|e| e.to_string())?
                .filter_map(|e| e.ok()).map(|e| e.path())
                .filter(|p| p.extension().is_some_and(|x| x == "toml")).collect();
            entries.sort();
            for path in entries {
                let name = path.display().to_string();
                let shared = parse_shared(&read(&name)?).map_err(|e| format!("{name}: {e}"))?;
                ok &= report(&name, &validate_shared(&shared));
            }
            Ok(ok)
        }
        _ => Err("gebruik: openaec-ribbon check|check-shared …".into()),
    }
}

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    match run(&args) {
        Ok(true) => { println!("✓ geldig"); ExitCode::SUCCESS }
        Ok(false) => ExitCode::from(1),
        Err(e) => { eprintln!("{e}"); ExitCode::from(2) }
    }
}
