use openaec_i18n::{has_key, t, Lang, KEYS};

#[test]
fn vertalingen() {
    assert_eq!(t(Lang::Nl, "action.copy"), Some("Kopiëren"));
    assert_eq!(t(Lang::En, "openaec.action.copy"), Some("Copy"));
    assert_eq!(t(Lang::Nl, "bestaat.niet"), None);
}

#[test]
fn alle_sleutels_in_beide_talen() {
    for key in KEYS {
        assert!(t(Lang::Nl, key).is_some() && t(Lang::En, key).is_some(), "{key}");
        assert!(has_key(key));
    }
}
