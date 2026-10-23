#!/usr/bin/env python3
"""Pin Reports' reachable UI routes and build a source-grounded layout review."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/openaec-reports')
COMMIT = '818e58118c0f046410137a3f5a948e4871d21e77'
assert subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip() == COMMIT
BASE = 'frontend/src/'


def source(path: str) -> str:
    return subprocess.check_output(['git', '-C', str(REPO), 'show', f'HEAD:{path}'], text=True)


def evidence(path: str, needle: str) -> dict:
    lines = source(path).splitlines()
    matches = [number for number, line in enumerate(lines, 1) if needle in line]
    assert matches, (path, needle)
    number = matches[-1] if needle == 'if (viewMode === \'split\') {' else matches[0]
    return {
        'file': path, 'line': number, 'marker': needle,
        'url': f'https://github.com/OpenAEC-Foundation/openaec-reports/blob/{COMMIT}/{path}#L{number}',
    }


def route(identifier: str, label: str, category: str, path: str, marker: str, note: str) -> dict:
    return {'id': identifier, 'label': label, 'category': category,
            'evidence': evidence(path, marker), 'note': note}


app = BASE + 'App.tsx'
shell = BASE + 'components/layout/AppShell.tsx'
main = BASE + 'components/layout/MainPanel.tsx'
sidebar = BASE + 'components/layout/Sidebar.tsx'
admin = BASE + 'components/admin/AdminPanel.tsx'

routes = [
    route('loading', 'Sessie laden', 'access', app, 'if (isAuthLoading) {', 'Tijdelijke laadweergave vóór sessiecontrole.'),
    route('sso', 'SSO-doorsturen', 'access', app, 'return <LoginPage />;', 'Fallback-splash; productie stuurt doorgaans eerder via Caddy/Authentik door.'),
    route('projects', 'Projectbrowser', 'primary', shell, 'viewMode === "projects"', 'Projectlijst links; rapportentabel rechts. Data en acties vereisen de server.'),
    route('admin', 'Beheer', 'primary', shell, 'viewMode === "admin"', 'Zes beheertabs onder één Beheer-pagina; hun inhoud is afhankelijk van account/API.'),
    route('rapport', 'Rapportinstellingen', 'editor', main, "activePanel === 'rapport' && <MetadataForm />", 'Standaard documentpaneel uit de zijbalk.'),
    route('voorblad', 'Voorblad', 'editor', main, "activePanel === 'voorblad' && <CoverForm />", 'Documentformulier voor titelblad en afbeelding.'),
    route('colofon', 'Colofon', 'editor', main, "activePanel === 'colofon' && <ColofonForm />", 'Documentformulier voor colofon en revisies.'),
    route('opties', 'Opties', 'editor', main, "activePanel === 'opties' && <OptionsPanel />", 'Documentopties; niet hetzelfde als app-instellingen.'),
    route('field-group', 'Formuliergroep', 'editor', main, 'return <FieldGroupForm groupKey={activeFieldGroup} />;', 'Voorwaardelijk: alleen wanneer het template veldgroepen bevat.'),
    route('section', 'Hoofdstukeditor', 'editor', main, '<SectionHeader section={section} chapterNumber={chapterNumber} />', 'Sorteerbare inhoudsblokken met een eigen invoegtoolbox.'),
    route('appendix', 'Bijlage-editor', 'editor', main, 'return <AppendixEditor appendixId={activeAppendix} />;', 'Voorwaardelijk: alleen bij een geselecteerde bijlage.'),
    route('json', 'JSON-editor', 'mode', main, "if (viewMode === 'json') {", 'Bewerkbare ruwe JSON met Toepassen en Formatteren.'),
    route('split', 'Editor + PDF', 'mode', main, "if (viewMode === 'split') {", 'Editor links en PDF-preview rechts, elk een eigen scroll-/werkvlak.'),
    route('preview', 'PDF-preview', 'mode', main, "if (viewMode === 'preview') {", 'Auto-preview, paginakeuze, regenereren en een iframe bij beschikbare PDF.'),
]
assert len({entry['id'] for entry in routes}) == len(routes) == 14

admin_tabs = [
    ('tenants', 'Tenants', '<TenantManagement />'),
    ('users', 'Gebruikers', '<UserManagement />'),
    ('api-keys', 'API Keys', '<ApiKeyManagement />'),
    ('templates', 'YAML Bestanden', '<TemplateManagement />'),
    ('brand', 'Brand', '<BrandManagement />'),
    ('help', 'Help', '<HelpPanel />'),
]
admin_tabs = [{'id': ident, 'label': label,
               'evidence': evidence(admin, f'activeTab === "{ident}" && {component}')}
              for ident, label, component in admin_tabs]

overlays = [
    ('backstage', 'Bestand', '<Backstage'),
    ('settings', 'Instellingen', '<SettingsDialog'),
    ('feedback', 'Feedback', '<FeedbackDialog'),
    ('shortcuts', 'Sneltoetsen', '<ShortcutHelp'),
]
overlays = [{'id': ident, 'label': label, 'evidence': evidence(shell, marker)}
            for ident, label, marker in overlays]

preview_states = [
    ('offline', 'Geen API', '{!connected ? ('),
    ('empty', 'Nog geen PDF', 'Nog geen PDF gegenereerd'),
    ('generated', 'PDF beschikbaar', '{lastPdfUrl ? ('),
]
preview_states = [{'id': ident, 'label': label, 'evidence': evidence(main, marker)}
                  for ident, label, marker in preview_states]

report = json.loads(source('schemas/example_structural.json'))
sample = {'project': report['project'], 'number': report['project_number'],
          'status': report['status'], 'sections': [section['title'] for section in report['sections']]}
manifest = {
    'repository': 'openaec-reports', 'commit': COMMIT,
    'scope': 'Source-reachable frontend screen destinations and conditional variants. No runtime screenshots in the pinned repository.',
    'routes': routes, 'admin_tabs': admin_tabs, 'overlays': overlays,
    'preview_states': preview_states, 'sample': sample,
    'layout_evidence': {
        'sidebar_default_width_px': 288, 'sidebar_min_width_px': 200, 'sidebar_max_width_px': 480,
        'sidebar_source': evidence(sidebar, 'const SIDEBAR_DEFAULT_WIDTH = 288;'),
        'sidebar_visibility_source': evidence(shell, '{sidebarVisible && <Sidebar />}'),
        'split_source': evidence(main, "if (viewMode === 'split') {"),
    },
    'limits': ['The HTML uses shared OpenAEC colors and measured sidebar constraints, but title/ribbon/workspace sizes are design approximations.',
               'Backend data, PDF rendering, SSO redirection and form mutations are illustrative in the review.'],
}
out = ROOT / 'harmonization/reports-screen-routes.json'
out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
template = (ROOT / 'design/reports-screen-route-template.html').read_text()
(ROOT / 'design/reports-screen-route-review.html').write_text(
    template.replace('/*REPORTS_DATA*/', json.dumps(manifest, ensure_ascii=False).replace('</', '<\\/')))
print(f"Reports: {len(routes)} routes, {len(admin_tabs)} admin tabs, {len(overlays)} overlays, {len(preview_states)} preview states")
