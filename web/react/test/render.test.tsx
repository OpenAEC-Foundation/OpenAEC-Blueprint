// Renders every component to HTML and checks the markup the web package expects,
// with the accessibility attributes. Run through scripts/check_react_components.mjs.
import { renderToStaticMarkup } from "react-dom/server";
import type { ReactElement } from "react";
import {
  ActionBar, Banner, Button, Checkbox, ChoiceTiles, Dialog, DocumentTabs, EmptyState, FigureTile, IconButton, InfoCard, Menu, OpenAECProvider,
  Panel, Pill, Progress, PropertyRow, RecentList, Select, Sidebar, Status, StatusBar, Steps, Switch, Table, Tabs, TextField, Tile, Toast,
} from "../src";

declare const process: { exitCode?: number };

let failures = 0;
let checks = 0;
function html(element: ReactElement) {
  return renderToStaticMarkup(<OpenAECProvider sprite="icons/standard.svg">{element}</OpenAECProvider>);
}
function expect(name: string, markup: string, ...parts: string[]) {
  for (const part of parts) {
    checks++;
    if (!markup.includes(part)) {
      failures++;
      console.log(`FOUT ${name}: mist ${part}\n  ${markup}`);
    }
  }
}
const noop = () => {};

expect("knop", html(<Button kind="primary" icon="file.save">Opslaan</Button>), 'class="oa-button oa-button--primary"', 'type="button"', 'href="icons/standard.svg#i16-file.save"', 'aria-hidden="true"', "Opslaan");
expect("compacte knop", html(<Button compact>Compact</Button>), 'class="oa-button oa-button--compact"');
expect("iconknop", html(<IconButton icon="edit.undo" label="Ongedaan maken" keys="Ctrl+Z" />), 'aria-label="Ongedaan maken"', 'data-oa-tip="Ongedaan maken"', 'aria-keyshortcuts="Control+Z"', 'data-oa-keys="Ctrl+Z"');
expect("schakelknop", html(<IconButton icon="view.grid" label="Raster" pressed />), 'aria-pressed="true"');
const field = html(<TextField id="dikte" label="Dikte (mm)" error="Geef een waarde groter dan 0." defaultValue="-20" />);
expect("veld met fout", field, 'class="oa-label"', '<label for="dikte">Dikte (mm)</label>', 'class="oa-field"', 'aria-invalid="true"', 'aria-describedby="dikte-message"', 'class="oa-field-message" id="dikte-message"');
expect("keuzelijst", html(<Select id="d" label="Discipline" options={["Constructie", "Installaties"]} />), '<select id="d" class="oa-field"', '<option value="Installaties">Installaties</option>');
expect("vinkje", html(<Checkbox label="Rapport meesturen" defaultChecked />), 'class="oa-check"', 'type="checkbox"');
expect("schakelaar", html(<Switch label="Automatisch bijwerken" />), 'class="oa-switch"', 'role="switch"');
expect("voortgang", html(<Progress label="Rapport maken" value={62} />), 'role="progressbar"', 'aria-valuenow="62"', 'width:62%');
expect("status", html(<Status tone="success">Gereed</Status>), 'class="oa-status oa-status--success"');
expect("pil", html(<Pill label="Alle" count={18} active />), 'class="oa-pill"', 'aria-pressed="true"', 'class="oa-count"');
expect("tegel", html(<Tile icon="file.new" title="Nieuw project" text="Begin leeg." href="#" />), 'class="oa-tile"', 'class="oa-icon-tile"', "#i24-file.new", 'class="oa-tile-title"');
const choice = html(<ChoiceTiles label="Soort rapport" value="kort" onChange={noop} options={[{ value: "vol", icon: "report.generate", title: "Volledig" }, { value: "kort", icon: "report.template", title: "Samenvatting" }]} />);
expect("keuzetegels", choice, 'role="radiogroup"', 'aria-label="Soort rapport"', 'role="radio" aria-checked="false" tabindex="-1"', 'role="radio" aria-checked="true" tabindex="0"', 'class="oa-tile oa-tile--choice"');
expect("recent", html(<RecentList items={[{ name: "Kantoor Velp", path: "D:\\Projecten", when: "vandaag" }]} />), 'class="oa-recent"', "<b>Kantoor Velp</b>", 'class="oa-meta"');
expect("infokaart", html(<InfoCard title="Project" facts={[["Nummer", "2026-041"]]} />), 'class="oa-info-card"', "<dt>Nummer</dt><dd>2026-041</dd>");
expect("cijfer", html(<FigureTile value={7} label="Geïnstalleerd" accent />), 'class="oa-figure oa-figure--accent"');
expect("fout", html(<Banner tone="error" onClose={noop}>Niet opgeslagen.</Banner>), 'class="oa-banner oa-banner--error"', 'role="alert"', "<b>Fout.</b>", 'aria-label="Sluiten"');
expect("let op", html(<Banner tone="warning">Twee profielen.</Banner>), 'role="status"', "<b>Let op.</b>");
expect("toast", html(<Toast title="Opgeslagen" onClose={noop}>Bewaard.</Toast>), 'class="oa-toast"', 'role="status"', "<b>Opgeslagen</b>");
const menu = html(<Menu label="Bewerken" items={[{ label: "Kopiëren", icon: "edit.copy", keys: "Ctrl+C", onSelect: noop }, "separator", { label: "Verwijderen", danger: true, onSelect: noop }]} />);
expect("menu", menu, 'role="menu"', 'role="menuitem"', "<kbd>Ctrl+C</kbd>", "<hr/>", 'class="oa-danger"');
const dialog = html(<Dialog open={false} title="Wijzigingen opslaan?" onClose={noop} actions={<Button kind="primary">Opslaan</Button>}><p>Tekst</p></Dialog>);
expect("dialoog", dialog, '<dialog class="oa-dialog" aria-labelledby=', 'class="oa-heading oa-heading--dialog"', 'class="oa-dialog-actions"');
expect("tabs", html(<Tabs label="Lint" tabs={[{ id: "start", label: "Start" }, { id: "beeld", label: "Beeld" }]} active="start" onSelect={noop} />), 'class="oa-tabs" role="tablist" aria-label="Lint"', 'role="tab" aria-selected="true" tabindex="0"', 'role="tab" aria-selected="false" tabindex="-1"');
const docs = html(<DocumentTabs tabs={[{ id: "a", title: "Kantoor Velp", dirty: true }]} active="a" onSelect={noop} onClose={noop} />);
expect("documenttabs", docs, 'class="oa-document-tabs" role="tablist"', 'class="oa-document-tab" role="tab" aria-selected="true"', 'class="oa-dirty" role="img" aria-label="niet opgeslagen"', 'aria-label="Sluiten: Kantoor Velp"');
expect("paneel", html(<Panel title="Eigenschappen"><PropertyRow name="Profiel">HEA 200</PropertyRow></Panel>), 'class="oa-panel" aria-label="Eigenschappen"', 'class="oa-panel-header"', 'class="oa-property"');
const table = html(<Table label="Elementen" columns={[{ key: "naam", label: "Element", maxWidth: 120 }, { key: "uc", label: "Unity check", numeric: true }]} rows={[{ naam: "Ligger 1", uc: "0,64" }, { naam: "Randligger as A tot en met D", uc: "0,81" }]} selected={1} onSelect={noop} />);
expect("tabel", table, 'class="oa-table" aria-label="Elementen"', '<th scope="col"', 'class="oa-number">0,64', 'aria-selected="true" tabindex="0"', 'aria-selected="false" tabindex="-1"', 'data-oa-tip="Randligger as A tot en met D"', 'class="oa-truncate"');
expect("statusbalk", html(<StatusBar message="Gereed" items={["3 elementen", "100%"]} />), 'class="oa-statusbar" role="status"', 'class="oa-spacer"');
expect("zijbalk", html(<Sidebar title="Rapport" items={[{ id: "a", label: "Gegevens" }, { id: "b", label: "Sjabloon" }]} current="b" />), 'class="oa-sidebar" aria-label="Rapport"', 'aria-current="page"');
expect("stappen", html(<Steps steps={["Gegevens", "Sjabloon", "Maken"]} current={1} />), 'class="oa-steps"', '<li class="oa-done">Gegevens</li>', '<li aria-current="step">Sjabloon</li>');
expect("actiebalk", html(<ActionBar info="Stap 2 van 4"><Button>Vorige</Button></ActionBar>), 'class="oa-action-bar"', "Stap 2 van 4");
expect("leeg", html(<EmptyState icon="view.search" title="Geen resultaten">Pas de zoekterm aan.</EmptyState>), 'class="oa-empty"', "#i24-view.search");

console.log(failures ? `${failures} van ${checks} controles mislukt` : `React-componenten: ${checks} controles op 30 componenten geslaagd`);
process.exitCode = failures ? 1 : 0;
