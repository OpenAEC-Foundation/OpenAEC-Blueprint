use serde::Deserialize;

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RibbonFile {
    pub app: String,
    pub format: u32,
    #[serde(default)]
    pub include: Vec<String>,
    pub quick_access: Option<QuickAccess>,
    #[serde(default, rename = "tab")]
    pub tabs: Vec<Tab>,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SharedTabFile {
    pub shared: String,
    pub format: u32,
    #[serde(rename = "tab")]
    pub tabs: Vec<Tab>,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct QuickAccess {
    pub items: Vec<String>,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Tab {
    pub id: String,
    pub label: String,
    pub contextual: Option<String>,
    #[serde(default, rename = "group")]
    pub groups: Vec<Group>,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Group {
    pub id: String,
    pub label: String,
    #[serde(default)]
    pub items: Vec<Item>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum ItemKind {
    Large,
    Small,
    Toggle,
    Dropdown,
    LargeDropdown,
    Split,
    Combo,
    Custom,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Item {
    #[serde(rename = "type")]
    pub kind: ItemKind,
    pub command: Option<String>,
    pub icon: Option<String>,
    pub label: Option<String>,
    pub shortcut: Option<String>,
    pub tooltip: Option<String>,
    pub slot: Option<String>,
    #[serde(default)]
    pub items: Vec<MenuEntry>,
}

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct MenuEntry {
    pub command: String,
    pub icon: Option<String>,
    pub label: String,
    pub shortcut: Option<String>,
}
