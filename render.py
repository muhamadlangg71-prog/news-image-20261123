#!/usr/bin/env python3
"""Render the 23 November 2026 world-news image (1024x1024 PNG).

Editorial front-page layout drawn with PIL + Liberation fonts:
masthead with the date, one lead story (Hormuz tanker strikes),
four secondary cards, one full-width climate strip and a Monday
markets ticker.
All facts verified from CNN / Reuters / AP / Al Jazeera / AFP on 23 Nov 2026.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (245, 241, 232)      # warm paper
NAVY = (16, 38, 63)
NAVY_DARK = (10, 26, 44)
INK = (24, 24, 24)
GREY = (74, 74, 74)
WHITE = (255, 255, 255)
GOLD = (232, 196, 106)
TEAL = (14, 122, 95)
RED = (178, 34, 34)
ORANGE = (198, 93, 0)
GREEN = (31, 122, 52)
PURPLE = (106, 62, 150)
BLUE = (24, 90, 160)
MUTED = (159, 179, 200)

FONT_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text, color):
    f = font(FONT_B, 20)
    draw.text((x, y), text, font=f, fill=color)
    return y + 28


def card(draw, x, y, w, h, accent, tag, headline, deck, hl_size=34):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE)
    draw.rectangle([x, y, x + w, y + 5], fill=accent)
    px, py = x + 18, y + 16
    py = kicker(draw, px, py, tag, accent)
    hf = font(FONT_B, hl_size)
    lines = wrap(draw, headline, hf, w - 36)
    py = draw_lines(draw, lines, px, py, hf, NAVY, hl_size + 7)
    df = font(FONT_R, 26)
    dlines = wrap(draw, deck, df, w - 36)
    draw_lines(draw, dlines, px, py + 4, df, GREY, 32)


def tanker(draw, cx, cy, color):
    """Stylised line-art oil tanker with waves, centred on (cx, cy)."""
    # hull
    draw.polygon([(cx - 78, cy - 8), (cx + 78, cy - 8), (cx + 62, cy + 22),
                  (cx - 62, cy + 22)], outline=color, width=5)
    # deck + bridge tower + funnel
    draw.line([cx - 78, cy - 8, cx + 78, cy - 8], fill=color, width=5)
    draw.rectangle([cx + 34, cy - 44, cx + 66, cy - 8], outline=color, width=4)
    draw.rectangle([cx - 58, cy - 30, cx - 42, cy - 8], outline=color, width=4)
    draw.line([cx - 30, cy - 8, cx - 30, cy - 26], fill=color, width=4)
    # waves
    for dy, x0, x1 in ((44, cx - 84, cx - 20), (44, cx - 4, cx + 84),
                       (62, cx - 70, cx + 10), (62, cx + 26, cx + 78)):
        draw.arc([x0, cy + dy - 10, x1, cy + dy + 10], start=200, end=340,
                 fill=color, width=4)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 100], fill=NAVY_DARK)
    d.text((28, 16), "MONDAY, 23 NOVEMBER 2026", font=font(FONT_B, 46), fill=WHITE)
    d.text((28, 66), "T H E   W O R L D   I N   O N E   I M A G E",
           font=font(FONT_B, 20), fill=GOLD)
    d.text((W - 28, 68), "SIX STORIES — ONE DAY", font=font(FONT_B, 20),
           fill=MUTED, anchor="ra")

    # ---- Lead: Hormuz tanker strikes ------------------------------------
    lx, ly, lw, lh = 28, 116, 968, 288
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=WHITE)
    d.rectangle([lx, ly, lx + lw, ly + 6], fill=RED)
    tx = lx + 28
    ty = ly + 20
    ty = kicker(d, tx, ty, "IRAN WAR  •  STRAIT OF HORMUZ", RED)
    hf = font(FONT_B, 64)
    lines = wrap(d, "HORMUZ UNDER FIRE", hf, 640)
    ty = draw_lines(d, lines, tx, ty, hf, NAVY, 72)
    df = font(FONT_R, 26)
    dlines = wrap(d, "Three tankers hit in two days as attacks reach their "
                     "highest level since the US–Iran war began. Bahrain "
                     "takes its case to the UN.",
                  df, 640)
    draw_lines(d, dlines, tx, ty + 6, df, GREY, 32)
    tanker(d, 872, ly + 150, RED)

    # ---- Secondary grid -------------------------------------------------
    col_w, row_h = 472, 190
    card(d, 28, 420, col_w, row_h, BLUE, "WAR IN UKRAINE  •  LIBYA",
         "Russian warship sinks off Libya",
         "Merkury capsized after a suspected Ukrainian sea-drone strike.")
    card(d, 524, 420, col_w, row_h, PURPLE, "USA  •  MIDTERMS",
         "Democrats hit 258 — biggest majority since 1992",
         "Hubbard beats Foxx by 330 votes in North Carolina.", hl_size=30)
    card(d, 28, 626, col_w, row_h, ORANGE, "MARKETS  •  SEOUL",
         "AI sell-off spreads: Kospi sinks 2.8% at open",
         "Kospi down 46.6% from its June peak; Seoul readies a rescue fund.")
    card(d, 524, 626, col_w, row_h, TEAL, "HEALTH  •  DR CONGO",
         "WHO pleads for peace as Ebola fight is disrupted",
         "Fighting near a hospital puts patients at grave risk.")

    # ---- Climate strip --------------------------------------------------
    sx, sy, sw, sh = 28, 832, 968, 96
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=WHITE)
    d.rectangle([sx, sy, sx + sw, sy + 5], fill=GREEN)
    kicker(d, sx + 18, sy + 14, "CLIMATE  •  ANTALYA AFTERMATH", GREEN)
    d.text((sx + 18, sy + 46),
           "COP31 collapses without a deal",
           font=font(FONT_B, 30), fill=NAVY)
    d.text((sx + sw - 18, sy + 18), "194", font=font(FONT_B, 46),
           fill=GREEN, anchor="ra")
    d.text((sx + sw - 18, sy + 66), "nations, no deal", font=font(FONT_R, 18),
           fill=GREY, anchor="ra")

    # ---- Markets ticker + sources ---------------------------------------
    d.rectangle([0, 944, W, H], fill=NAVY_DARK)
    d.text((28, 956), "MONDAY MARKETS  •  Kospi −2.8% — S&P 500 in correction, "
                      "Nasdaq 100 in bear market",
           font=font(FONT_B, 23), fill=WHITE)
    d.text((28, 988), "Sources: CNN, Reuters, AP, Al Jazeera, AFP  •  23 November 2026",
           font=font(FONT_R, 17), fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
