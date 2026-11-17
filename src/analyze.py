"""Turn the curated Ignite 2026 announcement list into a tidy dataset, summary stats and charts.

Input:   data/announcements.json   (hand-curated from Microsoft's Book of News and keynote coverage)
Outputs: data/announcements.csv, outputs/summary.json, outputs/charts/*.png
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"

STATUS = ["now", "preview", "early", "announced"]
STATUS_LABEL = {"now": "Available now", "preview": "Preview", "early": "Early access", "announced": "Announced / coming"}
# One-hue ordinal ramp: darker = closer to available.
STATUS_COLOR = {"now": "#1c5cab", "preview": "#3987e5", "early": "#86b6ef", "announced": "#c4d7ef"}
WHO_LABEL = {"everyone": "Everyone at work", "leaders": "Business leaders", "it": "IT & security",
             "dev": "Developers", "data": "Data & analytics"}
BG, INK, INK2, MUTED, GRID = "#f6f7f9", "#101418", "#4b5260", "#7c8391", "#e3e6eb"


def load():
    raw = json.loads((ROOT / "data" / "announcements.json").read_text())
    df = pd.DataFrame(raw["items"])
    df["top"] = df.get("top", False).fillna(False).astype(bool)
    flat = df.assign(who=df.who.map(lambda w: ";".join(w)))
    flat[["name", "cat", "status", "label", "who", "top", "what"]].to_csv(ROOT / "data" / "announcements.csv", index=False)
    return raw, df


def summarize(df):
    by_status = df.status.value_counts().reindex(STATUS, fill_value=0)
    by_cat = pd.crosstab(df.cat, df.status).reindex(columns=STATUS, fill_value=0)
    by_cat = by_cat.loc[by_cat.sum(axis=1).sort_values(ascending=False).index]
    who = df.explode("who").groupby("who").agg(total=("name", "size"), now=("status", lambda s: (s == "now").sum()))
    who = who.sort_values("total", ascending=False)
    s = {
        "total": int(len(df)),
        "by_status": {k: int(v) for k, v in by_status.items()},
        "share_available_now": round(by_status["now"] / len(df), 3),
        "by_category": {c: {k: int(v) for k, v in r.items()} for c, r in by_cat.iterrows()},
        "by_audience": {w: {"total": int(r.total), "now": int(r.now)} for w, r in who.iterrows()},
    }
    (OUT / "summary.json").write_text(json.dumps(s, indent=2))
    return s, by_cat, who


def style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK, "figure.facecolor": BG,
                         "axes.facecolor": BG, "savefig.facecolor": BG})


def header(fig, title, sub):
    fig.text(0.07, 0.94, title, fontsize=30, fontweight="bold", va="top", linespacing=1.15)
    fig.text(0.07, 0.80, sub, fontsize=16, color=INK2, va="top")
    fig.text(0.07, 0.035, "Data: Microsoft Ignite 2026 Book of News and keynote coverage, 17 Nov 2026. Curated dataset in this repo.",
             fontsize=11, color=MUTED)


def chart_categories(by_cat, s):
    fig = plt.figure(figsize=(10.8, 10.8), dpi=100)
    header(fig, f"Of {s['total']} headline announcements,\nonly {s['by_status']['now']} are available today",
           "Ignite 2026 announcements by area and availability")
    ax = fig.add_axes([0.30, 0.20, 0.62, 0.52])
    left = pd.Series(0, index=by_cat.index)
    y = range(len(by_cat))
    for st in STATUS:
        v = by_cat[st]
        ax.barh(list(y), v, left=left, color=STATUS_COLOR[st], height=0.62, edgecolor=BG, linewidth=2,
                label=STATUS_LABEL[st])
        left += v
    for i, (c, tot) in enumerate(by_cat.sum(axis=1).items()):
        ax.text(tot + 0.15, i, str(tot), va="center", fontsize=16, fontweight="bold")
    ax.set_yticks(list(y)); ax.set_yticklabels(by_cat.index, fontsize=16, color=INK)
    ax.invert_yaxis(); ax.set_xticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.tick_params(length=0)
    ax.legend(loc="upper center", bbox_to_anchor=(0.32, -0.04), ncol=2, frameon=False, fontsize=14)
    fig.savefig(OUT / "charts" / "1_announcements_by_area.png")
    plt.close(fig)


def chart_audience(who):
    fig = plt.figure(figsize=(10.8, 10.8), dpi=100)
    header(fig, "Who got the most\nfrom Day 1?", "Announcements relevant to each group (one announcement can serve several)")
    ax = fig.add_axes([0.30, 0.16, 0.62, 0.56])
    y = list(range(len(who)))
    ax.barh(y, who.total, color="#c4d7ef", height=0.6, label="Announced")
    ax.barh(y, who.now, color="#1c5cab", height=0.6, label="Available now")
    for i, (w, r) in enumerate(who.iterrows()):
        ax.text(r.total + 0.2, i, f"{r.total}", va="center", fontsize=17, fontweight="bold")
        if r.now >= 2: ax.text(r.now - 0.2, i, f"{r.now} now", va="center", ha="right", fontsize=12, color="white", fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels([WHO_LABEL[w] for w in who.index], fontsize=17)
    ax.invert_yaxis(); ax.set_xticks([])
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.tick_params(length=0)
    ax.legend(loc="upper center", bbox_to_anchor=(0.3, -0.02), ncol=2, frameon=False, fontsize=14)
    fig.savefig(OUT / "charts" / "2_who_benefits.png")
    plt.close(fig)


if __name__ == "__main__":
    (OUT / "charts").mkdir(parents=True, exist_ok=True)
    style()
    raw, df = load()
    s, by_cat, who = summarize(df)
    chart_categories(by_cat, s)
    chart_audience(who)
    print(json.dumps(s, indent=2))
