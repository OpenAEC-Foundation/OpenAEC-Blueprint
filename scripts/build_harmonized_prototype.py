"""Inject the reviewed studio taxonomy into the shared shell design study."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
apps = json.loads((root / "design/app-layouts.json").read_text())
template = (root / "design/harmonized-template.html").read_text()
payload = json.dumps(apps, ensure_ascii=False).replace("</", "<\\/")
(root / "design/harmonized.html").write_text(template.replace("/*APP_DATA*/", payload))
print(f"Generated shared shell for {len(apps)} studios")
