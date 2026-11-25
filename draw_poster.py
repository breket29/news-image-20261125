#!/usr/bin/env python3
"""Draw the news-image-20261125 poster: 'THE WORLD IN ONE DAY / WEDNESDAY, 25 NOVEMBER 2026'.

A newspaper front page, 1024x1024 PNG, drawn entirely with PIL (no photos).
Four stories, all verified against reputable sources on 25 Nov 2026:
  1. AI selloff: a day after Nvidia jumped 31.5% on Jensen Huang's
     reinstatement, the Nasdaq fell 1.5%, S&P 500 0.5%, Nvidia ~6%,
     Micron 11%, Philly chip index ~8%; the Trump administration is
     preparing tariff hikes on China, the EU and 14 other economies
     (WSJ) — Reuters / WSJ
  2. Ukraine drone strikes on Russian ships: Zelenskiy confirmed a hit
     on a Russian cargo ship in the Gulf of Finland; Russia accused
     Ukraine of "terrorist acts" after strikes in the gulf and off
     Benghazi, Libya — Reuters / AP
  3. First Pakistani in orbit: Muhammad Zeeshan Ali, 40, PAF pilot,
     launched 25 Nov 05:18 PKT aboard China's Shenzhou-24 to Tiangong;
     first Pakistani in orbit, first foreign astronaut aboard Tiangong
     — Reuters / AP
  4. Huawei guilty: a US jury on 24 Nov found Huawei guilty of stealing
     trade secrets, 10 of 12 counts, including bank fraud — Reuters / AP
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (176, 42, 30)
BLUE = (31, 78, 121)
GRAY = (85, 85, 85)
LIGHT = (233, 227, 214)
SEA = (38, 92, 130)
SAND = (214, 196, 150)
GREEN = (28, 120, 60)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
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


def draw_text_block(draw, x, y, max_w, lines, fnt, fill=INK, leading=6):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def hrule(draw, x0, x1, y, w=3, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def draw_chart_fall(draw, x, y, w, h):
    # falling stock chart: axes, gridlines, steep falling line, arrow, -6%
    ox, oy = x + 14, y + h - 26
    top = y + 34
    right = x + w - 14
    for gy in (oy - 60, oy - 120):
        draw.line([(ox, gy), (right, gy)], fill=(200, 194, 178), width=1)
    draw.line([(ox, top), (ox, oy)], fill=GRAY, width=2)
    draw.line([(ox, oy), (right, oy)], fill=GRAY, width=2)
    pts = [(ox, oy - 158), (ox + 52, oy - 148), (ox + 104, oy - 152),
           (ox + 156, oy - 104), (ox + 208, oy - 52), (ox + 258, oy - 8)]
    draw.line(pts, fill=RED, width=6, joint="curve")
    # arrowhead at the last point
    ex, ey = pts[-1]
    draw.polygon([(ex, ey + 14), (ex + 16, ey - 2), (ex - 2, ey - 2)], fill=RED)
    draw.text((x + 16, y + 8), "-6%", font=font(SANS_B, 34), fill=RED)
    f_nas = font(SANS_B, 20)
    nas = "Nasdaq -1.5%"
    draw.text((right - draw.textlength(nas, font=f_nas) - 8, y + 14), nas,
              font=f_nas, fill=INK)


def draw_ship_strike(draw, x, y, w, h):
    # sea, cargo ship with containers, a drone streak and a blast
    base = y + h
    for wx in range(x, x + w, 46):
        draw.arc([wx, base - 30, wx + 44, base - 12], 0, 180, fill=SEA, width=4)
    # hull
    draw.polygon([(x + 30, base - 46), (x + w - 20, base - 46),
                  (x + w - 44, base - 14), (x + 54, base - 14)], fill=(60, 64, 70))
    # containers
    for cx in (x + 60, x + 108, x + 156):
        draw.rectangle([cx, base - 76, cx + 42, base - 46], fill=(176, 42, 30),
                       outline=INK, width=1)
    draw.rectangle([x + 204, base - 76, x + 240, base - 46], fill=BLUE,
                   outline=INK, width=1)
    # bridge tower
    draw.rectangle([x + w - 62, base - 96, x + w - 28, base - 46],
                   fill=(220, 220, 220), outline=INK, width=1)
    # drone streak + blast
    draw.line([(x + 20, y + 12), (x + 84, y + 44)], fill=INK, width=3)
    draw.polygon([(x + 84, y + 44), (x + 100, y + 36), (x + 96, y + 54)],
                 fill=INK)
    for (bx, by, r) in ((x + 96, y + 52, 7), (x + 108, y + 62, 9),
                        (x + 88, y + 64, 6)):
        draw.ellipse([bx - r, by - r, bx + r, by + r], fill=(240, 140, 20))


def draw_rocket(draw, x, y, w, h):
    # stars, a rocket rising on a flame trail
    import random
    random.seed(25)
    for _ in range(14):
        sx = x + random.randint(4, w - 8)
        sy = y + random.randint(4, h - 60)
        draw.ellipse([sx, sy, sx + 4, sy + 4], fill=GRAY)
    cx = x + w // 2
    base = y + h
    # flame trail
    draw.polygon([(cx - 10, base - 40), (cx, base - 6), (cx + 10, base - 40)],
                 fill=(240, 140, 20))
    draw.polygon([(cx - 5, base - 40), (cx, base - 22), (cx + 5, base - 40)],
                 fill=(240, 200, 40))
    # body
    draw.polygon([(cx - 16, base - 40), (cx, base - 104), (cx + 16, base - 40)],
                 fill=(220, 220, 220), outline=INK)
    draw.rectangle([cx - 16, base - 66, cx + 16, base - 40], fill=GREEN)
    # fins
    draw.polygon([(cx - 16, base - 40), (cx - 34, base - 16), (cx - 16, base - 16)],
                 fill=(176, 42, 30))
    draw.polygon([(cx + 16, base - 40), (cx + 34, base - 16), (cx + 16, base - 16)],
                 fill=(176, 42, 30))
    # window
    draw.ellipse([cx - 7, base - 92, cx + 7, base - 78], fill=BLUE,
                 outline=INK, width=1)


def draw_gavel(draw, x, y, w, h):
    # judge's gavel: head, handle, sound block, motion lines
    cx, cy = x + w // 2, y + h // 2 - 6
    # motion arcs above the head
    for r in (34, 46):
        draw.arc([cx - r, cy - r - 18, cx + r, cy + r - 18], 180, 360,
                 fill=GRAY, width=3)
    # head (tilted block)
    draw.polygon([(cx - 52, cy - 26), (cx + 44, cy - 44), (cx + 52, cy - 24),
                  (cx - 44, cy - 6)], fill=(120, 72, 32), outline=INK)
    # handle
    draw.line([(cx + 6, cy - 10), (cx + 62, cy + 42)], fill=(96, 58, 26),
              width=10)
    # sound block
    draw.ellipse([cx - 58, cy + 34, cx + 6, cy + 52], fill=(70, 46, 24),
                 outline=INK, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    hrule(d, 28, 996, 26, 4)
    f_mast = font(SERIF, 62)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 44), title, font=f_mast, fill=INK)
    f_date = font(SANS_B, 25)
    date = "WEDNESDAY,  25  NOVEMBER  2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 122), date, font=f_date, fill=RED)
    hrule(d, 28, 996, 162, 3)
    hrule(d, 28, 996, 168, 1)

    # ---- lead story: AI selloff ----
    f_kick = font(SANS_B, 20)
    d.text((40, 188), "MARKETS  •  NEW YORK", font=f_kick, fill=RED)
    f_h1_size = 54
    while (f_h1_size > 30 and
           d.textlength("AI SHARES TUMBLE", font=font(SERIF, f_h1_size)) > 560):
        f_h1_size -= 2
    f_h1 = font(SERIF, f_h1_size)
    y = 218
    y = draw_text_block(d, 40, y, 560, ["AI SHARES TUMBLE"], f_h1, leading=2)
    f_h2 = font(SERIF, 28)
    y = draw_text_block(
        d, 40, y + 8, 560,
        wrap(d, "Chips sink a day after Nvidia's surge", f_h2, 560),
        f_h2, leading=4)
    f_body = font(SANS, 20)
    body = ("A day after Nvidia's 31.5% jump on Huang's "
            "return, AI shares slid: the Nasdaq fell 1.5%, "
            "the S&P 500 0.5%, Nvidia about 6%, Micron 11% "
            "and the Philly chip index about 8%. Washington "
            "is preparing tariff rises on China, the EU and "
            "14 others, the Journal reported.")
    y = draw_text_block(d, 40, y + 12, 560, wrap(d, body, f_body, 560), f_body, leading=6)
    print("lead body bottom y:", y)
    # lead illustration: falling chart
    d.rectangle([640, 188, 984, 470], outline=INK, width=2, fill=LIGHT)
    draw_chart_fall(d, 648, 196, 328, 266)
    d.text((652, 448), "The rally lasts a day; chips give it back.", font=font(SANS, 16), fill=GRAY)

    hrule(d, 40, 984, 496, 2)

    # ---- three stories in a row ----
    cols = [
        dict(x=40, w=296, kick="UKRAINE  •  GULF OF FINLAND", head="Kyiv hits\nRussian ships",
             body=("President Zelenskiy confirmed Ukrainian "
                   "drones hit a Russian cargo ship in the "
                   "Gulf of Finland. Moscow accused Kyiv of "
                   "'terrorist acts' after strikes in the gulf "
                   "and off Benghazi, Libya."),
             art=draw_ship_strike),
        dict(x=364, w=296, kick="SPACE  •  TIANGONG", head="First Pakistani\nin orbit",
             body=("Muhammad Zeeshan Ali, 40, a Pakistan Air "
                   "Force pilot, launched aboard China's "
                   "Shenzhou-24 at 05:18 PKT on Tuesday — the "
                   "first Pakistani in orbit and the first "
                   "foreign astronaut aboard Tiangong."),
             art=draw_rocket),
        dict(x=688, w=296, kick="COURTS  •  UNITED STATES", head="Huawei guilty\non 10 counts",
             body=("A US jury found Huawei guilty of stealing "
                   "trade secrets on 10 of 12 counts, "
                   "including bank fraud, in a verdict "
                   "delivered on Tuesday."),
             art=draw_gavel),
    ]
    f_kick2 = font(SANS_B, 17)
    f_head = font(SERIF, 32)
    f_body2 = font(SANS, 20)
    for c in cols:
        x, w = c["x"], c["w"]
        d.text((x, 516), c["kick"], font=f_kick2, fill=RED)
        # art panel
        d.rectangle([x, 548, x + w, 668], outline=INK, width=2, fill=LIGHT)
        c["art"](d, x + 8, 552, w - 16, 112)
        y = 684
        y = draw_text_block(d, x, y, w, c["head"].split("\n"), f_head, leading=2)
        y = draw_text_block(d, x, y + 8, w, wrap(d, c["body"], f_body2, w), f_body2, leading=6)
        print("column bottom y:", c["kick"], y)

    hrule(d, 40, 984, 972, 2)
    f_foot = font(SANS, 16)
    d.text((40, 984), "Sources: Reuters · AP",
           font=f_foot, fill=GRAY)
    d.text((640, 984), "THE WORLD IN ONE DAY — 25 NOV 2026",
           font=f_foot, fill=GRAY)

    img.save("poster.png", "PNG")
    print("saved poster.png", img.size)


if __name__ == "__main__":
    main()
