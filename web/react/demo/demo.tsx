// A small app with the React components, to try keyboard, dialog and themes in a
// browser. Build and open: node scripts/check_react_components.mjs --demo
import { StrictMode, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ActionBar, applyDisplay, Banner, Button, ChoiceTiles, Dialog, DocumentTabs, IconButton, Menu, OpenAECProvider, Panel, PropertyRow,
  Select, StatusBar, Steps, Table, Tabs, TextField, Toast, type Theme,
} from "../src";

const rows = [
  { element: "Ligger 1", profiel: "HEA 200", uc: "0,64" },
  { element: "Ligger 2", profiel: "HEA 180", uc: "0,97" },
  { element: "Randligger as A tot en met D, verdieping 2", profiel: "IPE 300", uc: "0,81" },
];

function Demo() {
  const [theme, setTheme] = useState<Theme>("light");
  const [tab, setTab] = useState("start");
  const [doc, setDoc] = useState("velp");
  const [row, setRow] = useState(1);
  const [report, setReport] = useState("vol");
  const [dialog, setDialog] = useState(false);
  const [toast, setToast] = useState(false);
  const [thickness, setThickness] = useState("-20");
  const pickTheme = (value: string) => { setTheme(value as Theme); applyDisplay({ theme: value as Theme }); };
  return (
    <OpenAECProvider sprite="icons/standard.svg">
      <div className="oa-app" style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
        <Tabs label="Lint" tabs={[{ id: "start", label: "Start" }, { id: "beeld", label: "Beeld" }, { id: "rapport", label: "Rapport" }]} active={tab} onSelect={setTab} />
        <div style={{ display: "flex", gap: 8, padding: 8, alignItems: "center" }}>
          <Button kind="primary" icon="file.save" onClick={() => setToast(true)}>Opslaan</Button>
          <Button onClick={() => setDialog(true)}>Sluiten…</Button>
          <IconButton icon="edit.undo" label="Ongedaan maken" keys="Ctrl+Z" />
          <IconButton icon="edit.redo" label="Opnieuw" keys="Ctrl+Y" />
          <div style={{ width: 180, marginLeft: "auto" }}>
            <Select label="Thema" value={theme} onChange={(e) => pickTheme(e.target.value)} options={["light", "dark", "blueprint", "high-contrast-dark", "high-contrast-light"]} />
          </div>
        </div>
        <DocumentTabs tabs={[{ id: "velp", title: "Kantoor Velp", dirty: true }, { id: "arnhem", title: "Brug Arnhem" }]} active={doc} onSelect={setDoc} onClose={() => {}} />
        <div style={{ display: "grid", gridTemplateColumns: "240px 1fr", flex: 1 }}>
          <Panel title="Eigenschappen">
            <PropertyRow name="Profiel">{rows[row].profiel}</PropertyRow>
            <PropertyRow name="Unity check">{rows[row].uc}</PropertyRow>
            <div style={{ padding: 8 }}>
              <TextField label="Dikte (mm)" value={thickness} onChange={(e) => setThickness(e.target.value)} error={Number(thickness.replace(",", ".")) > 0 ? undefined : "Geef een waarde groter dan 0."} />
            </div>
          </Panel>
          <div style={{ padding: 16, display: "grid", gap: 16, alignContent: "start", background: "var(--oa-frame)" }}>
            <Banner tone="warning">Twee profielen hebben geen materiaal.</Banner>
            <Table label="Elementen" columns={[{ key: "element", label: "Element", maxWidth: 160 }, { key: "profiel", label: "Profiel" }, { key: "uc", label: "Unity check", numeric: true }]} rows={rows} selected={row} onSelect={setRow} />
            <Steps steps={["Gegevens", "Sjabloon", "Controle", "Maken"]} current={1} />
            <ChoiceTiles label="Soort rapport" value={report} onChange={setReport} className="demo-choices"
              options={[{ value: "vol", icon: "report.generate", title: "Volledig rapport", text: "Met alle berekeningen." }, { value: "kort", icon: "report.template", title: "Samenvatting", text: "Alleen de uitkomsten." }]} />
            <Menu label="Bewerken" items={[{ label: "Kopiëren", icon: "edit.copy", keys: "Ctrl+C", onSelect: () => {} }, { label: "Plakken", icon: "edit.paste", keys: "Ctrl+V", onSelect: () => {} }, "separator", { label: "Verwijderen", danger: true, onSelect: () => {} }]} />
            <ActionBar info="Stap 2 van 4"><Button>Vorige</Button><Button kind="primary">Volgende</Button></ActionBar>
          </div>
        </div>
        <StatusBar message="Gereed" items={[`${rows.length} elementen`, "100%"]} />
        <Dialog open={dialog} title="Wijzigingen opslaan?" onClose={() => setDialog(false)}
          actions={<><Button kind="quiet" onClick={() => setDialog(false)}>Niet opslaan</Button><Button onClick={() => setDialog(false)}>Annuleren</Button><Button kind="primary" onClick={() => setDialog(false)}>Opslaan</Button></>}>
          <p className="oa-secondary">Kantoor Velp heeft wijzigingen die nog niet zijn opgeslagen.</p>
        </Dialog>
        {toast && <div style={{ position: "fixed", right: 16, bottom: 32 }}><Toast title="Opgeslagen" onClose={() => setToast(false)}>Kantoor Velp is bewaard.</Toast></div>}
      </div>
    </OpenAECProvider>
  );
}

createRoot(document.getElementById("root")!).render(<StrictMode><Demo /></StrictMode>);
