"""Draw the front-page poster for Friday 20 November 2026.

A single broadsheet front page, "The World in One Picture", drawn
entirely with Pillow: a masthead, one lead story, four more stories
in a grid, and a small line-art globe. The drawing is a pure
function of the constants below -- no randomness, no clock, no
network -- so running it twice produces byte-identical PNGs.

Run it directly to (re)draw the entry image beside this file:
    python3 render.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024
MARGIN = 46
CONTENT = WIDTH - 2 * MARGIN

PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (163, 22, 33)
MUTED = (96, 91, 82)
RULE = (150, 143, 130)
GLOBE_FILL = (224, 232, 236)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

SERIF = "DejaVuSerif.ttf"
SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"

LEAD = {
    "kicker": "WASHINGTON · THE IRAN DECISION",
    "headline": "TRUMP PUTS IRAN DECISION OFF TO 2027",
    "deck": "“We’ll see what happens after January 1,” the president says, "
            "in no rush over fresh strikes.",
}

GRID = [
    (
        "BERLIN · THE UKRAINE WAR",
        "EUROPE READY TO TALK TO RUSSIA",
        "At a Berlin summit, Merz says Europe will negotiate — with "
        "Kyiv and Europe at the table.",
    ),
    (
        "ODISHA · THE STORM",
        "CYCLONE AKVAN COMES ASHORE",
        "Weakened but still fierce, the storm crosses the coast near "
        "Gopalpur. Three lakh people moved to safety.",
    ),
    (
        "SPACE · THE LONGEST VOYAGE",
        "VOYAGER 1, ONE LIGHT-DAY OUT",
        "After 49 years, the probe is 16.1 billion miles out — the "
        "first object a full light-day from Earth.",
    ),
    (
        "SEOUL · THE MARTIAL-LAW TRIAL",
        "SEOUL COURT OVERTURNS 15-YEAR TERM",
        "The Supreme Court overturns the 15-year term for ex-PM Han "
        "Duck-soo; the case goes back for retrial.",
    ),
]

FOOTER = ("Sources: Reuters · Yonhap · India Meteorological Department "
          "· NASA · wire reports — 20 November 2026")


def load_font(filename, size):
    """Load a DejaVu font, falling back to Pillow's built-in font."""
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, filename), size)
    except OSError:
        return ImageFont.load_default()


