#!/usr/bin/env python3
"""Draw the one-image front page for 23 November 2026.

A single 1024x1024 newspaper-style sheet: a navy masthead, the
Hormuz tanker story as the lead, four smaller story panels, a
climate strip about COP31, and a markets ticker along the bottom.

Every headline and figure comes from reporting published on
23 November 2026 (CNN, Reuters, AP, Al Jazeera, AFP). The sheet is
drawn entirely with Pillow and the Liberation Sans family; running
this file writes entry.png next to it.
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
PAPER = (245, 241, 232)
DEEP_NAVY = (10, 26, 44)
NAVY = (16, 38, 63)
INK = (24, 24, 24)
SMOKE = (74, 74, 74)
SNOW = (255, 255, 255)
GILT = (232, 196, 106)
TEAL = (14, 122, 95)
CRIMSON = (178, 34, 34)
EMBER = (198, 93, 0)
LEAF = (31, 122, 52)
GRAPE = (106, 62, 150)
OCEAN = (24, 90, 160)
MIST = (159, 179, 200)

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(canvas, text, face, width):
    """Split text into the fewest lines that each fit inside width."""
    words = text.split()
    fitted = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if canvas.textlength(candidate, font=face) <= width:
            current = candidate
        else:
            if current:
                fitted.append(current)
            current = word
    if current:
        fitted.append(current)
    return fitted


def paint_lines(canvas, lines, x, y, face, colour, step):
    """Paint lines top to bottom, stepping down after each one."""
    for line in lines:
        canvas.text((x, y), line, font=face, fill=colour)
        y += step
    return y


def section_tag(canvas, x, y, text, colour):
    canvas.text((x, y), text, font=load_font(BOLD, 20), fill=colour)
    return y + 28


def story_card(canvas, x, y, w, h, accent, tag, headline, deck, head_size=34):
    canvas.rectangle([x, y, x + w, y + h], fill=SNOW)
    canvas.rectangle([x, y, x + w, y + 5], fill=accent)
    inner_x = x + 18
    cursor = section_tag(canvas, inner_x, y + 16, tag, accent)
    head_face = load_font(BOLD, head_size)
    cursor = paint_lines(canvas, fit_lines(canvas, headline, head_face, w - 36),
                         inner_x, cursor, head_face, NAVY, head_size + 7)
    deck_face = load_font(REGULAR, 26)
    paint_lines(canvas, fit_lines(canvas, deck, deck_face, w - 36),
                inner_x, cursor + 4, deck_face, SMOKE, 32)


def draw_tanker_ship(canvas, cx, cy, colour):
    """A small line-art tanker riding on two sketched waves."""
    canvas.polygon(
        [(cx - 78, cy - 8), (cx + 78, cy - 8), (cx + 62, cy + 22),
         (cx - 62, cy + 22)],
        outline=colour, width=5)
    canvas.line([cx - 78, cy - 8, cx + 78, cy - 8], fill=colour, width=5)
    canvas.rectangle([cx + 34, cy - 44, cx + 66, cy - 8],
                     outline=colour, width=4)
    canvas.rectangle([cx - 58, cy - 30, cx - 42, cy - 8],
                     outline=colour, width=4)
    canvas.line([cx - 30, cy - 8, cx - 30, cy - 26], fill=colour, width=4)
    for dy, left, right in ((44, cx - 84, cx - 20), (44, cx - 4, cx + 84),
                            (62, cx - 70, cx + 10), (62, cx + 26, cx + 78)):
        canvas.arc([left, cy + dy - 10, right, cy + dy + 10],
                   start=200, end=340, fill=colour, width=4)


def build_sheet():
    sheet = Image.new("RGB", CANVAS, PAPER)
    pen = ImageDraw.Draw(sheet)

    # Masthead: date, title line, story count.
    pen.rectangle([0, 0, 1024, 100], fill=DEEP_NAVY)
    pen.text((28, 16), "MONDAY, 23 NOVEMBER 2026",
             font=load_font(BOLD, 46), fill=SNOW)
    pen.text((28, 66), "T H E   W O R L D   I N   O N E   I M A G E",
             font=load_font(BOLD, 20), fill=GILT)
    pen.text((1024 - 28, 68), "SIX STORIES — ONE DAY",
             font=load_font(BOLD, 20), fill=MIST, anchor="ra")

    # Lead story: tanker attacks in the Strait of Hormuz.
    lead_x, lead_y, lead_w, lead_h = 28, 116, 968, 288
    pen.rectangle([lead_x, lead_y, lead_x + lead_w, lead_y + lead_h], fill=SNOW)
    pen.rectangle([lead_x, lead_y, lead_x + lead_w, lead_y + 6], fill=CRIMSON)
    text_x = lead_x + 28
    cursor = section_tag(pen, text_x, lead_y + 20,
                         "IRAN WAR  •  STRAIT OF HORMUZ", CRIMSON)
    lead_face = load_font(BOLD, 64)
    cursor = paint_lines(pen, fit_lines(pen, "HORMUZ UNDER FIRE", lead_face, 640),
                         text_x, cursor, lead_face, NAVY, 72)
    deck_face = load_font(REGULAR, 26)
    paint_lines(pen, fit_lines(pen, "Three tankers hit in two days as attacks reach their "
                                    "highest level since the US–Iran war began. Bahrain "
                                    "takes its case to the UN.",
                               deck_face, 640),
                text_x, cursor + 6, deck_face, SMOKE, 32)
    draw_tanker_ship(pen, 872, lead_y + 150, CRIMSON)

    # Four secondary stories in a two-by-two grid.
    stories = [
        (OCEAN, "WAR IN UKRAINE  •  LIBYA",
         "Russian warship sinks off Libya",
         "Merkury capsized after a suspected Ukrainian sea-drone strike.", 34),
        (GRAPE, "USA  •  MIDTERMS",
         "Democrats hit 258 — biggest majority since 1992",
         "Hubbard beats Foxx by 330 votes in North Carolina.", 30),
        (EMBER, "MARKETS  •  SEOUL",
         "AI sell-off spreads: Kospi sinks 2.8% at open",
         "Kospi down 46.6% from its June peak; Seoul readies a rescue fund.", 34),
        (TEAL, "HEALTH  •  DR CONGO",
         "WHO pleads for peace as Ebola fight is disrupted",
         "Fighting near a hospital puts patients at grave risk.", 34),
    ]
    for index, (accent, tag, headline, deck, size) in enumerate(stories):
        x = 28 + (index % 2) * 496
        y = 420 + (index // 2) * 206
        story_card(pen, x, y, 472, 190, accent, tag, headline, deck, size)

    # Climate strip: COP31 ends with no agreement.
    strip_x, strip_y, strip_w, strip_h = 28, 832, 968, 96
    pen.rectangle([strip_x, strip_y, strip_x + strip_w, strip_y + strip_h], fill=SNOW)
    pen.rectangle([strip_x, strip_y, strip_x + strip_w, strip_y + 5], fill=LEAF)
    section_tag(pen, strip_x + 18, strip_y + 14,
                "CLIMATE  •  ANTALYA AFTERMATH", LEAF)
    pen.text((strip_x + 18, strip_y + 46),
             "COP31 collapses without a deal",
             font=load_font(BOLD, 30), fill=NAVY)
    pen.text((strip_x + strip_w - 18, strip_y + 18), "194",
             font=load_font(BOLD, 46), fill=LEAF, anchor="ra")
    pen.text((strip_x + strip_w - 18, strip_y + 66), "nations, no deal",
             font=load_font(REGULAR, 18), fill=SMOKE, anchor="ra")

    # Bottom bar: Monday markets ticker and sources.
    pen.rectangle([0, 944, 1024, 1024], fill=DEEP_NAVY)
    pen.text((28, 956), "MONDAY MARKETS  •  Kospi −2.8% — S&P 500 in correction, "
                        "Nasdaq 100 in bear market",
             font=load_font(BOLD, 23), fill=SNOW)
    pen.text((28, 988), "Sources: CNN, Reuters, AP, Al Jazeera, AFP  •  23 November 2026",
             font=load_font(REGULAR, 17), fill=MIST)

    return sheet


def main():
    sheet = build_sheet()
    sheet.save("entry.png", optimize=True)
    print("saved entry.png", sheet.size)


if __name__ == "__main__":
    main()
