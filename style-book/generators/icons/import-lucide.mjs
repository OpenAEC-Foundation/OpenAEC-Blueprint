// Eenmalige import van UI-basisiconen uit lucide-static (ISC; deels MIT via Feather).
// Gebruik: node generators/icons/import-lucide.mjs <pad-naar-lucide-static/icons>
// Licentietekst: design/icons/LICENSE-lucide.txt (kopie van het LICENSE-bestand van het pakket).
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { repoPath } from "../lib/paths.mjs";
import { parseToml } from "../lib/toml.mjs";
import { importIcons, manifestToml } from "./import.mjs";

// lucide-naam → [id, nl, en, tags]
const MAP = {
  "menu": ["ui/menu", "Menu", "Menu", ["ui", "navigation"]],
  "x": ["ui/close", "Sluiten", "Close", ["ui", "window"]],
  "search": ["ui/search", "Zoeken", "Search", ["ui"]],
  "bell": ["ui/notifications", "Meldingen", "Notifications", ["ui"]],
  "user": ["ui/user", "Gebruiker", "User", ["ui", "account"]],
  "users": ["ui/users", "Gebruikers", "Users", ["ui", "account"]],
  "user-plus": ["ui/user-add", "Gebruiker toevoegen", "Add user", ["ui", "account"]],
  "key-round": ["ui/license", "Licentie", "License", ["ui", "account", "security"]],
  "layout-grid": ["ui/apps", "Apps", "Apps", ["ui", "navigation"]],
  "credit-card": ["ui/billing", "Facturering", "Billing", ["ui", "account"]],
  "receipt": ["ui/invoice", "Factuur", "Invoice", ["ui", "account"]],
  "file-text": ["ui/document", "Document", "Document", ["ui", "file"]],
  "chart-column": ["ui/chart", "Grafiek", "Chart", ["ui", "report"]],
  "shield": ["ui/security", "Beveiliging", "Security", ["ui", "security"]],
  "lock": ["ui/lock", "Vergrendeld", "Locked", ["ui", "security"]],
  "scroll-text": ["ui/log", "Logboek", "Log", ["ui"]],
  "life-buoy": ["ui/support", "Ondersteuning", "Support", ["ui", "help"]],
  "circle-question-mark": ["ui/question", "Vraag", "Question", ["ui", "help"]],
  "download": ["ui/download", "Downloaden", "Download", ["ui", "file"]],
  "upload": ["ui/upload", "Uploaden", "Upload", ["ui", "file"]],
  "funnel": ["ui/filter", "Filteren", "Filter", ["ui", "data"]],
  "arrow-up-narrow-wide": ["ui/sort-asc", "Oplopend sorteren", "Sort ascending", ["ui", "data"]],
  "arrow-down-wide-narrow": ["ui/sort-desc", "Aflopend sorteren", "Sort descending", ["ui", "data"]],
  "chevron-left": ["ui/chevron-left", "Naar links", "Left", ["ui", "navigation"]],
  "chevron-right": ["ui/chevron-right", "Naar rechts", "Right", ["ui", "navigation"]],
  "chevron-up": ["ui/chevron-up", "Omhoog", "Up", ["ui", "navigation"]],
  "chevron-down": ["ui/chevron-down", "Omlaag", "Down", ["ui", "navigation"]],
  "plus": ["ui/plus", "Toevoegen", "Add", ["ui"]],
  "minus": ["ui/minus", "Verwijderen uit", "Remove", ["ui"]],
  "ellipsis": ["ui/more", "Meer", "More", ["ui"]],
  "pencil": ["ui/edit", "Bewerken", "Edit", ["ui"]],
  "trash-2": ["ui/delete", "Verwijderen", "Delete", ["ui"]],
  "external-link": ["ui/external-link", "Openen in nieuw venster", "Open externally", ["ui", "navigation"]],
  "refresh-cw": ["ui/refresh", "Vernieuwen", "Refresh", ["ui"]],
  "triangle-alert": ["ui/warning", "Waarschuwing", "Warning", ["ui", "status"]],
  "circle-x": ["ui/error", "Fout", "Error", ["ui", "status"]],
  "circle-check": ["ui/success", "Gelukt", "Success", ["ui", "status"]],
  "cloud": ["ui/cloud", "Cloud", "Cloud", ["ui"]],
  "database": ["ui/database", "Opslag", "Storage", ["ui"]],
  "sparkles": ["ui/ai", "AI", "AI", ["ui"]],
  "mail": ["ui/mail", "E-mail", "Email", ["ui"]],
  "globe": ["ui/domain", "Domein", "Domain", ["ui"]],
  "activity": ["ui/status", "Servicestatus", "Service status", ["ui", "status"]],
  "chevrons-down-up": ["ui/collapse", "Inklappen", "Collapse", ["ui"]],
  "chevrons-up-down": ["ui/expand", "Uitklappen", "Expand", ["ui"]],
};

const source = process.argv[2];
if (!source) {
  console.error("gebruik: node generators/icons/import-lucide.mjs <pad-naar-lucide-static/icons>");
  process.exit(2);
}

const manifestPath = repoPath("design", "icons", "icons.toml");
const existing = parseToml(readFileSync(manifestPath, "utf8")).icon ?? [];
const taken = new Set(existing.map((e) => e.id));

const entries = Object.entries(MAP)
  .filter(([, [id]]) => !taken.has(id))
  .map(([name, [id, nl, en, tags]]) => ({
    id,
    // lucide zet class="lucide …" op de root; dat attribuut staat niet op de allow-list.
    svg: readFileSync(join(source, `${name}.svg`), "utf8").replace(/\sclass="[^"]*"/, ""),
    label: { nl, en },
    tags,
    source: "lucide",
  }));

const { written, duplicates } = importIcons(entries, repoPath("design", "icons"));
writeFileSync(manifestPath, manifestToml([...existing, ...written]), "utf8");
console.log(`${written.length} iconen toegevoegd, ${Object.keys(MAP).length - entries.length} bestonden al`);
for (const [a, b] of duplicates) console.log(`dubbel: ${a} = ${b} (overgeslagen)`);