def wrap_text(text, font, max_width):
    """Split text into lines that fit max_width, breaking on words."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if font.getlength(trial) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_block(draw, text, font, x, y, max_width, leading, fill=INK):
    """Draw wrapped text starting at (x, y); return the y below it."""
    for line in wrap_text(text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def tracked_width(text, font, tracking):
    """Width of text drawn with extra space between letters."""
    width = sum(font.getlength(ch) for ch in text)
    return width + tracking * max(len(text) - 1, 0)


def draw_tracked_centered(draw, text, font, cx, y, tracking, fill=INK):
    """Draw text centred on cx with extra space between letters."""
    x = cx - tracked_width(text, font, tracking) / 2
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + tracking


def draw_globe(draw, cx, cy, radius):
    """A small line-art globe: meridians, parallels, an orbit ring."""
    box = [cx - radius, cy - radius, cx + radius, cy + radius]
    draw.ellipse(box, fill=GLOBE_FILL, outline=INK, width=3)
    for fraction in (0.35, 0.7):
        rx = radius * fraction
        draw.ellipse(
            [cx - rx, cy - radius, cx + rx, cy + radius],
            outline=INK, width=2,
        )
    for dy in (-0.55, 0.0, 0.55):
        y = cy + radius * dy
        half = (radius ** 2 - (radius * dy) ** 2) ** 0.5
        draw.line([(cx - half, y), (cx + half, y)], fill=INK, width=2)
    orbit = [
        cx - radius - 16, cy - radius * 0.42,
        cx + radius + 16, cy + radius * 0.42,
    ]
    draw.ellipse(orbit, outline=RED, width=2)
    sx, sy = cx, cy - radius * 0.42
    star = [
        (sx, sy - 7), (sx + 2, sy - 2), (sx + 7, sy), (sx + 2, sy + 2),
        (sx, sy + 7), (sx - 2, sy + 2), (sx - 7, sy), (sx - 2, sy - 2),
    ]
    draw.polygon(star, fill=RED)


def draw_story_cell(draw, box, kicker, headline, deck):
    """One grid cell: red kicker, bold headline, short deck."""
    x, y, width = box
    kicker_font = load_font(SANS_BOLD, 17)
    draw.text((x, y), kicker, font=kicker_font, fill=RED)
    y += 26
    headline_font = load_font(SERIF_BOLD, 28)
    y = draw_block(draw, headline, headline_font, x, y, width, 34)
    y += 4
    deck_font = load_font(SERIF, 18)
    draw_block(draw, deck, deck_font, x, y, width, 22)


def build_poster():
    """Compose the whole front page and return the image."""
    image = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(image)

    draw.rectangle([26, 26, WIDTH - 27, HEIGHT - 27], outline=INK, width=3)
    draw.rectangle([34, 34, WIDTH - 35, HEIGHT - 35], outline=RULE, width=1)

    header_font = load_font(SANS_BOLD, 20)
    draw.text((MARGIN, 52), "FRIDAY · 20 NOVEMBER 2026",
              font=header_font, fill=INK)
    right = "FIVE STORIES · ONE PLANET"
    draw.text((WIDTH - MARGIN - header_font.getlength(right), 52), right,
              font=header_font, fill=INK)
    draw.line([(MARGIN, 84), (WIDTH - MARGIN, 84)], fill=INK, width=2)

    masthead_font = load_font(SERIF_BOLD, 92)
    title = "THE WORLD"
    draw.text(((WIDTH - masthead_font.getlength(title)) / 2, 92), title,
              font=masthead_font, fill=INK)
    subtitle_font = load_font(SANS_BOLD, 32)
    draw_tracked_centered(draw, "IN ONE PICTURE", subtitle_font,
                          WIDTH / 2, 192, 10)
    draw.line([(MARGIN, 234), (WIDTH - MARGIN, 234)], fill=INK, width=2)
    draw.line([(MARGIN, 240), (WIDTH - MARGIN, 240)], fill=RULE, width=1)

    y = 256
    kicker_font = load_font(SANS_BOLD, 20)
    draw.text((MARGIN, y), LEAD["kicker"], font=kicker_font, fill=RED)
    y += 28
    headline_font = load_font(SERIF_BOLD, 54)
    y = draw_block(draw, LEAD["headline"], headline_font,
                   MARGIN, y, CONTENT, 62)
    y += 8
    deck_font = load_font(SERIF, 24)
    y = draw_block(draw, LEAD["deck"], deck_font, MARGIN, y, CONTENT, 31)

    draw.line([(MARGIN, 490), (WIDTH - MARGIN, 490)], fill=RULE, width=1)
    draw_globe(draw, WIDTH / 2, 548, 50)
    side_font = load_font(SANS_BOLD, 18)
    left = "ONE DAY"
    draw.text((WIDTH / 2 - 50 - 40 - side_font.getlength(left), 539), left,
              font=side_font, fill=MUTED)
    draw.text((WIDTH / 2 + 50 + 40, 539), "ONE PLANET",
              font=side_font, fill=MUTED)
    draw.line([(MARGIN, 608), (WIDTH - MARGIN, 608)], fill=RULE, width=1)

    col_width = (CONTENT - 30) // 2
    grid_top = 622
    row_height = 160
    row_gap = 8
    draw.line([(WIDTH / 2, grid_top), (WIDTH / 2, grid_top + 2 * row_height + row_gap)],
              fill=RULE, width=1)
    draw.line([(MARGIN, grid_top + row_height + row_gap // 2),
               (WIDTH - MARGIN, grid_top + row_height + row_gap // 2)],
              fill=RULE, width=1)
    positions = [
        (MARGIN, grid_top),
        (WIDTH / 2 + 15, grid_top),
        (MARGIN, grid_top + row_height + row_gap),
        (WIDTH / 2 + 15, grid_top + row_height + row_gap),
    ]
    for (kicker, headline, deck), (x, top) in zip(GRID, positions):
        draw_story_cell(draw, (x, top, col_width), kicker, headline, deck)

    footer_y = 958
    draw.line([(MARGIN, footer_y), (WIDTH - MARGIN, footer_y)],
              fill=INK, width=1)
    footer_font = load_font(SANS, 15)
    draw.text(((WIDTH - footer_font.getlength(FOOTER)) / 2, 968), FOOTER,
              font=footer_font, fill=MUTED)

    return image


def save_poster(path):
    """Render the poster and write it to path as a PNG."""
    build_poster().save(path, format="PNG")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    save_poster(path)
    print("wrote", path)


if __name__ == "__main__":
    main()
