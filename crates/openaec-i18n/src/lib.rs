//! Gedeelde OpenAEC-termen. Bron: `design/i18n/` in OpenAEC-style-book.

mod generated;
pub use generated::KEYS;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Lang {
    Nl,
    En,
}

/// Vertaling van een gedeelde sleutel, bijv. `t(Lang::Nl, "action.copy")`.
/// Het voorvoegsel `openaec.` mag erbij staan of weggelaten worden.
pub fn t(lang: Lang, key: &str) -> Option<&'static str> {
    let key = key.strip_prefix("openaec.").unwrap_or(key);
    match lang {
        Lang::Nl => generated::nl(key),
        Lang::En => generated::en(key),
    }
}

/// `true` als de sleutel in alle talen bestaat (de generator garandeert gelijke sleutels).
pub fn has_key(key: &str) -> bool {
    t(Lang::Nl, key).is_some()
}
