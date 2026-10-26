# Componentspecificaties

Per component één bestand `<component>.md` met: opbouw, maten en kleuren als
tokens, toestanden (normaal, hover, actief, uitgeschakeld, focus),
toetsenbordgedrag en labels. De iced-implementatie (`openaec-ui`) en de
React-implementatie (`packages/`) volgen beide exact deze specificatie.

Vertrekpunt: `project-templates/Tauri+React/COMPONENT-MANIFEST.md`.

Versie 1 (specificaties worden geschreven in fase 1a/1b, per component vóór de bouw):

| Groep | Componenten |
|---|---|
| Schil | TitleBar, Ribbon, Backstage, DocumentTabs, StatusBar, zijpanelen, Startscherm |
| Basis | Button, IconButton, Input, Select/Combo, Checkbox/Toggle, Dialog, Tooltip, Contextmenu, Toast |
| Data | Table/DataGrid, Tree, PropertyGrid |
| Viewer | NavigationCube |
