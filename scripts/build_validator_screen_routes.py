#!/usr/bin/env python3
"""Pin the two BIM Validator UI branches and generate their visual route review."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/tmp/openaec-inventory/OpenAEC-BIM-validator')
COMMIT = '8f837dd9a56e12d9b61ddd9dd2b341abe9794256'
assert subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip() == COMMIT


def source(path: str) -> list[str]:
    return subprocess.check_output(['git', '-C', str(REPO), 'show', f'HEAD:{path}'], text=True).splitlines()


def evidence(path: str, marker: str) -> dict:
    lines = source(path)
    matches = [i for i, line in enumerate(lines, 1) if marker in line]
    assert matches, (path, marker)
    line = matches[-1] if marker == 'return <AppShell />;' else matches[0]
    return {'file': path, 'line': line, 'marker': marker,
            'url': f'https://github.com/OpenAEC-Foundation/OpenAEC-BIM-validator/blob/{COMMIT}/{path}#L{line}'}


def state(id_: str, label: str, branch: str, path: str, marker: str, note: str) -> dict:
    return {'id': id_, 'label': label, 'branch': branch, 'note': note, 'evidence': evidence(path, marker)}


base = 'viewer/src/'
app = base + 'App.tsx'
shell = base + 'components/layout/AppShell.tsx'
left = base + 'components/layout/LeftPanel.tsx'
right = base + 'components/layout/RightPanel.tsx'
center = base + 'components/layout/CenterPanel.tsx'
validation = base + 'components/validation/ValidationPanel.tsx'
legacy = base + 'LegacyValidationView.tsx'
bcf = base + 'components/bcf/BcfPanel.tsx'

routes = [
    state('viewer-empty', 'Viewer · leeg', 'viewer', left, 'Upload een IFC bestand', 'Geen project of model; 3D-engine laadt afzonderlijk.'),
    state('viewer-model', 'Viewer · model', 'viewer', shell, 'hasLoadedModel = project?.models.some', 'Drie panelen: modellen/eigenschappen links, 3D midden, validatie rechts.'),
    state('viewer-submitting', 'Validatie · upload', 'viewer', validation, 'Bestanden uploaden...', 'Rechter validatiepaneel toont de submit-status.'),
    state('viewer-polling', 'Validatie · voortgang', 'viewer', validation, 'phase === "polling"', 'Rechter validatiepaneel toont voortgang en annuleren.'),
    state('viewer-results', 'Validatie · resultaten', 'viewer', validation, '{validationResult && (', 'Resultatenboom en geselecteerd detail staan rechts van de 3D-canvas.'),
    state('viewer-error', 'Validatie · fout', 'viewer', validation, '{validationError && (', 'Compacte foutweergave in het rechterpaneel.'),
    state('viewer-clashes', 'Clashes · binnenkort', 'viewer', right, 'Clash detection — binnenkort beschikbaar', 'Tab bestaat, maar clashdetectie is nog een lege toestand.'),
    state('viewer-bcf', 'BCF · wachtrij', 'viewer', bcf, '<BcfIssueQueue />', 'BCF-tab met wachtrij; lokale export verschijnt alleen bij issues.'),
    state('legacy-idle', 'Legacy · invoer', 'legacy', legacy, 'type AppPhase = "idle"', 'Zelfstandig upload- en IDS-scherm op /validate, zonder ribbon of 3D-paneel.'),
    state('legacy-submitting', 'Legacy · upload', 'legacy', legacy, 'Uploading files and starting validation...', 'Zelfstandige upload-/submitstatus.'),
    state('legacy-polling', 'Legacy · voortgang', 'legacy', legacy, 'phase === "polling" || phase === "submitting"', 'Voortgang met annuleeractie.'),
    state('legacy-completed', 'Legacy · resultaat', 'legacy', legacy, '{validationResult && (', 'Samenvatting met specificatielijst en JSON-download.'),
    state('legacy-error', 'Legacy · fout', 'legacy', legacy, '{error && (', 'Foutkaart met opnieuw proberen en sluiten.'),
]
assert len({route['id'] for route in routes}) == len(routes) == 13

right_tabs = [
    state('validation', 'Validatie', 'tab', right, '{ id: "validation", label: "Validatie" }', 'IDS, status, resultaten en detail.'),
    state('clashes', 'Clashes', 'tab', right, '{ id: "clashes", label: "Clashes" }', 'Huidige lege toestand.'),
    state('bcf', 'BCF', 'tab', right, '{ id: "bcf", label: "BCF" }', 'Lokale issue-wachtrij en export.'),
]
overlays = [
    state('backstage', 'Bestand', 'overlay', shell, '<Backstage', 'Bestand-weergave.'),
    state('settings', 'Instellingen', 'overlay', shell, '<SettingsDialog', 'Thema en voorkeuren.'),
    state('feedback', 'Feedback', 'overlay', shell, '<FeedbackDialog', 'Feedbackdialoog.'),
    state('cloud', 'Cloud', 'overlay', shell, '<CloudDialog', 'Openen/opslaan via cloud.'),
    state('save-as', 'Opslaan als', 'overlay', shell, '<SaveAsDialog', 'Lokale/cloud opslaandialoog.'),
    state('open', 'Openen', 'overlay', shell, '<OpenDialog', 'Lokale/cloud opendialoog.'),
]
manifest = {
    'repository': 'OpenAEC-BIM-validator', 'commit': COMMIT,
    'url_routes': [
        {'path': '/ en /viewer', 'branch': 'viewer', 'evidence': evidence(app, 'return <AppShell />;')},
        {'path': '/validate', 'branch': 'legacy', 'evidence': evidence(app, 'return <LegacyValidationView />;')},
    ],
    'routes': routes, 'right_tabs': right_tabs, 'overlays': overlays,
    'layout': {
        'left_default_percent': 25, 'left_min_percent': 15,
        'center_min_percent': 30, 'right_default_percent': 25, 'right_min_percent': 15,
        'left_models_default_percent': 35, 'left_properties_percent': 65,
        'left_evidence': evidence(shell, 'const LEFT_PANEL_DEFAULT = "25%";'),
        'right_evidence': evidence(shell, 'const RIGHT_PANEL_DEFAULT = "25%";'),
        'center_evidence': evidence(shell, 'const CENTER_PANEL_MIN = "30%";'),
        'vertical_evidence': evidence(left, 'defaultSize="35%"'),
        'left_properties_evidence': evidence(left, '<PropertiesPanel />'),
        'right_tabs_evidence': evidence(right, 'const TABS:'),
        'viewer_evidence': evidence(center, '<div ref={containerRef} className="viewer-container__canvas" />'),
        'shell_css_evidence': evidence(base + 'components/layout/AppShell.css', 'TitleBar (32px) + Ribbon (122px) + Panels + StatusBar (22px)'),
    },
    'limits': [
        'No runtime UI screenshots were found in the pinned repository; this is a source-grounded schematic, not a pixel diff.',
        'The 3D model, results and backend-dependent dialogs use illustrative data; the actual viewer and validation engine are not ported.',
        'The older /validate route is distinct from the platform validation tab; they must not be counted as one screen.',
    ],
}
out = ROOT / 'harmonization/validator-screen-routes.json'
out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
template = (ROOT / 'design/validator-screen-route-template.html').read_text()
(ROOT / 'design/validator-screen-route-review.html').write_text(
    template.replace('/*VALIDATOR_DATA*/', json.dumps(manifest, ensure_ascii=False).replace('</', '<\\/')))
print(f"BIM Validator: {len(routes)} states, {len(right_tabs)} right tabs, {len(overlays)} overlays, 2 URL branches")
