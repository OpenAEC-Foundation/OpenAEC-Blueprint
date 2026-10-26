//! The C library of OpenAEC Blueprint.
//!
//! Gives tools that are not written in Rust the same design tokens and B2
//! icons as the Rust library: C, C++, C#, Python and anything else that can
//! call a C function. Every string it returns is UTF-8, ends with a NUL byte
//! and stays valid for the life of the program; the caller never frees it.
//! The functions are safe to call from any thread.
//!
//! The header is `include/openaec_blueprint.h`; `examples/list_icons.c` shows
//! the calls.

use std::collections::HashMap;
use std::ffi::{c_char, CStr, CString};
use std::sync::{Mutex, OnceLock};

use openaec_icons::{Icon, Size};

/// The version of this library, the same as the release: `YYYY.W.N`.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// The design tokens of UI 0.4, the single source of colours, sizes and fonts.
pub const TOKENS_JSON: &str = include_str!("../../../design/ontwerp-0.4/tokens-0.4.json");

/// A string kept for the life of the program, with a NUL at the end.
fn leak(text: &str) -> *const c_char {
    // The texts are SVG, JSON and identifiers: none holds a NUL byte.
    Box::leak(CString::new(text).expect("no NUL byte inside").into_boxed_c_str()).as_ptr()
}

fn interned(key: String, make: impl FnOnce() -> String) -> *const c_char {
    struct Ptr(*const c_char);
    // SAFETY: the pointers point at leaked, never-changed memory.
    unsafe impl Send for Ptr {}
    static CACHE: OnceLock<Mutex<HashMap<String, Ptr>>> = OnceLock::new();
    let mut cache = CACHE.get_or_init(Default::default).lock().unwrap_or_else(|e| e.into_inner());
    cache.entry(key).or_insert_with(|| Ptr(leak(&make()))).0
}

/// Reads a C string argument; `None` for a null pointer or invalid UTF-8.
///
/// # Safety
/// `text` is null or points at a NUL-terminated string.
unsafe fn arg<'a>(text: *const c_char) -> Option<&'a str> {
    if text.is_null() {
        return None;
    }
    CStr::from_ptr(text).to_str().ok()
}

fn ordered() -> &'static [Icon] {
    static ALL: OnceLock<Vec<Icon>> = OnceLock::new();
    ALL.get_or_init(|| {
        let mut all = Icon::all();
        all.sort_by_key(|icon| icon.id());
        all
    })
}

/// The version of the library, such as "2026.44.0".
#[no_mangle]
pub extern "C" fn oa_version() -> *const c_char {
    interned("version".into(), || VERSION.into())
}

/// All design tokens as one JSON document.
#[no_mangle]
pub extern "C" fn oa_tokens_json() -> *const c_char {
    interned("tokens".into(), || TOKENS_JSON.into())
}

/// The number of icons.
#[no_mangle]
pub extern "C" fn oa_icon_count() -> usize {
    ordered().len()
}

/// The identifier of the icon at `index`, in alphabetical order, such as
/// "file.open"; null when `index` is not below `oa_icon_count()`.
#[no_mangle]
pub extern "C" fn oa_icon_id(index: usize) -> *const c_char {
    match ordered().get(index) {
        Some(icon) => interned(format!("id:{}", icon.id()), || icon.id().into()),
        None => std::ptr::null(),
    }
}

/// The Dutch label of an icon, such as "Openen"; null for an unknown id.
///
/// # Safety
/// `id` is null or points at a NUL-terminated string.
#[no_mangle]
pub unsafe extern "C" fn oa_icon_label(id: *const c_char) -> *const c_char {
    match arg(id).and_then(Icon::from_id) {
        Some(icon) => interned(format!("label:{}", icon.id()), || icon.label().into()),
        None => std::ptr::null(),
    }
}

/// The SVG text of an icon for a size in pixels: up to 18 px gives the 16 px
/// master, larger sizes the 24 px master. The main colour is `currentColor`,
/// the accent `var(--icon-accent, currentColor)`. Null for an unknown id.
///
/// # Safety
/// `id` is null or points at a NUL-terminated string.
#[no_mangle]
pub unsafe extern "C" fn oa_icon_svg(id: *const c_char, pixels: u32) -> *const c_char {
    let Some(icon) = arg(id).and_then(Icon::from_id) else {
        return std::ptr::null();
    };
    let size = Size::for_pixels(pixels as f32);
    let master = if size == Size::S16 { 16 } else { 24 };
    interned(format!("svg:{}:{master}", icon.id()), || icon.svg(size).into())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn text(ptr: *const c_char) -> &'static str {
        assert!(!ptr.is_null());
        unsafe { CStr::from_ptr(ptr) }.to_str().unwrap()
    }

    #[test]
    fn version_is_year_week_number() {
        let version = text(oa_version());
        let parts: Vec<u32> = version.split('.').map(|p| p.parse().unwrap()).collect();
        assert_eq!(parts.len(), 3, "{version}");
        assert!(parts[0] >= 2026 && (1..=53).contains(&parts[1]), "{version}");
        assert!(!version.split('.').nth(1).unwrap().starts_with('0'), "no leading zero in the week");
    }

    #[test]
    fn tokens_are_json() {
        let tokens = text(oa_tokens_json());
        assert!(tokens.trim_start().starts_with('{') && tokens.trim_end().ends_with('}'));
        assert!(tokens.contains("#D97706"), "the OpenAEC amber is a token");
    }

    #[test]
    fn every_icon_is_reachable_by_index_and_id() {
        let count = oa_icon_count();
        assert!(count >= 900, "{count}");
        assert!(oa_icon_id(count).is_null());
        for index in 0..count {
            let id = oa_icon_id(index);
            let name = text(id);
            unsafe {
                assert!(!text(oa_icon_label(id)).is_empty(), "{name}");
                let small = text(oa_icon_svg(id, 16));
                let large = text(oa_icon_svg(id, 32));
                assert!(small.starts_with("<svg") && large.starts_with("<svg"), "{name}");
                // The same pointer on a second call: nothing is allocated twice.
                assert_eq!(oa_icon_svg(id, 16), oa_icon_svg(id, 12));
            }
        }
    }

    #[test]
    fn unknown_and_null_ids_give_null() {
        unsafe {
            assert!(oa_icon_svg(std::ptr::null(), 16).is_null());
            assert!(oa_icon_label(c"does.not-exist".as_ptr()).is_null());
            assert!(oa_icon_svg(c"does.not-exist".as_ptr(), 24).is_null());
        }
    }
}
