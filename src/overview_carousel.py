"""LinkedIn document carousel for the Ignite 2026 overview, built around keynote stills.

Inputs:  data/keynote_moments.json, data/outlook.json, outputs/img/*.jpg
Outputs: outputs/linkedin_overview_carousel.pdf, outputs/overview_slides/slide_XX.png (1080x1350)
"""
import json
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
STAGE, STAGE_INK, STAGE_INK2 = "#0b0f1a", "#f2f4f8", "#b9c1d0"
BG, INK, INK2, MUTED, BLUE, BLUE_LT, WASH = "#f5f6f8", "#0f1318", "#4a5160", "#7b8290", "#2a78d6", "#86b6ef", "#e7f0fc"
W, H = 10.8, 13.5
plt.rcParams.update({"font.family": "DejaVu Sans"})
wrap = lambda t, w: "\n".join(textwrap.wrap(t, w))
CREDIT = "Image: Microsoft Ignite 2026 keynote"


def page(n, total, dark=False):
    bg = STAGE if dark else BG
    fig = plt.figure(figsize=(W, H), dpi=100, facecolor=bg)
    fig.text(0.07, 0.955, "MICROSOFT IGNITE 2026  ·  OVERVIEW", fontsize=13, color=BLUE_LT if dark else "#1c5cab", fontweight="bold")
    fig.text(0.93, 0.955, f"{n}/{total}", fontsize=13, color=MUTED, ha="right")
    fig.add_artist(plt.Line2D([0.07, 0.93], [0.94, 0.94], color=STAGE_INK if dark else INK, lw=2))
    return fig, bg


def image(fig, path, y, h=0.36):
    ax = fig.add_axes([0.07, y, 0.86, h]); ax.imshow(mpimg.imread(path)); ax.axis("off")
    fig.text(0.07, y - 0.018, CREDIT, fontsize=10.5, color=MUTED)


def cover(fig, m):
    image(fig, ROOT / "outputs" / m["hero"]["img"], 0.50)
    fig.text(0.07, 0.43, "The day Microsoft started\nselling an AI workforce", fontsize=44, fontweight="bold", color=STAGE_INK, va="top", linespacing=1.1)
    fig.text(0.07, 0.25, "What was announced, what it means,\nand how it changes work in 2027.", fontsize=22, color=STAGE_INK2, va="top", linespacing=1.4)
    fig.text(0.93, 0.07, "Swipe  →", fontsize=20, color=STAGE_INK, fontweight="bold", ha="right")


def moment(fig, it, k):
    im = mpimg.imread(ROOT / "outputs" / it["img"]); h, w = im.shape[:2]
    x0, y0, f = it.get("crop", [0, 0, 1])
    im = im[int(y0 * h):int((y0 + f) * h), int(x0 * w):int((x0 + f) * w)]
    ax = fig.add_axes([0.0, 0.487, 1.0, 0.45]); ax.imshow(im, aspect="auto"); ax.axis("off")
    fig.text(0.07, 0.472, CREDIT + " · demo screen", fontsize=10.5, color=MUTED)
    fig.text(0.07, 0.448, it.get("product", f"KEY MOMENT {k}").upper(), fontsize=14, color="#1c5cab", fontweight="bold", va="top")
    fig.text(0.07, 0.418, wrap(it["title"], 30), fontsize=32, fontweight="bold", color=INK, va="top", linespacing=1.15)
    lines = len(textwrap.wrap(it["title"], 30))
    ax = fig.add_axes([0.05, 0.06, 0.90, 0.30 - 0.05 * (lines - 1)]); ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=WASH, transform=ax.transAxes))
    top = 0.36 - 0.05 * (lines - 1)
    fig.text(0.09, top - 0.025, "WHAT IT MEANS", fontsize=12.5, color="#1c5cab", fontweight="bold", va="top")
    first_two = ". ".join(it["means"].split(". ")[:2]).rstrip(".") + "."
    fig.text(0.09, top - 0.06, wrap(first_two, 50), fontsize=18, color=INK, va="top", linespacing=1.45)


