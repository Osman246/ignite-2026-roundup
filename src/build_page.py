"""Inject the announcement dataset and summary into the roundup page template.

Inputs:  data/announcements.json, outputs/summary.json, src/page_template.html
Output:  outputs/roundup.html
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    data = json.loads((ROOT / "data" / "announcements.json").read_text())
    data["summary"] = json.loads((ROOT / "outputs" / "summary.json").read_text())
    tpl = (ROOT / "src" / "page_template.html").read_text()
    out = ROOT / "outputs" / "roundup.html"
    out.write_text(tpl.replace("/*__DATA__*/null", json.dumps(data)))
    print("wrote", out)


if __name__ == "__main__":
    main()
