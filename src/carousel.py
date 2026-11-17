"""Render the LinkedIn document carousel for the Ignite 2026 roundup (PDF + PNG per slide, 1080x1350).

Inputs:  data/announcements.json, outputs/summary.json
Outputs: outputs/linkedin_carousel.pdf, outputs/slides/slide_XX.png
"""
import json
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
BG, CARD, INK, INK2, MUTED, RULE = "#f4f5f7", "#ffffff", "#0f1318", "#4a5160", "#7b8290", "#dde1e7"
BLUE, BLUE_INK, WASH = "#2a78d6", "#1c5cab", "#e7f0fc"
ST = {"now": ("AVAILABLE NOW", "#1c5cab"), "preview": ("PREVIEW", "#3987e5"),
      "early": ("EARLY ACCESS", "#86b6ef"), "announced": ("COMING", "#c4d7ef")}
W, H = 10.8, 13.5
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK})
SHORT = [
    "Word, Excel and PowerPoint open inside it. Directing agents becomes the key work skill.",
    "Its own models (MAI) and chips (Maia 300, Cobalt 200), alongside OpenAI and Meta models. More choice, lower costs.",
    "Identities, budgets, performance reviews and security cover. Managing agents becomes a management skill.",
    "Salesforce runs inside Copilot, Fabric data works in ChatGPT and Claude, and there are 350+ connectors.",
    "Open transparency standards, tighter Copilot data controls and a public admission about last week's outage.",
]
wrap = lambda t, w: "\n".join(textwrap.wrap(t, w))


def page(n, total):
    fig = plt.figure(figsize=(W, H), dpi=100, facecolor=BG)
    fig.text(0.07, 0.955, "MICROSOFT IGNITE 2026  ·  ROUNDUP SO FAR", fontsize=13, color=BLUE_INK, fontweight="bold")
    fig.text(0.93, 0.955, f"{n}/{total}", fontsize=13, color=MUTED, ha="right")
    fig.add_artist(plt.Line2D([0.07, 0.93], [0.94, 0.94], color=INK, lw=2))
    return fig


def card(fig, x, y, w, h, color=CARD, edge=RULE):
    fig.add_artist(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.012",
                                  transform=fig.transFigure, fc=color, ec=edge, lw=1.2))


def title(fig, kicker, text, size=40):
    fig.text(0.07, 0.885, kicker, fontsize=20, color=BLUE_INK, fontweight="bold", va="top")
    fig.text(0.07, 0.845, text, fontsize=size, fontweight="bold", va="top", linespacing=1.12)


def cover(fig, d):
    fig.text(0.07, 0.83, "Copilot is the new\noperating system\nfor work.", fontsize=58, fontweight="bold", va="top", linespacing=1.08)
    fig.text(0.07, 0.50, "Everything Microsoft announced at\nIgnite 2026 so far, in 2 minutes.", fontsize=28, color=BLUE_INK, fontweight="bold", va="top", linespacing=1.3)
    fig.text(0.07, 0.35, "✓  The best announcements\n✓  What you can use today\n✓  What it means for 2027", fontsize=22, color=INK2, va="top", linespacing=1.7)
    fig.text(0.07, 0.07, "Sources: Microsoft Ignite 2026 Book of News and keynote coverage, 17 Nov 2026", fontsize=12, color=MUTED)
    fig.text(0.93, 0.07, "Swipe  →", fontsize=20, fontweight="bold", ha="right")


def tldr(fig, d):
    title(fig, "The 30-second version", "Day 1 in four lines")
    rows = [("Copilot takes centre stage", "Word, Excel and PowerPoint now open inside Copilot, with agents that work on tasks for you."),
            ("Agents get managed", "Agents get their own identities, budgets and performance tracking."),
            ("Microsoft's own AI", "New MAI models for code, security and images, plus the Maia 300 chip."),
            ("Security first", "Security agents that handle about 80% of a typical alert queue.")]
    for i, (h, b) in enumerate(rows):
        y = 0.62 - i * 0.145
        card(fig, 0.07, y - 0.035, 0.86, 0.125)
        fig.text(0.10, y + 0.06, h, fontsize=23, fontweight="bold", va="top")
        fig.text(0.10, y + 0.017, wrap(b, 58), fontsize=17, color=INK2, va="top", linespacing=1.4)


def numbers(fig, d):
    title(fig, "By the numbers", "Day 1 in six numbers")
    for i, (n, label, src) in enumerate(d["numbers"]):
        col, row = i % 2, i // 2
        x, y = 0.07 + col * 0.44, 0.60 - row * 0.20
        card(fig, x, y - 0.02, 0.42, 0.18)
        fig.text(x + 0.03, y + 0.12, n, fontsize=34, fontweight="bold", color=BLUE_INK, va="top")
        fig.text(x + 0.03, y + 0.065, wrap(label, 28), fontsize=15, color=INK, va="top", linespacing=1.35)
        fig.text(x + 0.39, y + 0.135, src.replace(", per press coverage", ""), fontsize=10, color=MUTED, va="top", ha="right")


