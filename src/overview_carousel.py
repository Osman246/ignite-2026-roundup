"""LinkedIn document carousel for the Ignite 2026 overview (1080x1350, PDF + PNGs).

Type: EB Garamond for headlines (with *italic* accents) and Inter for labels and body,
matching the style of my earlier LinkedIn posts. Fonts are not committed; see README.

Inputs:  data/keynote_moments.json, data/outlook.json, outputs/img/*.jpg, fonts/*.ttf
Outputs: outputs/linkedin_overview_carousel.pdf, outputs/overview_slides/slide_XX.png
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "fonts"
OUT = ROOT / "outputs"
W, H, M = 1080, 1350, 72

PAPER, CARD = (245, 246, 248), (255, 255, 255)
INK, INK2, MUTED, RULE = (15, 19, 24), (74, 81, 96), (123, 130, 144), (221, 225, 231)
BLUE, BLUE_INK, BLUE_LT, WASH = (42, 120, 214), (28, 92, 171), (134, 182, 239), (231, 240, 252)
STAGE, STAGE_INK, STAGE_INK2 = (11, 15, 26), (242, 244, 248), (185, 193, 208)

_cache = {}


def serif(size, italic=False, weight=500):
    key = ("s", size, italic, weight)
    if key not in _cache:
        f = ImageFont.truetype(str(FONTS / f"EBGaramond{'-Italic' if italic else ''}[wght].ttf"), int(size))
        f.set_variation_by_axes([weight])
        _cache[key] = f
    return _cache[key]


def sans(size, weight=400):
    key = ("i", size, weight)
    if key not in _cache:
        f = ImageFont.truetype(str(FONTS / "Inter.ttf"), int(size))
        f.set_variation_by_axes([min(max(size, 14), 32), weight])
        _cache[key] = f
    return _cache[key]


def tracked(d, xy, s, f, fill, tracking=2.5):
    x, y = xy
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill, anchor="ls")
        x += d.textlength(ch, font=f) + tracking


def wrap(d, s, f, maxw):
    lines, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + ([cur] if cur else [])


def para(d, x, y, s, f, fill, maxw, lh):
    for line in wrap(d, s, f, maxw):
        d.text((x, y), line, font=f, fill=fill, anchor="ls"); y += lh
    return y


def headline(d, x, y, markup, size, maxw, ink, accent, lh=1.08):
    """*word* = italic, ^word^ = accent colour (combine as *^word^*). Returns baseline of next line."""
    words, it, col = [], False, False
    for raw in markup.split():
        w = raw
        if w.startswith("*"): it, w = True, w[1:]
        if w.startswith("^"): col, w = True, w[1:]
        end_it = w.endswith("*")
        w = w.rstrip("*")
        end_col = w.endswith("^")
        w = w.rstrip("^")
        words.append((w, it, col))
        if end_col: col = False
        if end_it: it = False
    cx, cy, space = x, y, d.textlength(" ", font=serif(size))
    for w, i, c in words:
        f = serif(size, i, 500 if i else 600)
        wl = d.textlength(w, font=f)
        if cx > x and cx + wl > x + maxw:
            cx, cy = x, cy + size * lh
        d.text((cx, cy), w, font=f, fill=accent if c else ink, anchor="ls")
        cx += wl + space
    return cy + size * lh


def rounded_mask(size, r):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=255)
    return mask


def paste_image(canvas, path, box, crop=(0, 0, 1), radius=18, border=None):
    x, y, w, h = box
    im = Image.open(path).convert("RGB")
    iw, ih = im.size
    x0, y0, f = crop
    im = im.crop((int(x0 * iw), int(y0 * ih), int((x0 + f) * iw), int((y0 + f) * ih)))
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    im = im.crop((l, t, l + w, t + h))
    canvas.paste(im, (x, y), rounded_mask(im.size, radius) if radius else None)
    if border:
        ImageDraw.Draw(canvas).rounded_rectangle([x, y, x + w - 1, y + h - 1], radius, outline=border, width=2)


def chrome(d, n, total, dark=False, source="Image: Microsoft Ignite 2026 keynote demo"):
    ink, muted, rule = (STAGE_INK, STAGE_INK2, (52, 58, 72)) if dark else (INK, MUTED, RULE)
    d.text((M, 78), "Microsoft Ignite 2026", font=sans(21, 650), fill=ink, anchor="ls")
    d.text((W - M, 78), f"{n:02d} / {total:02d}", font=sans(21, 600), fill=muted, anchor="rs")
    d.line([(M, 100), (W - M, 100)], fill=rule, width=2)
    d.line([(M, H - 92), (W - M, H - 92)], fill=rule, width=4)
    d.line([(M, H - 92), (M + (W - 2 * M) * n / total, H - 92)], fill=BLUE_LT if dark else BLUE, width=4)
    if source:
        d.text((M, H - 54), source, font=sans(18, 400), fill=muted, anchor="ls")
    if n < total:
        d.text((W - M, H - 54), "Swipe  →", font=sans(22, 650), fill=ink, anchor="rs")


def kicker(d, y, s, col):
    tracked(d, (M, y), s.upper(), sans(20, 650), col, tracking=2.6)


PRODUCT = {
    "product_copilot_workiq": dict(
        head="Copilot runs the *^Monday sales review^*",
        stat="3 systems, 1 ask", label="Salesforce, Outlook and Teams, with every step shown for you to check.",
        means="The analysis you spend Monday morning assembling arrives as one answer you can verify."),
    "product_autopilot": dict(
        head="Autopilot takes *^standing orders^*",
        stat="Set it once", label="“If a client goes quiet for a week, draft a follow-up for me to approve.”",
        means="Delegation, not assistance. Briefing and supervising an agent becomes part of the job."),
    "product_agent365_analytics": dict(
        head="AI finally gets an *^ROI dashboard^*",
        stat="$38.8K → $100.1K", label="Cost against estimated AI value for one research team (demo data).",
        means="Anyone running an AI rollout will be expected to show numbers like these."),
    "product_foundry_alaska": dict(
        head="A small trained model: *^97% accurate, 227× cheaper^*",
        stat="$370 → $2", label="A month, with accuracy up from 94% to 97%. Alaska Airlines demo, synthetic data.",
        means="On narrow, repeat tasks, a small model trained on your own data beats the giants."),
    "product_admin_agents": dict(
        head="IT gets a *^clean-up crew^* for agents",
        stat="2,600", label="Idle agents in one demo tenant, with rules to notify, block and delete them.",
        means="Anyone can build an agent now. Someone has to track and retire them."),
}


def cover(n, total, m):
    im = Image.new("RGB", (W, H), STAGE); d = ImageDraw.Draw(im)
    paste_image(im, OUT / m["hero"]["img"], (0, 112, W, 608), radius=0)
    chrome(d, n, total, dark=True, source="Image: Microsoft Ignite 2026 keynote")
    kicker(d, 800, "Day 1 · San Francisco · 17 Nov 2026", BLUE_LT)
    y = headline(d, M, 900, "The day Microsoft started selling an *^AI workforce^*", 92, W - 2 * M, STAGE_INK, BLUE_LT, 1.02)
    para(d, M, y + 12, "Five product demos, what they mean, and the one skill to build for 2027.", sans(31, 400), STAGE_INK2, W - 2 * M, 44)
    return im


def product_slide(n, total, it):
    c = PRODUCT[Path(it["img"]).stem]
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    chrome(d, n, total)
    kicker(d, 160, it["product"], BLUE_INK)
    y = headline(d, M, 236, c["head"], 64, W - 2 * M, INK, BLUE_INK, 1.06)
    img_y = int(y - 20)
    paste_image(im, OUT / it["img"], (M, img_y, W - 2 * M, 556), crop=it.get("crop", (0, 0, 1)), border=RULE)
    sy = img_y + 556 + 96
    d.text((M, sy), c["stat"], font=serif(88, False, 600), fill=BLUE_INK, anchor="ls")
    y2 = para(d, M, sy + 52, c["label"], sans(25, 450), INK2, W - 2 * M, 34)
    d.line([(M, y2 + 6), (M + 60, y2 + 6)], fill=BLUE, width=3)
    para(d, M, y2 + 58, c["means"], serif(38, True, 500), INK, W - 2 * M, 46)
    return im


def forces(n, total, o):
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    chrome(d, n, total, source="Analysis: my own, from the Ignite 2026 announcements")
    kicker(d, 160, "The wider picture", BLUE_INK)
    headline(d, M, 246, "Five shifts to plan for in *^2027^*", 76, W - 2 * M, INK, BLUE_INK)
    y = 430
    for i, f in enumerate(o["forces"], 1):
        d.text((M, y + 6), str(i), font=serif(72, True, 500), fill=BLUE, anchor="ls")
        y2 = para(d, M + 80, y - 26, f["title"], sans(29, 650), INK, W - 2 * M - 80, 38)
        line = f["so_what"].split(". ")[0].rstrip(".") + "."
        y2 = para(d, M + 80, y2 + 2, line, sans(22, 400), INK2, W - 2 * M - 80, 31)
        y = y2 + 92
        if i < 5:
            d.line([(M + 80, y - 62), (W - M, y - 62)], fill=RULE, width=1)
    return im


def roles(n, total, o):
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    chrome(d, n, total, source="Analysis: my own, from the Ignite 2026 announcements")
    kicker(d, 160, "Professional relevance", BLUE_INK)
    headline(d, M, 246, "The *^one skill^* to build, by role", 76, W - 2 * M, INK, BLUE_INK)
    cw, ch, gap = (W - 2 * M - 24) // 2, 262, 24
    for i, r in enumerate(o["roles"]):
        x, y = M + (i % 2) * (cw + gap), 340 + (i // 2) * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], 18, fill=CARD, outline=RULE, width=2)
        tracked(d, (x + 28, y + 52), r["role"].upper(), sans(18, 650), MUTED, tracking=2.2)
        para(d, x + 28, y + 104, r["skill"], serif(38, True, 500), BLUE_INK, cw - 56, 44)
    return im


def bottom(n, total, o):
    im = Image.new("RGB", (W, H), STAGE); d = ImageDraw.Draw(im)
    paste_image(im, OUT / "img" / "keynote_nadella.jpg", (0, 112, W, 520), radius=0)
    chrome(d, n, total, dark=True, source="Image: Microsoft Ignite 2026 keynote")
    kicker(d, 712, "The bottom line", BLUE_LT)
    y = headline(d, M, 800, "The question for 2027 isn't *whether* to use AI. It's how much work you hand to agents, and how you prove it's *^worth it.^*",
                 54, W - 2 * M, STAGE_INK, BLUE_LT, 1.12)
    d.rounded_rectangle([M, y + 10, W - M, y + 170], 18, fill=(22, 30, 48))
    d.text((M + 32, y + 70), "Which shift will change your job first?", font=sans(30, 650), fill=STAGE_INK, anchor="ls")
    d.text((M + 32, y + 122), "Tell me in the comments, and save this for 2027 planning.", font=sans(24, 400), fill=STAGE_INK2, anchor="ls")
    return im


def main():
    m = json.loads((ROOT / "data" / "keynote_moments.json").read_text())
    o = json.loads((ROOT / "data" / "outlook.json").read_text())
    by = {Path(i["img"]).stem: i for i in m["items"]}
    order = ["product_copilot_workiq", "product_autopilot", "product_agent365_analytics", "product_foundry_alaska", "product_admin_agents"]
    total = 1 + len(order) + 3
    slides = [cover(1, total, m)]
    slides += [product_slide(i + 2, total, by[k]) for i, k in enumerate(order)]
    slides += [forces(total - 2, total, o), roles(total - 1, total, o), bottom(total, total, o)]
    d = OUT / "overview_slides"; d.mkdir(parents=True, exist_ok=True)
    for p in d.glob("slide_*.png"):
        p.unlink()
    for i, s in enumerate(slides, 1):
        s.save(d / f"slide_{i:02d}.png")
    slides[0].save(OUT / "linkedin_overview_carousel.pdf", save_all=True, append_images=slides[1:], resolution=150)
    print("wrote", len(slides), "slides")


if __name__ == "__main__":
    main()
