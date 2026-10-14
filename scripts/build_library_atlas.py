"""Render the pinned imported-icon research archive for visual comparison."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / "harmonization/library-icon-index.json").read_text())
template = (root / "design/library-icons-template.html").read_text()
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
(root / "design/library-icons.html").write_text(template.replace("/*ICON_DATA*/", payload))
print(f"Built imported icon atlas: {data['downloaded']} SVGs")
