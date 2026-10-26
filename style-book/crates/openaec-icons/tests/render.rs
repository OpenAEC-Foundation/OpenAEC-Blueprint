use openaec_icons::Icon;
use openaec_tokens::{DARK, LIGHT};
use resvg::{tiny_skia, usvg};
use std::path::PathBuf;

const SIZE: u32 = 48;

fn render(svg: &str) -> tiny_skia::Pixmap {
    let tree = usvg::Tree::from_str(svg, &usvg::Options::default()).expect("SVG moet parsen");
    let mut pixmap = tiny_skia::Pixmap::new(SIZE, SIZE).unwrap();
    let scale = SIZE as f32 / tree.size().width();
    resvg::render(&tree, tiny_skia::Transform::from_scale(scale, scale), &mut pixmap.as_mut());
    pixmap
}

fn snapshot_path(icon: Icon, theme: &str) -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("tests/snapshots")
        .join(format!("{}.{theme}.png", icon.id().replace('/', "__")))
}

/// Max. 0,5% van de pixels mag meer dan 2 per kanaal afwijken (afrondingsverschillen per platform).
fn close_enough(a: &tiny_skia::Pixmap, b: &tiny_skia::Pixmap) -> bool {
    let diff = a.data().chunks(4).zip(b.data().chunks(4))
        .filter(|(p, q)| p.iter().zip(q.iter()).any(|(x, y)| x.abs_diff(*y) > 2))
        .count();
    diff * 200 <= (SIZE * SIZE) as usize
}

#[test]
fn ids_zijn_uniek_en_terug_te_vinden() {
    for icon in Icon::ALL {
        assert_eq!(Icon::from_id(icon.id()), Some(*icon));
    }
    assert_eq!(Icon::from_id("bestaat/niet"), None);
}

#[test]
fn elk_icoon_rendert_en_komt_overeen_met_snapshot() {
    let update = std::env::var("UPDATE_SNAPSHOTS").is_ok();
    for icon in Icon::ALL {
        for (theme, color) in [("light", LIGHT.text_primary), ("dark", DARK.text_primary)] {
            let pixmap = render(&icon.svg_colored(&color.to_hex()));
            assert!(pixmap.data().iter().skip(3).step_by(4).any(|a| *a > 0), "{} rendert leeg", icon.id());
            let path = snapshot_path(*icon, theme);
            if update {
                std::fs::create_dir_all(path.parent().unwrap()).unwrap();
                pixmap.save_png(&path).unwrap();
                continue;
            }
            let expected = tiny_skia::Pixmap::load_png(&path)
                .unwrap_or_else(|_| panic!("snapshot ontbreekt: {} — draai met UPDATE_SNAPSHOTS=1", path.display()));
            assert!(close_enough(&pixmap, &expected), "{} ({theme}) wijkt af van snapshot", icon.id());
        }
    }
}
