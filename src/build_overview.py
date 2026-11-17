"""Build the Ignite 2026 visual overview page.

Inputs:  data/announcements.json, data/outlook.json, data/keynote_moments.json,
         outputs/summary.json, outputs/img/keynote_*.jpg (stills from Microsoft's keynote replay)
Output:  outputs/overview.html
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    d = {
        "ann": json.loads((ROOT / "data" / "announcements.json").read_text()),
        "outlook": json.loads((ROOT / "data" / "outlook.json").read_text()),
        "moments": json.loads((ROOT / "data" / "keynote_moments.json").read_text()),
        "summary": json.loads((ROOT / "outputs" / "summary.json").read_text()),
    }
    tpl = (ROOT / "src" / "overview_template.html").read_text()
    out = ROOT / "outputs" / "overview.html"
    out.write_text(tpl.replace("/*__DATA__*/null", json.dumps(d)))
    print("wrote", out)


if __name__ == "__main__":
    main()