def forces(fig, o):
    fig.text(0.07, 0.885, "The wider picture", fontsize=20, color="#1c5cab", fontweight="bold", va="top")
    fig.text(0.07, 0.845, "Five forces shaping\nwork in 2027", fontsize=40, fontweight="bold", color=INK, va="top", linespacing=1.12)
    for i, f in enumerate(o["forces"]):
        y = 0.68 - i * 0.128
        fig.text(0.07, y, str(i + 1), fontsize=34, fontweight="bold", color=BLUE, va="top")
        fig.text(0.15, y, wrap(f["title"], 38), fontsize=20, fontweight="bold", color=INK, va="top", linespacing=1.2)
        n = len(textwrap.wrap(f["title"], 38))
        fig.text(0.15, y - 0.027 * n - 0.008, wrap(f["so_what"].split(". ")[0].rstrip(".") + ".", 60), fontsize=13.5, color=INK2, va="top", linespacing=1.35)


def roles(fig, o):
    fig.text(0.07, 0.885, "Professional relevance", fontsize=20, color="#1c5cab", fontweight="bold", va="top")
    fig.text(0.07, 0.845, "The skill to build,\nby role", fontsize=40, fontweight="bold", color=INK, va="top", linespacing=1.12)
    for i, r in enumerate(o["roles"]):
        col, row = i % 2, i // 2
        x, y = 0.07 + col * 0.44, 0.62 - row * 0.19
        ax = fig.add_axes([x, y - 0.13, 0.42, 0.16]); ax.axis("off")
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, color="white", transform=ax.transAxes))
        fig.text(x + 0.025, y + 0.015, r["role"], fontsize=17, fontweight="bold", color=INK, va="top")
        fig.text(x + 0.025, y - 0.03, wrap(r["skill"], 30), fontsize=14.5, color="#1c5cab", va="top", linespacing=1.35)


def bottom(fig, o, m):
    ax = fig.add_axes([0.07, 0.55, 0.86, 0.33]); ax.imshow(mpimg.imread(ROOT / "outputs" / "img" / "keynote_nadella.jpg")); ax.axis("off")
    fig.text(0.07, 0.535, CREDIT, fontsize=10.5, color=MUTED)
    fig.text(0.07, 0.48, "The bottom line", fontsize=18, color=BLUE_LT, fontweight="bold", va="top")
    fig.text(0.07, 0.44, wrap(o["bottom_line"], 38), fontsize=25, color=STAGE_INK, fontweight="bold", va="top", linespacing=1.3)
    fig.text(0.07, 0.15, "Which shift will change your job first?\nFull overview + open data: link in the comments.", fontsize=18, color=STAGE_INK2, va="top", linespacing=1.5)


def main():
    m = json.loads((ROOT / "data" / "keynote_moments.json").read_text())
    o = json.loads((ROOT / "data" / "outlook.json").read_text())
    picks = [m["items"][i] for i in (0, 1, 4, 6, 5)]
    plan = [("dark", lambda f: cover(f, m))] + [("light", (lambda f, it=it, k=k: moment(f, it, k))) for k, it in enumerate(picks, 1)] + \
           [("light", lambda f: forces(f, o)), ("light", lambda f: roles(f, o)), ("dark", lambda f: bottom(f, o, m))]
    d = OUT / "overview_slides"; d.mkdir(parents=True, exist_ok=True)
    with PdfPages(OUT / "linkedin_overview_carousel.pdf") as pdf:
        for n, (mode, b) in enumerate(plan, 1):
            fig, bg = page(n, len(plan), dark=mode == "dark"); b(fig)
            pdf.savefig(fig, facecolor=bg); fig.savefig(d / f"slide_{n:02d}.png", facecolor=bg); plt.close(fig)
    print("wrote", len(plan), "slides")


if __name__ == "__main__":
    main()