def best(fig, d):
    title(fig, "Best of Day 1", "Six worth getting\nexcited about")
    tops = [i for i in d["items"] if i.get("top")]
    for k, it in enumerate(tops):
        col, row = k % 2, k // 2
        x, y = 0.07 + col * 0.44, 0.52 - row * 0.17
        card(fig, x, y - 0.03, 0.42, 0.15)
        fig.text(x + 0.03, y + 0.10, str(k + 1), fontsize=26, fontweight="bold", color=BLUE, va="top")
        fig.text(x + 0.09, y + 0.10, wrap(it["name"], 22), fontsize=17, fontweight="bold", va="top", linespacing=1.2)
        lab, c = ST[it["status"]]
        fig.text(x + 0.09, y - 0.005, lab, fontsize=11, color=INK, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.4", fc=BG, ec=c, lw=1.5))


def data_slide(fig, d, s):
    title(fig, "The reality check", f"{s['by_status']['now']} of {s['total']} headline\nannouncements are\navailable today")
    ax = fig.add_axes([0.07, 0.36, 0.86, 0.10]); ax.axis("off")
    left = 0
    for k in ["now", "preview", "early", "announced"]:
        v = s["by_status"][k]
        ax.barh(0, v, left=left, color=ST[k][1], height=0.8, edgecolor=BG, linewidth=3)
        ax.text(left + v / 2, 0, str(v), ha="center", va="center", fontsize=24, fontweight="bold",
                color="white" if k in ("now", "preview") else INK)
        left += v
    ax.set_xlim(0, s["total"]); ax.set_ylim(-0.6, 0.6)
    for i, k in enumerate(["now", "preview", "early", "announced"]):
        x = 0.07 + i * 0.215
        fig.add_artist(plt.Rectangle((x, 0.315), 0.02, 0.016, color=ST[k][1], transform=fig.transFigure))
        fig.text(x + 0.03, 0.323, ST[k][0].title(), fontsize=14, color=INK2, va="center")
    dv, ev = s["by_audience"]["dev"], s["by_audience"]["everyone"]
    fig.text(0.07, 0.25, f"Developers did best: {dv['now']} of {dv['total']} live now.\nEveryday workers: {ev['now']} of {ev['total']}.",
             fontsize=22, fontweight="bold", va="top", linespacing=1.4)
    fig.text(0.07, 0.14, "The biggest Copilot features arrive over the coming\nmonths, not this week.", fontsize=18, color=INK2, va="top", linespacing=1.4)
    fig.text(0.07, 0.05, "My count of Day 1 headline announcements, using Microsoft's availability labels.", fontsize=12, color=MUTED)


def takes(fig, d, part):
    sl = d["takeaways"][:3] if part == 1 else d["takeaways"][3:]
    start = 1 if part == 1 else 4
    title(fig, "What it means going forward", "Five shifts to plan for\nin 2027" + (" (1/2)" if part == 1 else " (2/2)"), size=36)
    for i, t in enumerate(sl):
        y = 0.64 - i * 0.20
        fig.text(0.07, y, str(start + i), fontsize=40, fontweight="bold", color=BLUE, va="top")
        fig.text(0.16, y, wrap(t["title"], 34), fontsize=22, fontweight="bold", va="top", linespacing=1.2)
        lines = len(textwrap.wrap(t["title"], 34))
        fig.text(0.16, y - 0.034 * lines - 0.008, wrap(SHORT[start + i - 1], 48), fontsize=17, color=INK2, va="top", linespacing=1.4)


def watch(fig, d):
    title(fig, "What to watch next", "Coming up")
    for i, w in enumerate(d["watch"]):
        y = 0.66 - i * 0.13
        fig.text(0.07, y, "→", fontsize=24, color=BLUE, fontweight="bold", va="top")
        fig.text(0.13, y, wrap(w, 48), fontsize=19, va="top", linespacing=1.4)


def cta(fig, d):
    fig.text(0.07, 0.80, "Which one would\nchange your week\nthe most?", fontsize=54, fontweight="bold", va="top", linespacing=1.1)
    fig.text(0.07, 0.45, "Tell me in the comments.", fontsize=26, color=BLUE_INK, fontweight="bold")
    fig.text(0.07, 0.36, "Full interactive roundup, filterable by your role,\nplus the open dataset and code: link in the comments.",
             fontsize=19, color=INK2, va="top", linespacing=1.5)
    fig.text(0.07, 0.07, "Follow for the Day 2 to Day 4 updates.", fontsize=16, color=INK, fontweight="bold")


def main():
    d = json.loads((ROOT / "data" / "announcements.json").read_text())
    s = json.loads((OUT / "summary.json").read_text())
    builders = [lambda f: cover(f, d), lambda f: tldr(f, d), lambda f: numbers(f, d), lambda f: best(f, d),
                lambda f: data_slide(f, d, s), lambda f: takes(f, d, 1), lambda f: takes(f, d, 2),
                lambda f: watch(f, d), lambda f: cta(f, d)]
    (OUT / "slides").mkdir(parents=True, exist_ok=True)
    with PdfPages(OUT / "linkedin_carousel.pdf") as pdf:
        for n, b in enumerate(builders, 1):
            fig = page(n, len(builders)); b(fig)
            pdf.savefig(fig, facecolor=BG); fig.savefig(OUT / "slides" / f"slide_{n:02d}.png", facecolor=BG)
            plt.close(fig)
    print("wrote", len(builders), "slides")


if __name__ == "__main__":
    main()
