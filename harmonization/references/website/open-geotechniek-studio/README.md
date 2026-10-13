# Open Geotechniek Studio — Screenshots

Take 10 screenshots covering:

1. Welcome / empty state
2. Single CPT chart with hover (tooltip + Robertson zone highlighted)
3. Multi-CPT side-by-side with NAP alignment (3+ sonderingen)
4. Project browser (LeftPanel) with multiple CPTs visible
5. Map view with BRO sonderingen + project sonderingen + distance lines
6. Topotijdreis slider showing 1900 vs 2024 (split or two screenshots)
7. Rapport preview with sidebar (section toggles visible)
8. PDF page (cover) close-up
9. PDF page (chart page) close-up
10. Sonderingstekening view with drawing frame loaded and markers placed

Save as PNG, 1920x1080 or higher. Filenames:

- `01-welcome.png`
- `02-chart.png`
- `03-multi-cpt.png`
- `04-project-browser.png`
- `05-map-bro.png`
- `06a-topo-1900.png`
- `06b-topo-2024.png`
- `07-rapport-preview.png`
- `08-pdf-cover.png`
- `09-pdf-chart.png`
- `10-sonderingstekening.png`

The user takes these screenshots manually — they cannot be automated from a coding session (the agent has no display of its own and Tauri's window can't be reached programmatically without a running dev server). Run `npm run tauri dev` from `apps/desktop/`, set up the demo scenarios, and capture with the OS screenshot tool of choice (Snipping Tool, ShareX, Cmd-Shift-4, Flameshot, …).

## Supporting copy

- `linkedin.md` — Dutch LinkedIn post (200-300 words) ready for posting.
- `video-script.md` — Scene-by-scene script for a 60-90s screen recording.
