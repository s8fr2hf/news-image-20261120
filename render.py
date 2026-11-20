"""Draw the 20 November 2026 front-page poster to entry.png (build time only).

Layout (1024x1024, all drawing done here with Pillow):
  masthead band, lead story with three country discs, a 2x2 grid of
  further stories, and a ticker strip along the bottom.
Everything is fixed text, so the output is fully deterministic.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 241, 227)
NAVY = (20, 36, 62)
NAVY_LIGHT = (34, 58, 92)
GOLD = (184, 138, 44)
GOLD_LIGHT = (214, 172, 84)
INK = (24, 24, 24)
GREY = (92, 92, 92)
RED = (158, 34, 34)
WHITE = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=None):
    """Draw wrapped text, return the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.25)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.3)


def panel(draw, x, y, w, h, kicker, headline, body):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=NAVY, width=2)
    draw.rectangle([x, y, x + w, y + 30], fill=NAVY)
    draw.text((x + 12, y + 5), kicker, font=font(SANS_BOLD, 17), fill=GOLD_LIGHT)
    text_block(draw, x + 12, y + 44, headline, font(SANS_BOLD, 24),
               RED, w - 24, leading=30)
    text_block(draw, x + 12, y + 108, body, font(SANS, 19),
               INK, w - 24, leading=25)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # --- masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 132], fill=NAVY)
    d.rectangle([0, 132, W, 138], fill=GOLD)
    centred(d, W // 2, 16, "THE WORLD IN ONE PICTURE",
            font(SERIF, 52), WHITE)
    centred(d, W // 2, 82, "FRIDAY  ·  20 NOVEMBER 2026",
            font(SANS_BOLD, 26), GOLD_LIGHT)

    # --- lead story -----------------------------------------------------
    d.rectangle([28, 160, W - 28, 452], fill=WHITE, outline=NAVY, width=2)
    d.text((48, 176), "WASHINGTON  ·  IRAN DECISION",
           font=font(SANS_BOLD, 18), fill=GOLD)
    text_block(d, 48, 206, "TRUMP PUTS IRAN CALL OFF UNTIL 2027",
               font(SERIF, 40), NAVY, W - 96, leading=48)
    text_block(d, 48, 306,
               "No rush on new strikes, he tells Reuters: "
               "'We'll see what happens after January 1.' "
               "Netanyahu had pressed for a second bombing campaign.",
               font(SANS, 24), INK, 620, leading=31)
    # three country discs
    discs = [("USA", NAVY_LIGHT), ("IRN", RED), ("ISR", (58, 96, 58))]
    cx = 760
    for label, colour in discs:
        d.ellipse([cx, 300, cx + 74, 374], fill=colour, outline=GOLD, width=3)
        tw = d.textlength(label, font=font(SANS_BOLD, 20))
        d.text((cx + (74 - tw) / 2, 328), label,
               font=font(SANS_BOLD, 20), fill=WHITE)
        cx += 84
    d.line([48, 402, 976, 402], fill=GOLD, width=2)
    d.text((48, 412), "$48bn: cost of US operations against Iran since February, the Pentagon told Congress",
           font=font(SANS, 19), fill=GREY)

    # --- 2x2 grid --------------------------------------------------------
    gx, gy = 28, 474
    pw, ph, gap = 472, 196, 24
    panel(d, gx, gy, pw, ph, "BERLIN",
          "EUROPE READY FOR TALKS WITH RUSSIA",
          "Coalition of the Willing leaders say they are ready to negotiate an end to the Ukraine war.")
    panel(d, gx + pw + gap, gy, pw, ph, "ODISHA",
          "CYCLONE AKVAN LANDFALL TODAY",
          "300,000 evacuated as the severe storm nears Gopalpur, gusts to 110 km/h.")
    panel(d, gx, gy + ph + gap, pw, ph, "SPACE",
          "VOYAGER 1 ONE LIGHT-DAY AWAY",
          "NASA confirms the probe crossed 25.9 billion km on 18 Nov; a signal now takes 24 hours each way.")
    panel(d, gx + pw + gap, gy + ph + gap, pw, ph, "SEOUL",
          "HAN'S 15-YEAR TERM OVERTURNED",
          "Top court sends the ex-PM's martial-law case back for retrial; other findings stand.")

    # --- ticker ----------------------------------------------------------
    d.rectangle([0, 916, W, H], fill=NAVY)
    d.rectangle([0, 916, W, 922], fill=GOLD)
    ticker = ("GTA 6 passes $1.84bn, topping The Odyssey's box office  \u00b7  "
              "Hayabusa2 retargeted after engine failure  \u00b7  "
              "Nicholls 113* lifts NZ to 243/5 vs India  \u00b7  "
              "Russian strikes damage Austrian and Dutch embassies in Kyiv")
    text_block(d, 28, 936, ticker, font(SANS_BOLD, 22), WHITE,
               W - 56, leading=30)

    img.save("entry.png", "PNG", optimize=True)


if __name__ == "__main__":
    main()
